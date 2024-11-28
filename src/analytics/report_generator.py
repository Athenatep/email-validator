import logging
from typing import Dict, List
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    """Generates detailed validation reports."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_report(
        self,
        results: List[Dict],
        stats: Dict,
        output_format: str = "json"
    ) -> str:
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
            # Create reports directory if it doesn't exist
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
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
            
    def _generate_json_report(
        self,
        results: List[Dict],
        stats: Dict,
        timestamp: str
    ) -> str:
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
            
            # Convert results to DataFrame for easier CSV handling
            df = pd.DataFrame(results)
            
            # Flatten nested dictionaries
            df["checks"] = df["checks"].apply(json.dumps)
            df["suggestions"] = df["suggestions"].apply(lambda x: "|".join(x))
            df["issues"] = df["issues"].apply(lambda x: "|".join(x))
            
            df.to_csv(filename, index=False)
            return filename
            
        except Exception as e:
            self.logger.error(f"Error generating CSV report: {str(e)}")
            return ""