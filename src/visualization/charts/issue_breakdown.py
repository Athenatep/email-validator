import logging
from typing import Dict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from .base_chart import BaseChart

class IssueBreakdownChart(BaseChart):
    """Generates issue breakdown bar chart"""
    
    def generate(self, df: pd.DataFrame, config: Dict = None) -> str:
        """Create bar chart of validation issues."""
        try:
            if not self.validate_data(df, ['issues']):
                return ""
                
            self.setup_plot(config)
            
            # Collect all issues
            all_issues = []
            for issues in df['issues']:
                all_issues.extend(issues)
                
            issue_counts = pd.Series(all_issues).value_counts()
            
            # Create bar plot
            sns.barplot(x=issue_counts.values, y=issue_counts.index)
            plt.title('Common Validation Issues')
            plt.xlabel('Count')
            
            return self.save_plot('issue_breakdown.png')
            
        except Exception as e:
            self.logger.error(f"Error creating issue breakdown: {str(e)}")
            return ""