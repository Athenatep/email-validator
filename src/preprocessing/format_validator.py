import logging
from typing import List, Dict
import re
from email.utils import parseaddr

class FormatValidator:
    """Validates email format and structure"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_pattern = re.compile(r"""
            ^(?!\.)                    # No dot at start
            [a-zA-Z0-9._%+-]+         # Local part
            @                          # @ symbol
            (?![-.])                   # No dot or hyphen after @
            [a-zA-Z0-9.-]+            # Domain name
            \.                         # Dot before TLD
            [a-zA-Z]{2,}$             # TLD
        """, re.VERBOSE)
        
    def validate_format(self, email: str) -> Dict[str, any]:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            Dict containing validation results
        """
        try:
            results = {
                "is_valid": False,
                "issues": []
            }
            
            # Basic format check
            if not '@' in email:
                results["issues"].append("Missing @ symbol")
                return results
                
            # Parse email address
            name, addr = parseaddr(email)
            if not addr:
                results["issues"].append("Invalid email format")
                return results
                
            # Length checks
            if len(email) > 254:
                results["issues"].append("Email too long (max 254 chars)")
            
            local_part, domain = addr.split('@')
            if len(local_part) > 64:
                results["issues"].append("Local part too long (max 64 chars)")
                
            # Pattern check
            if not self.email_pattern.match(addr):
                results["issues"].append("Failed format validation")
                
            results["is_valid"] = len(results["issues"]) == 0
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating format: {str(e)}")
            return {"is_valid": False, "issues": ["Validation error"]}