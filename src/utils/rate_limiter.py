import asyncio
import logging
from typing import Dict
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, requests_per_second: int = 10):
        self.logger = logging.getLogger(__name__)
        self.requests_per_second = requests_per_second
        self.requests: Dict[str, list] = defaultdict(list)
        
    async def acquire(self, domain: str):
        """
        Rate limit requests to a specific domain.
        
        Args:
            domain: Domain to rate limit
        """
        try:
            now = datetime.now()
            self.cleanup_old_requests(domain, now)
            
            # Check if we're at the limit
            if len(self.requests[domain]) >= self.requests_per_second:
                # Calculate delay needed
                oldest_request = self.requests[domain][0]
                delay = 1.0 - (now - oldest_request).total_seconds()
                if delay > 0:
                    await asyncio.sleep(delay)
                    
            # Add current request
            self.requests[domain].append(now)
            
        except Exception as e:
            self.logger.error(f"Error in rate limiter for {domain}: {str(e)}")
            
    def cleanup_old_requests(self, domain: str, now: datetime):
        """Remove requests older than 1 second."""
        cutoff = now - timedelta(seconds=1)
        self.requests[domain] = [
            req for req in self.requests[domain]
            if req > cutoff
        ]