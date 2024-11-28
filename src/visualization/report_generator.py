import logging
from typing import Dict, List
import pandas as pd
from pathlib import Path
from datetime import datetime
from .chart_manager import ChartManager

class ReportGenerator:
    """Generates comprehensive validation reports with visualizations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chart_manager = ChartManager()
        self.output_dir = Path("reports")
        self.output_dir.mkdir(exist_ok=True)
        
    async def generate_report(
        self,
        results: List[Dict],
        format: str = "html"
    ) -> str:
        """
        Generate a comprehensive validation report.
        
        Args:
            results: List of validation results
            format: Output format (html/pdf)
            
        Returns:
            Path to generated report
        """
        try:
            # Generate charts
            chart_paths = self.chart_manager.generate_charts(results)
            
            # Create report based on format
            if format == "html":
                return self._generate_html_report(results, chart_paths)
            elif format == "pdf":
                return self._generate_pdf_report(results, chart_paths)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return ""
            
    def _generate_html_report(
        self,
        results: List[Dict],
        chart_paths: Dict[str, str]
    ) -> str:
        """Generate HTML report with embedded charts."""
        try:
            df = pd.DataFrame(results)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Calculate summary statistics
            stats = {
                "total_emails": len(df),
                "valid_emails": df['is_valid'].sum(),
                "average_score": df['score'].mean(),
                "common_issues": pd.Series(
                    [i for issues in df['issues'] for i in issues]
                ).value_counts().to_dict()
            }
            
            # Generate HTML content
            html_content = self._generate_html_content(stats, chart_paths, timestamp)
            
            # Save HTML report
            filepath = self.output_dir / f"validation_report_{timestamp}.html"
            with open(filepath, "w") as f:
                f.write(html_content)
                
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error generating HTML report: {str(e)}")
            return ""
            
    def _generate_html_content(
        self,
        stats: Dict,
        chart_paths: Dict[str, str],
        timestamp: str
    ) -> str:
        """Generate HTML content for the report."""
        return f"""
        <html>
        <head>
            <title>Email Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .section {{ margin-bottom: 30px; }}
                .chart {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; border: 1px solid #ddd; }}
                th {{ background-color: #f5f5f5; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Email Validation Report</h1>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <div class="section">
                    <h2>Summary Statistics</h2>
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Total Emails</td><td>{stats['total_emails']}</td></tr>
                        <tr><td>Valid Emails</td><td>{stats['valid_emails']}</td></tr>
                        <tr><td>Average Score</td><td>{stats['average_score']:.2f}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>Visualizations</h2>
                    {self._embed_charts(chart_paths)}
                </div>
                
                <div class="section">
                    <h2>Common Issues</h2>
                    <table>
                        <tr><th>Issue</th><th>Count</th></tr>
                        {''.join(f"<tr><td>{issue}</td><td>{count}</td></tr>"
                               for issue, count in stats['common_issues'].items())}
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
            
    def _embed_charts(self, chart_paths: Dict[str, str]) -> str:
        """Create HTML for embedding charts."""
        try:
            html_parts = []
            for chart_type, path in chart_paths.items():
                if path:
                    html_parts.append(f"""
                    <div class="chart">
                        <h3>{chart_type.replace('_', ' ').title()}</h3>
                        <img src="{path}" alt="{chart_type}" style="max-width: 100%;">
                    </div>
                    """)
            return "\n".join(html_parts)
            
        except Exception as e:
            self.logger.error(f"Error embedding charts: {str(e)}")
            return ""