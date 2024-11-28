import dns.resolver
import logging
from typing import Dict
import whois
from datetime import datetime

class DomainValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def validate(self, domain: str) -> Dict[str, any]:
        """
        Validates a domain by checking DNS records and registration.
        
        Args:
            domain: The domain to validate
            
        Returns:
            Dict containing validation results
        """
        try:
            results = {
                "is_valid": False,
                "has_mx": False,
                "domain_age": None,
                "issues": []
            }

            # Check MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                results["has_mx"] = bool(mx_records)
                if not results["has_mx"]:
                    results["issues"].append("No MX records found")
            except Exception as e:
                results["issues"].append(f"MX record lookup failed: {str(e)}")

            # Check domain registration
            try:
                domain_info = whois.whois(domain)
                if domain_info.creation_date:
                    if isinstance(domain_info.creation_date, list):
                        creation_date = domain_info.creation_date[0]
                    else:
                        creation_date = domain_info.creation_date
                    
                    domain_age = (datetime.now() - creation_date).days
                    results["domain_age"] = domain_age
                    
                    if domain_age < 30:
                        results["issues"].append("Domain is less than 30 days old")
            except Exception as e:
                results["issues"].append(f"Domain registration lookup failed: {str(e)}")

            results["is_valid"] = len(results["issues"]) == 0
            return results

        except Exception as e:
            self.logger.error(f"Error validating domain {domain}: {str(e)}")
            return {
                "is_valid": False,
                "has_mx": False,
                "domain_age": None,
                "issues": [f"Validation error: {str(e)}"]
            }