import logging
from typing import Dict, Set

class RoleValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.role_addresses: Set[str] = {
            "admin", "administrator", "webmaster", "hostmaster", "postmaster",
            "root", "abuse", "noc", "security", "support", "info", "marketing",
            "sales", "contact", "help", "enquiries", "careers", "job", "jobs",
            "newsletter", "noreply", "no-reply", "notifications", "team"
        }
        
    def check_role_address(self, email: str) -> Dict:
        """
        Check if email is a role-based address.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing role address check results
        """
        try:
            local_part = email.split('@')[0].lower()
            
            # Check exact matches
            is_role = local_part in self.role_addresses
            
            # Check prefixes/suffixes
            if not is_role:
                for role in self.role_addresses:
                    if local_part.startswith(role) or local_part.endswith(role):
                        is_role = True
                        break
                        
            return {
                "is_role_address": is_role,
                "role_type": local_part if is_role else None,
                "risk_level": "high" if is_role else "low"
            }
            
        except Exception as e:
            self.logger.error(f"Error checking role address: {str(e)}")
            return {
                "is_role_address": False,
                "role_type": None,
                "risk_level": "unknown"
            }