import logging
from typing import Dict, List, Set, Tuple
from Levenshtein import distance
from collections import defaultdict

class BatchDeduplicator:
    """Handles efficient deduplication of large email lists"""
    
    def __init__(self, similarity_threshold: int = 2):
        self.logger = logging.getLogger(__name__)
        self.similarity_threshold = similarity_threshold
        
    def deduplicate(self, emails: List[str]) -> Dict[str, any]:
        """
        Deduplicate a list of emails, detecting exact and similar duplicates.
        
        Args:
            emails: List of email addresses
            
        Returns:
            Dict containing:
                - unique_emails: List of unique emails
                - duplicates: Dict mapping emails to their duplicates
                - similar_groups: Dict of similar email groups
                - stats: Deduplication statistics
        """
        try:
            results = {
                "unique_emails": [],
                "duplicates": defaultdict(list),
                "similar_groups": defaultdict(list),
                "stats": {
                    "total": len(emails),
                    "unique": 0,
                    "exact_duplicates": 0,
                    "similar": 0
                }
            }
            
            # First pass: Exact duplicates
            email_set: Set[str] = set()
            for email in emails:
                normalized = email.lower().strip()
                if normalized in email_set:
                    results["duplicates"][normalized].append(email)
                    results["stats"]["exact_duplicates"] += 1
                else:
                    email_set.add(normalized)
                    results["unique_emails"].append(email)
                    
            # Second pass: Similar emails
            domain_groups = self._group_by_domain(results["unique_emails"])
            
            for domain, domain_emails in domain_groups.items():
                similar_groups = self._find_similar_groups(domain_emails)
                for primary, similar in similar_groups.items():
                    if similar:
                        results["similar_groups"][primary].extend(similar)
                        results["stats"]["similar"] += len(similar)
                        
            # Update statistics
            results["stats"]["unique"] = len(results["unique_emails"])
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error deduplicating emails: {str(e)}")
            return {
                "unique_emails": emails,
                "duplicates": {},
                "similar_groups": {},
                "stats": {
                    "total": len(emails),
                    "unique": len(emails),
                    "exact_duplicates": 0,
                    "similar": 0,
                    "error": str(e)
                }
            }
            
    def _group_by_domain(self, emails: List[str]) -> Dict[str, List[str]]:
        """Group emails by domain for efficient similarity checking."""
        domain_groups = defaultdict(list)
        for email in emails:
            try:
                _, domain = email.lower().split('@')
                domain_groups[domain].append(email)
            except ValueError:
                continue
        return domain_groups
        
    def _find_similar_groups(self, emails: List[str]) -> Dict[str, List[str]]:
        """Find groups of similar emails within the same domain."""
        similar_groups = {}
        processed = set()
        
        for email in emails:
            if email in processed:
                continue
                
            similar = []
            local_part1 = email.split('@')[0].lower()
            
            for other in emails:
                if other != email and other not in processed:
                    local_part2 = other.split('@')[0].lower()
                    if distance(local_part1, local_part2) <= self.similarity_threshold:
                        similar.append(other)
                        processed.add(other)
                        
            if similar:
                similar_groups[email] = similar
                processed.add(email)
                
        return similar_groups