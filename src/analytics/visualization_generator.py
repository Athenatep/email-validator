import logging
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

class VisualizationGenerator:
    """Generates visualizations of validation results."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_visualizations(self, results: List[Dict]) -> Dict[str, str]:
        """
        Generate various visualizations of validation results.
        
        Args:
            results: List of validation results
            
        Returns:
            Dict mapping visualization names to file paths
        """
        try:
            # Create visualizations directory
            viz_dir = Path("reports/visualizations")
            viz_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert results to DataFrame
            df = pd.DataFrame(results)
            
            # Generate visualizations
            paths = {}
            
            # Validation scores distribution
            paths["score_dist"] = self._plot_score_distribution(df)
            
            # Issue types breakdown
            paths["issue_types"] = self._plot_issue_breakdown(df)
            
            # Validation results over time
            paths["time_series"] = self._plot_time_series(df)
            
            # Domain distribution
            paths["domains"] = self._plot_domain_distribution(df)
            
            return paths
            
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")
            return {}
            
    def _plot_score_distribution(self, df: pd.DataFrame) -> str:
        """Plot distribution of validation scores."""
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x="score", bins=20)
            plt.title("Distribution of Validation Scores")
            plt.xlabel("Score")
            plt.ylabel("Count")
            
            filepath = "reports/visualizations/score_distribution.png"
            plt.savefig(filepath)
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error plotting score distribution: {str(e)}")
            return ""
            
    def _plot_issue_breakdown(self, df: pd.DataFrame) -> str:
        """Plot breakdown of validation issues."""
        try:
            # Collect all issues
            all_issues = []
            for issues in df["issues"]:
                all_issues.extend(issues)
                
            issue_counts = pd.Series(all_issues).value_counts()
            
            plt.figure(figsize=(12, 6))
            issue_counts.plot(kind="bar")
            plt.title("Common Validation Issues")
            plt.xlabel("Issue Type")
            plt.ylabel("Frequency")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            
            filepath = "reports/visualizations/issue_breakdown.png"
            plt.savefig(filepath)
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error plotting issue breakdown: {str(e)}")
            return ""
            
    def _plot_time_series(self, df: pd.DataFrame) -> str:
        """Plot validation results over time."""
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            daily_stats = df.groupby(df["timestamp"].dt.date)["is_valid"].agg(["count", "mean"])
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Plot total validations
            daily_stats["count"].plot(ax=ax1)
            ax1.set_title("Daily Validation Volume")
            ax1.set_ylabel("Number of Validations")
            
            # Plot validity rate
            daily_stats["mean"].plot(ax=ax2)
            ax2.set_title("Daily Validity Rate")
            ax2.set_ylabel("Validity Rate")
            
            plt.tight_layout()
            
            filepath = "reports/visualizations/time_series.png"
            plt.savefig(filepath)
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error plotting time series: {str(e)}")
            return ""
            
    def _plot_domain_distribution(self, df: pd.DataFrame) -> str:
        """Plot distribution of email domains."""
        try:
            domains = df["email"].apply(lambda x: x.split("@")[1])
            domain_counts = domains.value_counts().head(10)
            
            plt.figure(figsize=(10, 6))
            domain_counts.plot(kind="bar")
            plt.title("Top 10 Email Domains")
            plt.xlabel("Domain")
            plt.ylabel("Count")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            
            filepath = "reports/visualizations/domain_distribution.png"
            plt.savefig(filepath)
            plt.close()
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error plotting domain distribution: {str(e)}")
            return ""