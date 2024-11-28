import logging
from typing import Dict, List
from collections import defaultdict
import json
from datetime import datetime

class StatsCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stats = defaultdict(int)
        self.domain_stats = defaultdict(lambda: defaultdict(int))
        
    def collect_result(self, result: Dict):
        """
        Collect statistics from validation result.
        
        Args:
            result: Validation result to collect stats from
        """
        try:
            # Increment total checks
            self.stats["total_checks"] += 1
            
            # Track validation status
            self.stats["valid_emails" if result.get("valid") else "invalid_emails"] += 1
            
            # Track specific issues
            if "checks" in result:
                checks = result["checks"]
                
                if checks.get("spam_trap", {}).get("is_spam_trap"):
                    self.stats["spam_traps"] += 1
                    
                if checks.get("disposable", {}).get("is_disposable"):
                    self.stats["disposable"] += 1
                    
                if checks.get("catchall", {}).get("is_catchall"):
                    self.stats["catchall"] += 1
                    
            # Collect domain statistics
            if "@" in result["email"]:
                domain = result["email"].split("@")[1]
                self.domain_stats[domain]["total"] += 1
                self.domain_stats[domain]["valid" if result.get("valid") else "invalid"] += 1
                
        except Exception as e:
            self.logger.error(f"Error collecting stats: {str(e)}")
            
    def get_summary(self) -> Dict:
        """Get statistical summary of validation results."""
        try:
            return {
                "total_processed": self.stats["total_checks"],
                "valid_ratio": self.stats["valid_emails"] / max(self.stats["total_checks"], 1),
                "issues_found": {
                    "spam_traps": self.stats["spam_traps"],
                    "disposable": self.stats["disposable"],
                    "catchall": self.stats["catchall"]
                },
                "top_domains": sorted(
                    self.domain_stats.items(),
                    key=lambda x: x[1]["total"],
                    reverse=True
                )[:10]
            }
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return {}