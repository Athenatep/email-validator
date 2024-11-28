import logging
from typing import List, Set, Dict, Tuple
from Levenshtein import distance

class Deduplicator:
    """Removes duplicate and similar email addresses"""
    
    def __init__(self, similarity_threshold: int = 2):
        self.logger = logging.getLogger(__name__)
        self.similarity_threshold = similarity_threshold
        
    def deduplicate(self, emails: List[str]) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Remove duplicates and group similar emails.
        
        Args:
            emails: List of email addresses
            
        Returns:
            Tuple of (unique_emails, similar_groups)
        """
        try:
            unique_emails: Set[str] = set()
            similar_groups: Dict[str, List[str]] = {}
            
            for email in emails:
                if email in unique_emails:
                    continue
                    
                # Check for similar emails
                similar = self._find_similar(email, unique_emails)
                if similar:
                    primary = min(similar, key=len)  # Use shortest as primary
                    if primary not in similar_groups:
                        similar_groups[primary] = []
                    similar_groups[primary].append(email)
                else:
                    unique_emails.add(email)
                    
            return list(unique_emails), similar_groups
            
        except Exception as e:
            self.logger.error(f"Error deduplicating emails: {str(e)}")
            return [], {}
            
    def _find_similar(self, email: str, existing: Set[str]) -> Set[str]:
        """Find similar emails in existing set."""
        try:
            similar = set()
            local_part, domain = email.split('@')
            
            for existing_email in existing:
                existing_local, existing_domain = existing_email.split('@')
                
                # Only compare emails with same domain
                if domain == existing_domain:
                    if distance(local_part, existing_local) <= self.similarity_threshold:
                        similar.add(existing_email)
                        
            return similar
            
        except Exception as e:
            self.logger.error(f"Error finding similar emails: {str(e)}")
            return set()