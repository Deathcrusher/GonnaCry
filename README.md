# GonnaCry v2.0 - Modernized EDR Testing Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Research](https://img.shields.io/badge/purpose-security%20research-red.svg)]()

**Modernized Linux Ransomware for EDR/Security Testing** - Educational security research tool designed to help test and validate Endpoint Detection and Response (EDR) systems.

## ⚠️ Disclaimer

**This tool is for EDUCATIONAL PURPOSES ONLY.** 

- Must NOT be used to harm, threaten, or hurt other people's computers
- Only use in isolated test environments you own or have explicit permission to test
- Purpose is to share knowledge and awareness about malware, cryptography, and security
- The authors are not responsible for any misuse of this software

## 🎯 Objectives

GonnaCry v2.0 helps security professionals and researchers:
- Test EDR detection capabilities
- Validate IOC (Indicators of Compromise) detection
- Simulate ransomware TTPs (Tactics, Techniques, and Procedures)
- Understand modern encryption schemes used in ransomware
- Train security teams on ransomware response

## ✨ Features

### Modern Encryption
- **AES-256-CBC** for file encryption with random IV per file
- **RSA-2048** for secure key exchange using OAEP padding
- Unique AES key generated for each file
- Secure key management with metadata storage

### Safety First
- **Test Mode**: Safely encrypts only designated test directories
- **Safe Mode**: Prevents encryption of critical system directories (`/bin`, `/etc`, `/usr`, etc.)
- **Environment Variables**: Easy configuration without code changes
- **Explicit Overrides**: Dangerous operations require explicit flags

### EDR Testing Features
- **IOC Markers**: `.GNCRY` file extension for easy detection
- **Ransom Notes**: `README_DECRYPT.txt` files created in encrypted directories
- **Logging**: Comprehensive logging for analysis
- **Metadata Files**: Encryption metadata stored for decryption testing

### Cross-Platform Ready
- Currently supports **Linux** 
- Modular architecture designed for future Windows/macOS support
- Pure Python implementation (pycryptodome)

## 📦 Installation

### Requirements
- Python 3.8+
- pycryptodome library

### Setup
```bash
# Clone repository
cd /workspace

# Install dependencies
pip install pycryptodome

# Verify installation
cd src/GonnaCry
python3 -c "from core.crypto import *; print('✓ Cryptography module OK')"
```

## 🚀 Usage

### Quick Start - Test Mode (Recommended)

Test mode is the safest way to experiment. It only encrypts files in a designated test directory:

```bash
# Run in test mode (creates test files automatically)
cd src/GonnaCry
GONNACRY_TEST_MODE=true python3 main.py --test

# Or using environment variable
export GONNACRY_TEST_MODE=true
python3 main.py --test
```

### Encrypt Specific Directory

```bash
# Encrypt a specific directory (with safety checks)
python3 main.py --directory /path/to/test/files

# With recursive search (default)
python3 main.py -d /path/to/test/files -r
```

### Decrypt Files

```bash
# Decrypt files using saved metadata
python3 main.py --decrypt --directory /path/to/encrypted/files
```

### Advanced Options

```bash
# Show all options
python3 main.py --help

# Disable safety checks (DANGEROUS - only in isolated VM!)
python3 main.py --directory /path --no-safety

# Custom test directory
GONNACRY_TEST_DIR=/custom/test/path python3 main.py --test

# Debug logging
GONNACRY_LOG_LEVEL=DEBUG python3 main.py --test
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GONNACRY_TEST_MODE` | `false` | Enable test mode (safe) |
| `GONNACRY_TEST_DIR` | `./tests/test_files` | Test directory path |
| `GONNACRY_SAFE_MODE` | `true` | Enable safety checks |
| `GONNACRY_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `GONNACRY_LOG_FILE` | `./gonnacry.log` | Log file path |

### Supported File Extensions

The tool targets common user files:
- Documents: `.txt`, `.doc`, `.docx`, `.pdf`, `.xls`, `.xlsx`
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- Media: `.mp3`, `.mp4`, `.avi`, `.mkv`
- Archives: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- Code: `.py`, `.js`, `.html`, `.css`, `.cpp`, `.java`
- Databases: `.db`, `.sql`, `.sqlite`

## 🛡️ EDR Detection Points

Use GonnaCry to test these detection vectors:

### File System IOCs
- New files with `.GNCRY` extension
- `README_DECRYPT.txt` ransom notes
- Rapid file modifications
- Unusual file entropy changes

### Process Behavior
- Python processes accessing multiple user files
- Cryptographic API usage patterns
- File deletion after encryption
- Metadata file creation

### Network (Future)
- RSA key exchange attempts
- C2 communication patterns
- Unusual outbound connections

## 📁 Project Structure

```
src/GonnaCry/
├── main.py              # Main entry point
├── config/
│   ├── __init__.py
│   └── settings.py      # Configuration & environment variables
├── core/
│   ├── __init__.py
│   └── crypto.py        # AES-256 & RSA-2048 encryption
├── utils/
│   ├── __init__.py
│   └── file_ops.py      # File operations & safety checks
├── tests/
│   └── test_files/      # Safe test directory
└── gonnacry.log         # Runtime logs
```

## 🧪 Testing Workflow

### 1. Prepare Test Environment
```bash
# Create test directory
mkdir -p /tmp/gonnacry_test
echo "Important document" > /tmp/gonnacry_test/document.txt
echo "Secret data" > /tmp/gonnacry_test/secrets.docx
```

### 2. Run Encryption Test
```bash
cd src/GonnaCry
python3 main.py --directory /tmp/gonnacry_test
```

### 3. Verify EDR Detection
Check your EDR console for:
- File encryption alerts
- IOC matches (`.GNCRY` extension)
- Suspicious process behavior

### 4. Decrypt and Recover
```bash
python3 main.py --decrypt --directory /tmp/gonnacry_test
```

### 5. Analyze Logs
```bash
cat gonnacry.log
```

## 🔐 How Encryption Works

1. **Key Generation**: RSA-2048 key pair generated per session
2. **File Encryption**: Each file gets unique AES-256-CBC key
3. **Key Wrapping**: AES keys encrypted with RSA public key
4. **Metadata Storage**: Encrypted keys + RSA private key saved locally
5. **Secure Deletion**: Original files securely overwritten

In a real attack scenario, the RSA private key would be sent to a C2 server. For testing, it's stored in metadata files.

## 📚 Educational Resources

- [How Ransomware Works](https://0x00sec.org/t/how-ransomware-works-and-gonnacry-linux-ransomware/4594)
- [Encryption Techniques](https://medium.com/@tarcisioma/ransomware-encryption-techniques-696531d07bb9)
- [Industry Impact](https://medium.com/@tarcisioma/how-can-a-malware-encrypt-a-company-existence-c7ed584f66b3)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Windows and macOS support
- Additional encryption modes
- More realistic TTP simulation
- Enhanced EDR evasion techniques (for research)
- Automated testing frameworks

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Original GonnaCry project by [Tarcisio Marinho](https://github.com/tarcisio-marinho/GonnaCry)

Modernized for educational purposes to help security professionals better understand and defend against ransomware threats.

---

**Remember**: Use responsibly and only in authorized test environments!
