import logging
from typing import Dict, List
import re

class TypoDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.common_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'aol.com', 'icloud.com', 'protonmail.com'
        }
        self.common_typos = {
            'gmail.com': ['gmai.com', 'gmial.com', 'gmal.com', 'gmale.com'],
            'yahoo.com': ['yaho.com', 'yahooo.com', 'yahou.com'],
            'hotmail.com': ['hotmai.com', 'hotmal.com', 'hotmial.com'],
            'outlook.com': ['outlok.com', 'outlool.com', 'outlock.com']
        }
        
    def check_typos(self, email: str) -> Dict[str, any]:
        """
        Check for common email typos and suggest corrections.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing typo detection results
        """
        try:
            local_part, domain = email.lower().split('@')
            suggestions = []
            
            # Check for common domain typos
            for correct_domain, typos in self.common_typos.items():
                if domain in typos:
                    suggestions.append(f"{local_part}@{correct_domain}")
                    
            # Check for common local part typos
            if domain in self.common_domains:
                # Double letters
                fixed_doubles = re.sub(r'(.)\1+', r'\1\1', local_part)
                if fixed_doubles != local_part:
                    suggestions.append(f"{fixed_doubles}@{domain}")
                    
                # Missing dots in gmail
                if domain == 'gmail.com' and '.' in local_part:
                    no_dots = local_part.replace('.', '')
                    suggestions.append(f"{no_dots}@{domain}")
                    
            return {
                "has_typos": bool(suggestions),
                "original": email,
                "suggestions": suggestions,
                "reason": "Potential typos detected" if suggestions else None
            }
            
        except Exception as e:
            self.logger.error(f"Error checking typos for {email}: {str(e)}")
            return {
                "has_typos": False,
                "original": email,
                "suggestions": [],
                "reason": "Error during check"
            }