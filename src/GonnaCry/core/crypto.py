"""
Modern Cryptography Module for GonnaCry
Uses pycryptodome for AES-256 and RSA-2048 encryption
"""

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import base64


class AESCipher:
    """AES-256-CBC cipher for file encryption"""
    
    def __init__(self, key=None):
        if key is None:
            self.key = get_random_bytes(32)  # 256 bits
        else:
            self.key = key if len(key) == 32 else key.ljust(32, b'\0')[:32]
    
    def encrypt(self, plaintext):
        """Encrypt data with AES-256-CBC"""
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # PKCS7 padding
        pad_len = 16 - (len(plaintext) % 16)
        padded_data = plaintext + bytes([pad_len]) * pad_len
        
        ciphertext = cipher.encrypt(padded_data)
        return iv + ciphertext
    
    def decrypt(self, ciphertext):
        """Decrypt data with AES-256-CBC"""
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(actual_ciphertext)
        
        # Remove PKCS7 padding
        pad_len = padded_data[-1]
        return padded_data[:-pad_len]


class RSAKeyPair:
    """RSA-2048 key pair for asymmetric encryption"""
    
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        self.generate_keys()
    
    def generate_keys(self):
        """Generate RSA key pair"""
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()
    
    def get_private_key_pem(self):
        """Export private key in PEM format"""
        return self.private_key.export_key('PEM')
    
    def get_public_key_pem(self):
        """Export public key in PEM format"""
        return self.public_key.export_key('PEM')
    
    def encrypt(self, data):
        """Encrypt data with public key using OAEP padding"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        cipher = PKCS1_OAEP.new(self.public_key, hashAlgo=SHA256)
        return cipher.encrypt(data)
    
    def decrypt(self, encrypted_data):
        """Decrypt data with private key using OAEP padding"""
        cipher = PKCS1_OAEP.new(self.private_key, hashAlgo=SHA256)
        return cipher.decrypt(encrypted_data)


def generate_file_key():
    """Generate a random AES key for file encryption"""
    return get_random_bytes(32)


def encrypt_file_key(file_key, rsa_public_key_pem):
    """Encrypt AES file key with RSA public key"""
    public_key = RSA.import_key(rsa_public_key_pem)
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    return cipher.encrypt(file_key)


def decrypt_file_key(encrypted_key, rsa_private_key_pem):
    """Decrypt AES file key with RSA private key"""
    private_key = RSA.import_key(rsa_private_key_pem)
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    return cipher.decrypt(encrypted_key)
