# GonnaCry v2.0 - Modernized Linux Ransomware for EDR Testing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Educational security research tool for testing EDR (Endpoint Detection and Response) systems**

---

## ⚠️ Disclaimer

This software is provided **FOR EDUCATIONAL PURPOSES ONLY**. 

- **DO NOT** use this to harm, threaten, or hurt other people's computers
- **DO NOT** run this on production systems or files you care about
- **DO** use this in isolated test environments only
- **DO** understand the legal implications before using

---

## 🚀 What's New in v2.0

### Modernization Improvements
- ✅ **Modern Cryptography**: Uses `pycryptodome` instead of deprecated `pycrypto`
- ✅ **Clean Architecture**: Modular design with separate core, utils, and config
- ✅ **Safety Controls**: Built-in protection against accidental system damage
- ✅ **EDR Testing Features**: Test mode, IOC markers, configurable settings

### Encryption Scheme
- ✅ **AES-256-CBC**: Strong symmetric encryption for files
- ✅ **RSA-2048**: Asymmetric encryption for key exchange
- ✅ **Unique Keys**: Each file gets its own random AES key

---

## 📦 Installation

```bash
cd /workspace/src
pip install -r requirements.txt
python3 main.py --help
```

---

## 🎯 Usage

### Basic Test Mode (Recommended)
```bash
# Run in safe test mode
python3 main.py --test

# Or with environment variable
GONNACRY_TEST_MODE=true python3 main.py
```

### Encrypt Specific Directory
```bash
python3 main.py --directory /path/to/test/files
```

### Decrypt Files
```bash
python3 main.py --decrypt --directory /path/to/encrypted/files
```

### Advanced Options
```bash
# Disable safety checks (DANGEROUS!)
python3 main.py --directory /some/path --no-safety

# Set custom test directory
GONNACRY_TEST_DIR=/custom/test/path python3 main.py --test

# Enable debug logging
GONNACRY_LOG_LEVEL=DEBUG python3 main.py --test
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GONNACRY_TEST_MODE` | `false` | Enable safe test mode |
| `GONNACRY_TEST_DIR` | `./tests/test_files` | Test directory path |
| `GONNACRY_SAFE_MODE` | `true` | Enable safety checks |
| `GONNACRY_LOG_LEVEL` | `INFO` | Logging level |

---

## 🛡️ EDR Testing Guide

### Indicators of Compromise (IOCs)
- Encrypted files have `.GNCRY` extension
- Ransom note: `README_DECRYPT.txt`
- Metadata files: `.encryption_metadata_*.dat`

### Testing Scenarios
1. **Detection Test**: Run `--test` and check EDR alerts
2. **Prevention Test**: Verify if EDR blocks execution
3. **Response Test**: Test incident response procedures

---

## 📁 Project Structure

```
GonnaCry/
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
├── config/
│   └── settings.py     # Configuration
├── core/
│   └── crypto.py       # Cryptography module
├── utils/
│   └── file_ops.py     # File operations
└── tests/
    └── test_files/     # Test directory
```

---

## 🔬 How It Works

1. **File Discovery**: Scan for supported file types
2. **Key Generation**: RSA-2048 + unique AES-256 per file
3. **Encryption**: AES-256-CBC with secure original deletion
4. **Key Protection**: AES keys encrypted with RSA public key
5. **Metadata**: Store mapping for decryption

---

## 🤝 Contributing

Areas for improvement:
- [ ] Windows/macOS compatibility
- [ ] Additional encryption algorithms
- [ ] Unit tests
- [ ] Docker containerization

---

## 📝 License

MIT License - Educational purposes only

---

**Original GonnaCry by Tarcisio Marinho**  
**Modernized for EDR Security Testing**
