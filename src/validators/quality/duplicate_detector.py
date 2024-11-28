import logging
from typing import Dict, Set
from Levenshtein import distance

class DuplicateDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.seen_emails: Set[str] = set()
        self.similar_threshold = 2

    def check(self, email: str) -> Dict[str, any]:
        """
        Detects exact and similar duplicate emails.
        
        Args:
            email: Email to check
            
        Returns:
            Dict containing duplicate detection results
        """
        try:
            email = email.lower().strip()
            results = {
                "is_duplicate": False,
                "duplicate_type": None,
                "similar_to": None,
                "similarity_score": 0,
                "issues": []
            }

            # Check for exact duplicates
            if email in self.seen_emails:
                results.update({
                    "is_duplicate": True,
                    "duplicate_type": "exact",
                    "issues": ["Exact duplicate found"]
                })
                return results

            # Check for similar emails
            local_part, domain = email.split('@')
            for seen_email in self.seen_emails:
                seen_local, seen_domain = seen_email.split('@')
                
                if domain == seen_domain:
                    similarity = distance(local_part, seen_local)
                    if similarity <= self.similar_threshold:
                        results.update({
                            "is_duplicate": True,
                            "duplicate_type": "similar",
                            "similar_to": seen_email,
                            "similarity_score": similarity,
                            "issues": [f"Similar to existing email: {seen_email}"]
                        })
                        return results

            # Add to seen set if not duplicate
            self.seen_emails.add(email)
            return results

        except Exception as e:
            self.logger.error(f"Error checking duplicates for {email}: {str(e)}")
            return {
                "is_duplicate": False,
                "duplicate_type": None,
                "similar_to": None,
                "similarity_score": 0,
                "issues": [f"Duplicate check failed: {str(e)}"]
            }