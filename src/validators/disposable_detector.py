import logging
from typing import Dict, Set
import aiohttp
import json

class DisposableDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.disposable_domains: Set[str] = set()
        self._load_disposable_domains()
        
    def _load_disposable_domains(self):
        """Load known disposable email domains."""
        try:
            with open('data/disposable_domains.json', 'r') as f:
                self.disposable_domains = set(json.load(f))
        except FileNotFoundError:
            self.logger.warning("Disposable domains file not found, using empty set")
            
    async def is_disposable(self, email: str) -> Dict[str, bool]:
        """
        Check if email is from a disposable domain.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing disposable email check results
        """
        try:
            domain = email.split('@')[1].lower()
            
            # Check against known disposable domains
            is_disposable = domain in self.disposable_domains
            
            # Additional check using external API
            if not is_disposable:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://open.kickbox.com/v1/disposable/{domain}') as response:
                        if response.status == 200:
                            result = await response.json()
                            is_disposable = result.get('disposable', False)
                            
            return {
                "is_disposable": is_disposable,
                "domain": domain,
                "reason": "Disposable email service detected" if is_disposable else None
            }
            
        except Exception as e:
            self.logger.error(f"Error checking disposable email {email}: {str(e)}")
            return {"is_disposable": False, "domain": None, "reason": "Error during check"}