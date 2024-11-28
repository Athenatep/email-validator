import logging
from typing import Dict, List
import pandas as pd
from pathlib import Path
from .charts.validation_summary import ValidationSummaryChart
from .charts.score_distribution import ScoreDistributionChart
from .charts.issue_breakdown import IssueBreakdownChart
from .charts.domain_distribution import DomainDistributionChart
from .charts.validation_timeline import ValidationTimelineChart

class ChartManager:
    """Manages the generation of all visualization charts"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path("reports/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize chart generators
        self.validation_summary = ValidationSummaryChart(self.output_dir)
        self.score_distribution = ScoreDistributionChart(self.output_dir)
        self.issue_breakdown = IssueBreakdownChart(self.output_dir)
        self.domain_distribution = DomainDistributionChart(self.output_dir)
        self.validation_timeline = ValidationTimelineChart(self.output_dir)
        
    def generate_charts(self, results: List[Dict]) -> Dict[str, str]:
        """
        Generate all visualization charts.
        
        Args:
            results: List of validation results
            
        Returns:
            Dict mapping chart types to file paths
        """
        try:
            df = pd.DataFrame(results)
            
            return {
                "validation_summary": self.validation_summary.generate(df),
                "score_distribution": self.score_distribution.generate(df),
                "issue_breakdown": self.issue_breakdown.generate(df),
                "domain_distribution": self.domain_distribution.generate(df),
                "validation_timeline": self.validation_timeline.generate(df)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating charts: {str(e)}")
            return {}