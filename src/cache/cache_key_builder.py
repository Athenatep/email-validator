import hashlib
from typing import Dict, Optional, Any

class CacheKeyBuilder:
    """Builds consistent cache keys for different types of cached data"""
    
    @staticmethod
    def build_validation_key(email: str, options: Optional[Dict] = None) -> str:
        """
        Build cache key for validation results.
        
        Args:
            email: Email address
            options: Optional validation options
            
        Returns:
            Cache key string
        """
        # Normalize email
        normalized_email = email.lower().strip()
        
        # Create base key
        key_parts = [f"validation:{normalized_email}"]
        
        # Add options hash if present
        if options:
            options_str = str(sorted(options.items()))
            options_hash = hashlib.md5(options_str.encode()).hexdigest()[:8]
            key_parts.append(f"opts:{options_hash}")
            
        return ":".join(key_parts)
        
    @staticmethod
    def build_domain_key(domain: str) -> str:
        """
        Build cache key for domain information.
        
        Args:
            domain: Domain name
            
        Returns:
            Cache key string
        """
        return f"domain:{domain.lower()}"