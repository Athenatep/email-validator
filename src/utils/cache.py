import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class Cache:
    def __init__(self, ttl_seconds: int = 3600):
        self.logger = logging.getLogger(__name__)
        self.ttl = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = {}
        
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/missing
        """
        try:
            if key in self.cache:
                entry = self.cache[key]
                if datetime.now() < entry['expires']:
                    return entry['value']
                else:
                    del self.cache[key]
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving from cache: {str(e)}")
            return None
            
    def set(self, key: str, value: Any):
        """
        Set value in cache with expiration.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        try:
            self.cache[key] = {
                'value': value,
                'expires': datetime.now() + timedelta(seconds=self.ttl)
            }
        except Exception as e:
            self.logger.error(f"Error setting cache: {str(e)}")
            
    def clear(self):
        """Clear all expired entries from cache."""
        try:
            now = datetime.now()
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry['expires'] < now
            ]
            for key in expired_keys:
                del self.cache[key]
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")