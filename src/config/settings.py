import json
import os
from typing import Dict

def load_config() -> Dict:
    """
    Load configuration from config file.
    
    Returns:
        Dict containing configuration settings
    """
    config_path = 'config/config.json'
    
    # Create default config if it doesn't exist
    if not os.path.exists(config_path):
        default_config = {
            "batch_size": 1000,
            "cache_enabled": True,
            "cache_timeout": 3600,
            "max_retries": 3,
            "timeout": 10,
            "validation_options": {
                "check_syntax": True,
                "check_mx": True,
                "check_smtp": True,
                "detect_spam_traps": True,
                "detect_catchall": True,
                "check_duplicates": True,
                "similar_email_threshold": 2,
                "disposable_check": True
            },
            "smtp": {
                "timeout": 10,
                "retries": 2,
                "verify_cert": True
            }
        }
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
            
        return default_config
        
    # Load existing config
    with open(config_path, 'r') as f:
        return json.load(f)