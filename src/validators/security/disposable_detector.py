import logging
from typing import Dict, Set
import aiohttp
import json
import os

class DisposableDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.disposable_domains: Set[str] = set()
        self._load_disposable_domains()

    def _load_disposable_domains(self):
        """Load known disposable email domains."""
        try:
            domains_file = os.path.join(
                os.path.dirname(__file__), 
                '../../data/disposable_domains.json'
            )
            with open(domains_file, 'r') as f:
                self.disposable_domains = set(json.load(f))
        except FileNotFoundError:
            self.logger.warning("Disposable domains file not found, using empty set")

    async def check(self, email: str) -> Dict[str, any]:
        """
        Check if email is from a disposable domain.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing disposable email check results
        """
        try:
            domain = email.split('@')[1].lower()
            results = {
                "is_disposable": False,
                "confidence": 0,
                "sources": [],
                "issues": []
            }

            # Check against known disposable domains
            if domain in self.disposable_domains:
                results["is_disposable"] = True
                results["confidence"] = 1.0
                results["sources"].append("local_database")
                return results

            # Check external API
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f'https://open.kickbox.com/v1/disposable/{domain}'
                    ) as response:
                        if response.status == 200:
                            api_result = await response.json()
                            if api_result.get('disposable'):
                                results["is_disposable"] = True
                                results["confidence"] = 0.8
                                results["sources"].append("kickbox_api")
            except Exception as e:
                results["issues"].append(f"API check failed: {str(e)}")

            return results

        except Exception as e:
            self.logger.error(f"Error checking disposable email {email}: {str(e)}")
            return {
                "is_disposable": False,
                "confidence": 0,
                "sources": [],
                "issues": [f"Check failed: {str(e)}"]
            }