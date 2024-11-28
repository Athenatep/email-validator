# Ubuntu Installation Guide

## Prerequisites

1. **Python 3.9 or higher**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **System Dependencies**
   The setup script will automatically install required system packages:
   - build-essential
   - Python development files
   - Qt6 dependencies
   - Image processing libraries

## Installation Steps

1. **Download the Project**
   ```bash
   git clone <repository-url>
   # or download and extract ZIP file
   ```

2. **Run Setup Script**
   ```bash
   cd email-validator
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

## Starting the Application

1. **GUI Interface**
   ```bash
   source venv/bin/activate
   python src/main.py
   ```

2. **REST API**
   ```bash
   source venv/bin/activate
   python -m uvicorn src.api.main:app --reload
   ```

## Troubleshooting

1. **Permission Issues**
   ```bash
   sudo chown -R $USER:$USER .
   chmod +x scripts/setup.sh
   ```

2. **Package Installation Errors**
   - Ensure you have internet connection
   - Try running setup script with sudo if needed
   - Check system Python version: `python3 --version`

3. **Virtual Environment Issues**
   ```bash
   rm -rf venv
   ./scripts/setup.sh
   ```

4. **Qt Dependencies**
   If GUI fails to start:
   ```bash
   sudo apt install -y qt6-base-dev libqt6gui6
   ```

## Need Help?

- Check logs in `logs/email_validator.log`
- Verify Python installation: `python3 --version`
- Ensure all dependencies are installed: `pip list`
- Check system package status: `dpkg -l | grep -E 'qt6|python3'`