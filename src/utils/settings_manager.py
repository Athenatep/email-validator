import json
import logging
from pathlib import Path
from typing import Dict, Any

class SettingsManager:
    """Manages application settings."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings_file = Path.home() / '.email_validator' / 'settings.json'
        self.settings_file.parent.mkdir(exist_ok=True)
        self.settings = self._load_settings()
        
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            return self._get_default_settings()
            
        except Exception as e:
            self.logger.error(f"Error loading settings: {str(e)}")
            return self._get_default_settings()
            
    def _save_settings(self):
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving settings: {str(e)}")
            
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            "validation_options": {
                "check_syntax": True,
                "check_domain": True,
                "check_mx": True,
                "check_smtp": True,
                "check_disposable": True,
                "check_spam": True,
                "check_reputation": True,
                "check_typos": True,
                "check_duplicates": True
            },
            "batch_size": 100,
            "theme": "light_blue",
            "last_directory": str(Path.home()),
            "export_format": "csv"
        }
        
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        return self.settings.get(key, default)
        
    def set_setting(self, key: str, value: Any):
        """Set setting value."""
        self.settings[key] = value
        self._save_settings()
        
    def get_validation_options(self) -> Dict[str, bool]:
        """Get validation options."""
        return self.settings.get("validation_options", {})
        
    def set_validation_options(self, options: Dict[str, bool]):
        """Set validation options."""
        self.settings["validation_options"] = options
        self._save_settings()