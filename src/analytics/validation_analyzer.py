import logging
from typing import Dict, List
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class ValidationAnalyzer:
    """Analyzes and generates insights from validation results."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results_history: List[Dict] = []
        
    def add_result(self, result: Dict):
        """Add a validation result to the analysis history."""
        try:
            result_with_timestamp = {
                **result,
                "timestamp": datetime.now().isoformat()
            }
            self.results_history.append(result_with_timestamp)
        except Exception as e:
            self.logger.error(f"Error adding result to analysis: {str(e)}")
            
    def get_summary_stats(self) -> Dict:
        """Get summary statistics of validation results."""
        try:
            total = len(self.results_history)
            if not total:
                return {"message": "No validation data available"}
                
            valid_count = sum(1 for r in self.results_history if r.get("is_valid"))
            
            return {
                "total_validations": total,
                "valid_emails": valid_count,
                "invalid_emails": total - valid_count,
                "validity_rate": valid_count / total if total else 0,
                "average_score": sum(r.get("score", 0) for r in self.results_history) / total,
                "common_issues": self._get_common_issues()
            }
        except Exception as e:
            self.logger.error(f"Error generating summary stats: {str(e)}")
            return {"error": str(e)}
            
    def _get_common_issues(self) -> Dict[str, int]:
        """Get frequency count of validation issues."""
        try:
            issue_counts = {}
            for result in self.results_history:
                for issue in result.get("issues", []):
                    issue_counts[issue] = issue_counts.get(issue, 0) + 1
            return dict(sorted(
                issue_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10])
        except Exception as e:
            self.logger.error(f"Error analyzing common issues: {str(e)}")
            return {}