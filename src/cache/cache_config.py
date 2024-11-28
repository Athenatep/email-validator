from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CacheConfig:
    """Configuration for cache behavior"""
    enabled: bool = True
    default_ttl: int = 3600  # 1 hour
    max_size: int = 10000
    cleanup_interval: int = 300  # 5 minutes
    
    validation_ttls: Dict[str, int] = None
    
    def __post_init__(self):
        if self.validation_ttls is None:
            self.validation_ttls = {
                "domain": 86400,     # 24 hours for domain info
                "mx": 43200,         # 12 hours for MX records
                "reputation": 3600,   # 1 hour for reputation
                "disposable": 86400,  # 24 hours for disposable check
                "validation": 1800    # 30 minutes for full validation
            }