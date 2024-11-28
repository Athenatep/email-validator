import re
from typing import Dict
from tld import get_tld
import logging

class SpamTrapDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.patterns = [
            r'^abuse@',
            r'^postmaster@',
            r'^spam@',
            r'^noreply@',
            r'^no-reply@',
            r'^admin@'
        ]
        
    def check_spam_trap(self, email: str) -> Dict[str, bool]:
        """
        Detects potential spam trap emails.
        
        Args:
            email: Email address to check
            
        Returns:
            Dict containing spam trap detection results
        """
        try:
            email = email.lower()
            
            # Check common spam trap patterns
            for pattern in self.patterns:
                if re.match(pattern, email):
                    return {
                        "is_spam_trap": True,
                        "reason": "Common spam trap pattern detected"
                    }
            
            # Check for role-based emails
            local_part = email.split('@')[0]
            if local_part in ['info', 'sales', 'support', 'contact']:
                return {
                    "is_spam_trap": True,
                    "reason": "Role-based email detected"
                }
                
            return {"is_spam_trap": False, "reason": None}
            
        except Exception as e:
            self.logger.error(f"Error checking spam trap for {email}: {str(e)}")
            return {"is_spam_trap": False, "reason": "Error during check"}