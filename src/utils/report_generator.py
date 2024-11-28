import logging
from typing import Dict, List
import json
import csv
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_report(self, results: List[Dict], stats: Dict, output_format: str = "json") -> str:
        """
        Generate validation report in specified format.
        
        Args:
            results: List of validation results
            stats: Statistics summary
            output_format: Desired output format (json/csv)
            
        Returns:
            Path to generated report file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_format == "json":
                return self._generate_json_report(results, stats, timestamp)
            elif output_format == "csv":
                return self._generate_csv_report(results, timestamp)
            else:
                raise ValueError(f"Unsupported format: {output_format}")
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return ""
            
    def _generate_json_report(self, results: List[Dict], stats: Dict, timestamp: str) -> str:
        """Generate JSON report."""
        try:
            report_data = {
                "timestamp": timestamp,
                "summary": stats,
                "results": results
            }
            
            filename = f"reports/validation_report_{timestamp}.json"
            with open(filename, "w") as f:
                json.dump(report_data, f, indent=2)
                
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generating JSON report: {str(e)}")
            return ""
            
    def _generate_csv_report(self, results: List[Dict], timestamp: str) -> str:
        """Generate CSV report."""
        try:
            filename = f"reports/validation_report_{timestamp}.csv"
            
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Email", "Valid", "Issues", "Spam Trap", "Disposable",
                    "Catchall", "Role Address", "Suggestions"
                ])
                
                # Write results
                for result in results:
                    writer.writerow([
                        result["email"],
                        result.get("valid", False),
                        "|".join(result.get("issues", [])),
                        result.get("checks", {}).get("spam_trap", {}).get("is_spam_trap", False),
                        result.get("checks", {}).get("disposable", {}).get("is_disposable", False),
                        result.get("checks", {}).get("catchall", {}).get("is_catchall", False),
                        result.get("checks", {}).get("role", {}).get("is_role_address", False),
                        "|".join(result.get("suggestions", []))
                    ])
                    
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generating CSV report: {str(e)}")
            return ""