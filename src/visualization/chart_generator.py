import logging
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime

class ChartGenerator:
    """Generates various visualization charts for validation results"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path("reports/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")
        
    def generate_charts(self, results: List[Dict]) -> Dict[str, str]:
        """
        Generate multiple visualization charts.
        
        Args:
            results: List of validation results
            
        Returns:
            Dict mapping chart types to file paths
        """
        try:
            df = pd.DataFrame(results)
            paths = {}
            
            # Generate various charts
            paths["validation_summary"] = self._create_validation_summary(df)
            paths["score_distribution"] = self._create_score_distribution(df)
            paths["issue_breakdown"] = self._create_issue_breakdown(df)
            paths["domain_distribution"] = self._create_domain_distribution(df)
            paths["validation_timeline"] = self._create_validation_timeline(df)
            
            return paths
            
        except Exception as e:
            self.logger.error(f"Error generating charts: {str(e)}")
            return {}
            
    def _create_validation_summary(self, df: pd.DataFrame) -> str:
        """Create pie chart of validation results."""
        try:
            plt.figure(figsize=(10, 8))
            valid_counts = df['is_valid'].value_counts()
            plt.pie(
                valid_counts,
                labels=['Valid', 'Invalid'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c']
            )
            plt.title('Email Validation Results')
            
            filepath = self.output_dir / 'validation_summary.png'
            plt.savefig(filepath)
            plt.close()
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error creating validation summary: {str(e)}")
            return ""
            
    def _create_score_distribution(self, df: pd.DataFrame) -> str:
        """Create histogram of validation scores."""
        try:
            plt.figure(figsize=(12, 6))
            sns.histplot(data=df, x='score', bins=20)
            plt.title('Distribution of Validation Scores')
            plt.xlabel('Score')
            plt.ylabel('Count')
            
            filepath = self.output_dir / 'score_distribution.png'
            plt.savefig(filepath)
            plt.close()
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error creating score distribution: {str(e)}")
            return ""
            
    def _create_issue_breakdown(self, df: pd.DataFrame) -> str:
        """Create bar chart of validation issues."""
        try:
            plt.figure(figsize=(12, 8))
            
            # Collect all issues
            all_issues = []
            for issues in df['issues']:
                all_issues.extend(issues)
                
            issue_counts = pd.Series(all_issues).value_counts()
            
            # Create bar plot
            sns.barplot(x=issue_counts.values, y=issue_counts.index)
            plt.title('Common Validation Issues')
            plt.xlabel('Count')
            
            filepath = self.output_dir / 'issue_breakdown.png'
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error creating issue breakdown: {str(e)}")
            return ""
            
    def _create_domain_distribution(self, df: pd.DataFrame) -> str:
        """Create bar chart of email domains."""
        try:
            plt.figure(figsize=(12, 6))
            
            # Extract domains
            domains = df['email'].apply(lambda x: x.split('@')[1])
            domain_counts = domains.value_counts().head(10)
            
            # Create bar plot
            sns.barplot(x=domain_counts.values, y=domain_counts.index)
            plt.title('Top 10 Email Domains')
            plt.xlabel('Count')
            
            filepath = self.output_dir / 'domain_distribution.png'
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error creating domain distribution: {str(e)}")
            return ""
            
    def _create_validation_timeline(self, df: pd.DataFrame) -> str:
        """Create line chart of validation results over time."""
        try:
            plt.figure(figsize=(12, 6))
            
            # Convert timestamp to datetime if needed
            if 'timestamp' not in df.columns:
                df['timestamp'] = pd.Timestamp.now()
                
            # Group by timestamp
            timeline_data = df.groupby(
                pd.Grouper(key='timestamp', freq='H')
            )['is_valid'].agg(['count', 'mean'])
            
            # Create dual-axis plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            
            # Plot total validations
            timeline_data['count'].plot(ax=ax1)
            ax1.set_title('Validation Volume Over Time')
            ax1.set_ylabel('Number of Validations')
            
            # Plot validity rate
            timeline_data['mean'].plot(ax=ax2)
            ax2.set_title('Validity Rate Over Time')
            ax2.set_ylabel('Validity Rate')
            
            plt.tight_layout()
            
            filepath = self.output_dir / 'validation_timeline.png'
            plt.savefig(filepath)
            plt.close()
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error creating validation timeline: {str(e)}")
            return ""