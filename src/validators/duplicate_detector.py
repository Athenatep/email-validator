from typing import Dict, List, Set
import logging
from Levenshtein import distance

class DuplicateDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.seen_emails: Set[str] = set()
        self.similar_threshold = 2  # Levenshtein distance threshold
        
    def check_duplicate(self, email: str) -> Dict[str, bool]:
        """
        Detects exact and similar duplicate emails.
        
        Args:
            email: Email to check for duplicates
            
        Returns:
            Dict containing duplicate detection results
        """
        try:
            email = email.lower().strip()
            
            # Check for exact duplicates
            if email in self.seen_emails:
                return {
                    "is_duplicate": True,
                    "type": "exact",
                    "reason": "Exact duplicate found"
                }
                
            # Check for similar emails (typos, etc.)
            for seen_email in self.seen_emails:
                if self._is_similar(email, seen_email):
                    return {
                        "is_duplicate": True,
                        "type": "similar",
                        "reason": f"Similar to existing email: {seen_email}"
                    }
                    
            # Add email to seen set
            self.seen_emails.add(email)
            return {"is_duplicate": False, "type": None, "reason": None}
            
        except Exception as e:
            self.logger.error(f"Error checking duplicates for {email}: {str(e)}")
            return {"is_duplicate": False, "type": None, "reason": "Error during check"}
            
    def _is_similar(self, email1: str, email2: str) -> bool:
        """Check if two emails are similar based on Levenshtein distance."""
        if email1 == email2:
            return True
            
        # Split emails into local and domain parts
        local1, domain1 = email1.split('@')
        local2, domain2 = email2.split('@')
        
        # If domains are different, not similar
        if domain1 != domain2:
            return False
            
        # Check similarity of local parts
        return distance(local1, local2) <= self.similar_threshold