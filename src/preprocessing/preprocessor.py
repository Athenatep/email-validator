import logging
from typing import List, Dict, Any
from .email_cleaner import EmailCleaner
from .batch_deduplicator import BatchDeduplicator
from .format_validator import FormatValidator

class EmailPreprocessor:
    """Coordinates email preprocessing tasks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cleaner = EmailCleaner()
        self.deduplicator = BatchDeduplicator()
        self.format_validator = FormatValidator()
        
    async def preprocess(self, emails: List[str]) -> Dict[str, Any]:
        """
        Preprocess a list of email addresses.
        
        Args:
            emails: List of raw email addresses
            
        Returns:
            Dict containing preprocessing results
        """
        try:
            results = {
                "original_count": len(emails),
                "processed_count": 0,
                "invalid_format": [],
                "duplicates": {},
                "similar_groups": {},
                "processed_emails": [],
                "stats": {}
            }
            
            # Clean emails
            cleaned_emails = self.cleaner.clean_list(emails)
            
            # Validate format
            valid_emails = []
            for email in cleaned_emails:
                validation = self.format_validator.validate_format(email)
                if validation["is_valid"]:
                    valid_emails.append(email)
                else:
                    results["invalid_format"].append({
                        "email": email,
                        "issues": validation["issues"]
                    })
            
            # Deduplicate emails
            dedup_results = self.deduplicator.deduplicate(valid_emails)
            results["processed_emails"] = dedup_results["unique_emails"]
            results["duplicates"] = dedup_results["duplicates"]
            results["similar_groups"] = dedup_results["similar_groups"]
            
            # Calculate statistics
            results["processed_count"] = len(results["processed_emails"])
            results["stats"] = {
                "total_cleaned": len(cleaned_emails),
                "total_valid": len(valid_emails),
                "total_unique": len(results["processed_emails"]),
                "exact_duplicates": dedup_results["stats"]["exact_duplicates"],
                "similar_emails": dedup_results["stats"]["similar"],
                "invalid_count": len(results["invalid_format"])
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error preprocessing emails: {str(e)}")
            return {
                "original_count": len(emails),
                "processed_count": 0,
                "invalid_format": [],
                "duplicates": {},
                "similar_groups": {},
                "processed_emails": [],
                "stats": {},
                "error": str(e)
            }