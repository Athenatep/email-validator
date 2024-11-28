import logging
from typing import Dict, Any, Optional
from .cache_store import CacheStore
from .cache_key_builder import CacheKeyBuilder

class CacheManager:
    """Manages caching operations with key building and validation"""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.logger = logging.getLogger(__name__)
        self.store = CacheStore(default_ttl=ttl_seconds)
        self.key_builder = CacheKeyBuilder()
        
    async def get_validation_result(self, email: str, options: Optional[Dict] = None) -> Optional[Dict]:
        """
        Get cached validation result.
        
        Args:
            email: Email address
            options: Validation options
            
        Returns:
            Cached validation result or None
        """
        try:
            key = self.key_builder.build_validation_key(email, options)
            return await self.store.get(key)
        except Exception as e:
            self.logger.error(f"Error getting validation result: {str(e)}")
            return None
            
    async def cache_validation_result(
        self,
        email: str,
        result: Dict,
        options: Optional[Dict] = None,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache validation result.
        
        Args:
            email: Email address
            result: Validation result
            options: Validation options
            ttl: Optional TTL in seconds
            
        Returns:
            bool indicating success
        """
        try:
            key = self.key_builder.build_validation_key(email, options)
            return await self.store.set(key, result, ttl)
        except Exception as e:
            self.logger.error(f"Error caching validation result: {str(e)}")
            return False
            
    async def get_domain_info(self, domain: str) -> Optional[Dict]:
        """
        Get cached domain information.
        
        Args:
            domain: Domain name
            
        Returns:
            Cached domain info or None
        """
        try:
            key = self.key_builder.build_domain_key(domain)
            return await self.store.get(key)
        except Exception as e:
            self.logger.error(f"Error getting domain info: {str(e)}")
            return None
            
    async def cache_domain_info(
        self,
        domain: str,
        info: Dict,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache domain information.
        
        Args:
            domain: Domain name
            info: Domain information
            ttl: Optional TTL in seconds
            
        Returns:
            bool indicating success
        """
        try:
            key = self.key_builder.build_domain_key(domain)
            return await self.store.set(key, info, ttl)
        except Exception as e:
            self.logger.error(f"Error caching domain info: {str(e)}")
            return False
            
    async def clear_expired(self) -> int:
        """
        Clear expired cache entries.
        
        Returns:
            Number of entries cleared
        """
        return await self.store.clear_expired()
        
    async def get_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Dict containing cache stats
        """
        return await self.store.get_stats()