import logging
import re
from typing import Dict
from email.utils import parseaddr

class FormatValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.strict_regex = re.compile(r"""
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
        Performs comprehensive format validation.
        
        Args:
            email: Email to validate
            
        Returns:
            Dict containing format validation results
        """
        try:
            email = email.strip()
            results = {
                "is_valid": False,
                "issues": [],
                "normalized": None
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
                
            local_part, domain = addr.split('@')
            
            # Length checks
            if len(email) > 254:
                results["issues"].append("Email too long (max 254 chars)")
            if len(local_part) > 64:
                results["issues"].append("Local part too long (max 64 chars)")
                
            # Local part checks
            if local_part.startswith('.'):
                results["issues"].append("Local part cannot start with dot")
            if local_part.endswith('.'):
                results["issues"].append("Local part cannot end with dot")
            if '..' in local_part:
                results["issues"].append("Local part cannot contain consecutive dots")
                
            # Domain checks
            if domain.startswith('-'):
                results["issues"].append("Domain cannot start with hyphen")
            if domain.endswith('-'):
                results["issues"].append("Domain cannot end with hyphen")
            if '..' in domain:
                results["issues"].append("Domain cannot contain consecutive dots")
                
            # Strict regex check
            if not self.strict_regex.match(addr):
                results["issues"].append("Failed strict format validation")
                
            # Set final results
            results["is_valid"] = len(results["issues"]) == 0
            if results["is_valid"]:
                results["normalized"] = addr.lower()
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error validating format for {email}: {str(e)}")
            return {
                "is_valid": False,
                "issues": ["Error during validation"],
                "normalized": None
            }