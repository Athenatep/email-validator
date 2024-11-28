import logging
from typing import Dict
import aiohttp
import dns.resolver
from datetime import datetime

class ReputationValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.blacklists = [
            "zen.spamhaus.org",
            "bl.spamcop.net",
            "dnsbl.sorbs.net"
        ]

    async def check_reputation(self, email: str) -> Dict[str, any]:
        """
        Check email and domain reputation using multiple sources.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing reputation check results
        """
        try:
            domain = email.split('@')[1]
            results = {
                "reputation_score": 100,  # Start with perfect score
                "blacklisted": False,
                "blacklist_matches": [],
                "domain_age_days": None,
                "issues": []
            }

            # Check domain age
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://whois.whoisxmlapi.com/api/v1?domain={domain}"
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if creation_date := data.get("creationDate"):
                                creation_date = datetime.fromisoformat(creation_date)
                                age_days = (datetime.now() - creation_date).days
                                results["domain_age_days"] = age_days
                                
                                if age_days < 30:
                                    results["reputation_score"] -= 20
                                    results["issues"].append("Domain is very new")
            except Exception as e:
                results["issues"].append(f"Domain age check failed: {str(e)}")

            # Check blacklists
            for blacklist in self.blacklists:
                try:
                    query = f"{domain}.{blacklist}"
                    await dns.resolver.resolve(query, "A")
                    results["blacklisted"] = True
                    results["blacklist_matches"].append(blacklist)
                    results["reputation_score"] -= 30
                except dns.resolver.NXDOMAIN:
                    continue
                except Exception as e:
                    results["issues"].append(f"Blacklist check failed for {blacklist}")

            # Additional reputation factors
            if '@' in email.split('@')[0]:
                results["reputation_score"] -= 10
                results["issues"].append("Local part contains @ symbol")

            if len(email) > 100:
                results["reputation_score"] -= 5
                results["issues"].append("Unusually long email address")

            # Ensure score stays within bounds
            results["reputation_score"] = max(0, min(100, results["reputation_score"]))

            return results

        except Exception as e:
            self.logger.error(f"Error checking reputation: {str(e)}")
            return {
                "reputation_score": 0,
                "blacklisted": False,
                "blacklist_matches": [],
                "domain_age_days": None,
                "issues": [f"Reputation check failed: {str(e)}"]
            }