import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import json
from pathlib import Path

def setup_logger():
    """Configure logging for the application."""
    
    # Load config
    config_path = Path('config/config.json')
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            log_config = config['production']['logging']
    else:
        log_config = {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/email_validator.log",
            "max_size": 10485760,
            "backup_count": 5
        }

    # Create logs directory if it doesn't exist
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Setup logging format
    formatter = logging.Formatter(log_config['format'])
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_config['level'])
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_config['file'],
        maxBytes=log_config['max_size'],
        backupCount=log_config['backup_count']
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Log startup information
    logger.info("Logger initialized")