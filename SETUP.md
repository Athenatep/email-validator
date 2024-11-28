# Windows Setup Guide

## Prerequisites Installation

1. **Install Python 3.9+**
   ```
   - Download Python from https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation
   - Verify installation: python --version
   ```

2. **Install Git (Optional)**
   ```
   - Download from https://git-scm.com/download/win
   - Use default installation options
   ```

## Project Setup

1. **Create Project Directory**
   ```
   mkdir email-validator
   cd email-validator
   ```

2. **Create Virtual Environment**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Create Required Directories**
   ```
   mkdir logs
   mkdir reports
   mkdir reports\visualizations
   mkdir data
   mkdir config
   ```

5. **Copy Configuration Files**
   ```
   - Copy config/config.json to the config directory
   - Copy data/disposable_domains.json to the data directory
   ```

## Running the Application

1. **GUI Interface**
   ```
   python src/main.py
   ```

2. **REST API**
   ```
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```

3. **Run Tests**
   ```
   python -m pytest tests/
   ```

## Troubleshooting

1. **PyQt6 Installation Issues**
   - Install Visual C++ Redistributable
   - Run: pip install --force-reinstall PyQt6

2. **DNS Resolution Issues**
   - Check Windows firewall settings
   - Verify DNS server configuration

3. **SMTP Connection Problems**
   - Check network connectivity
   - Verify port 25 is not blocked

4. **Permission Issues**
   - Run as administrator if needed
   - Check folder permissions

## Environment Variables

Optional environment variables:
```
EMAIL_VALIDATOR_CONFIG=path/to/config.json
EMAIL_VALIDATOR_LOG_LEVEL=INFO
EMAIL_VALIDATOR_CACHE_SIZE=10000
```

## Updating

1. **Update Dependencies**
   ```
   pip install --upgrade -r requirements.txt
   ```

2. **Update Configuration**
   ```
   - Backup existing config.json
   - Copy new config template
   - Merge custom settings
   ```

## Support

For issues:
1. Check logs in logs/email_validator.log
2. Verify configuration in config/config.json
3. Ensure all dependencies are installed
4. Check Windows Event Viewer for errors