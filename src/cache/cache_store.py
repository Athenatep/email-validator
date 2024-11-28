import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from threading import Lock
from .cache_config import CacheConfig
from .cache_metrics import CacheMetrics

class CacheStore:
    """Thread-safe in-memory cache with TTL support and metrics"""
    
    def __init__(self, config: CacheConfig):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.metrics = CacheMetrics()
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        try:
            with self._lock:
                if key in self._store:
                    entry = self._store[key]
                    if datetime.now() < entry['expires']:
                        self.metrics.record_hit()
                        return entry['value']
                    else:
                        del self._store[key]
                        self.metrics.record_eviction()
                
                self.metrics.record_miss()
                return None
                
        except Exception as e:
            self.logger.error(f"Error retrieving from cache: {str(e)}")
            return None
            
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        category: Optional[str] = None
    ) -> bool:
        """Set value in cache with expiration."""
        try:
            if not self.config.enabled:
                return False
                
            with self._lock:
                # Check cache size limit
                if len(self._store) >= self.config.max_size:
                    await self._evict_entries()
                    
                # Get TTL based on category or default
                if category and category in self.config.validation_ttls:
                    ttl = self.config.validation_ttls[category]
                ttl = ttl or self.config.default_ttl
                
                expiration = datetime.now() + timedelta(seconds=ttl)
                self._store[key] = {
                    'value': value,
                    'expires': expiration,
                    'category': category
                }
                
                self.metrics.update_total_entries(len(self._store))
                return True
                
        except Exception as e:
            self.logger.error(f"Error setting cache: {str(e)}")
            return False
            
    async def _evict_entries(self) -> int:
        """Evict expired and excess entries."""
        try:
            now = datetime.now()
            evicted = 0
            
            # First, remove expired entries
            expired_keys = [
                key for key, entry in self._store.items()
                if entry['expires'] < now
            ]
            
            for key in expired_keys:
                del self._store[key]
                evicted += 1
                
            # If still over limit, remove oldest entries
            if len(self._store) >= self.config.max_size:
                sorted_entries = sorted(
                    self._store.items(),
                    key=lambda x: x[1]['expires']
                )
                
                to_remove = len(self._store) - self.config.max_size + 100
                for key, _ in sorted_entries[:to_remove]:
                    del self._store[key]
                    evicted += 1
                    
            self.metrics.record_eviction()
            return evicted
            
        except Exception as e:
            self.logger.error(f"Error evicting entries: {str(e)}")
            return 0
            
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics and metrics."""
        try:
            with self._lock:
                stats = self.metrics.get_stats()
                stats.update({
                    'size': len(self._store),
                    'max_size': self.config.max_size,
                    'enabled': self.config.enabled
                })
                return stats
                
        except Exception as e:
            self.logger.error(f"Error getting cache stats: {str(e)}")
            return {}