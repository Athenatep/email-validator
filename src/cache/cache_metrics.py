import logging
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class CacheMetrics:
    """Tracks cache performance metrics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_entries: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    
    def record_hit(self):
        """Record cache hit."""
        self.hits += 1
        
    def record_miss(self):
        """Record cache miss."""
        self.misses += 1
        
    def record_eviction(self):
        """Record cache eviction."""
        self.evictions += 1
        
    def update_total_entries(self, count: int):
        """Update total entries count."""
        self.total_entries = count
        
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
        
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "total_entries": self.total_entries,
            "hit_rate": self.get_hit_rate(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }