import dns.resolver
import logging
from typing import Dict

class DomainValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def validate_domain(self, domain: str) -> Dict[str, bool]:
        """
        Validates a domain by checking MX records.
        
        Args:
            domain: The domain to validate
            
        Returns:
            Dict containing validation results
        """
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return {
                "has_mx": bool(mx_records),
                "is_valid": bool(mx_records)
            }
        except Exception as e:
            self.logger.error(f"Error validating domain {domain}: {str(e)}")
            return {"has_mx": False, "is_valid": False}