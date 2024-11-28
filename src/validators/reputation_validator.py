import logging
from typing import Dict
import aiohttp

class ReputationValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def check_reputation(self, email: str, domain: str) -> Dict:
        """
        Check email and domain reputation using multiple sources.
        
        Args:
            email: Email to check
            domain: Domain to check
            
        Returns:
            Dict containing reputation check results
        """
        try:
            results = {
                "score": 0,
                "issues": [],
                "blacklisted": False,
                "sources": []
            }
            
            # Check domain age
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://whois.whoisxmlapi.com/api/v1?domain={domain}") as response:
                    if response.status == 200:
                        data = await response.json()
                        creation_date = data.get("creationDate")
                        if creation_date:
                            results["domain_age"] = creation_date
                            
            # Check blacklists
            blacklists = ["spamhaus.org", "spamcop.net", "sorbs.net"]
            for blacklist in blacklists:
                try:
                    import dns.resolver
                    query = f"{domain}.{blacklist}"
                    dns.resolver.resolve(query, "A")
                    results["blacklisted"] = True
                    results["issues"].append(f"Listed in {blacklist}")
                    results["sources"].append(blacklist)
                except dns.resolver.NXDOMAIN:
                    continue
                    
            return results
            
        except Exception as e:
            self.logger.error(f"Error checking reputation: {str(e)}")
            return {
                "score": 0,
                "issues": ["Error during reputation check"],
                "blacklisted": False,
                "sources": []
            }