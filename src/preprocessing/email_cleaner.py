import logging
from typing import List, Set
import re

class EmailCleaner:
    """Cleans and normalizes email addresses"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.whitespace_pattern = re.compile(r'\s+')
        self.invalid_chars_pattern = re.compile(r'[^\w\d.@+-]')
        
    def clean_email(self, email: str) -> str:
        """
        Clean and normalize a single email address.
        
        Args:
            email: Raw email address
            
        Returns:
            Cleaned email address
        """
        try:
            if not email:
                return ""
                
            # Convert to lowercase and strip whitespace
            cleaned = email.lower().strip()
            
            # Remove any whitespace within the email
            cleaned = self.whitespace_pattern.sub('', cleaned)
            
            # Remove invalid characters
            cleaned = self.invalid_chars_pattern.sub('', cleaned)
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error cleaning email {email}: {str(e)}")
            return ""
            
    def clean_list(self, emails: List[str]) -> List[str]:
        """
        Clean a list of email addresses.
        
        Args:
            emails: List of raw email addresses
            
        Returns:
            List of cleaned email addresses
        """
        try:
            cleaned = []
            for email in emails:
                if clean_email := self.clean_email(email):
                    cleaned.append(clean_email)
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error cleaning email list: {str(e)}")
            return []