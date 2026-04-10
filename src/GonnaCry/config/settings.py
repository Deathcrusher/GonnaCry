"""
GonnaCry Configuration Settings
Modernized configuration for EDR testing purposes
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Encryption settings
AES_KEY_SIZE = 256  # bits
RSA_KEY_SIZE = 2048  # bits

# File encryption settings
SUPPORTED_EXTENSIONS = [
    '.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.mp3', '.mp4', '.avi', '.mkv',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.py', '.js', '.html', '.css', '.cpp', '.java',
    '.db', '.sql', '.sqlite',
]

# Test mode settings (for EDR testing)
TEST_MODE = os.getenv('GONNACRY_TEST_MODE', 'false').lower() == 'true'
TEST_DIRECTORY = os.getenv('GONNACRY_TEST_DIR', str(BASE_DIR / 'tests' / 'test_files'))

# IOC markers for EDR detection
IOC_MARKERS = {
    'file_extension': '.GNCRY',
    'ransom_note': 'README_DECRYPT.txt',
    'user_agent': 'GonnaCry/2.0',
}

# Logging
LOG_LEVEL = os.getenv('GONNACRY_LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('GONNACRY_LOG_FILE', str(BASE_DIR / 'gonnacry.log'))

# Safety settings (prevent accidental encryption)
SAFE_MODE = os.getenv('GONNACRY_SAFE_MODE', 'true').lower() == 'true'
SAFE_DIRECTORIES = [
    '/bin', '/sbin', '/usr', '/lib', '/lib64',
    '/etc', '/var', '/proc', '/sys', '/dev',
]

# Network settings (for key exchange simulation)
SERVER_PUBLIC_KEY = None  # Will be generated if not provided
DECRYPTOR_PATH = str(BASE_DIR / 'bin' / 'decryptor')
DAEMON_PATH = str(BASE_DIR / 'bin' / 'daemon')
