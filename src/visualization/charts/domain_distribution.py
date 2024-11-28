import logging
from typing import Dict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from .base_chart import BaseChart

class DomainDistributionChart(BaseChart):
    """Generates domain distribution bar chart"""
    
    def generate(self, df: pd.DataFrame, config: Dict = None) -> str:
        """Create bar chart of email domains."""
        try:
            if not self.validate_data(df, ['email']):
                return ""
                
            self.setup_plot(config)
            
            # Extract domains
            domains = df['email'].apply(lambda x: x.split('@')[1])
            domain_counts = domains.value_counts().head(10)
            
            # Create bar plot
            sns.barplot(x=domain_counts.values, y=domain_counts.index)
            plt.title('Top 10 Email Domains')
            plt.xlabel('Count')
            
            return self.save_plot('domain_distribution.png')
            
        except Exception as e:
            self.logger.error(f"Error creating domain distribution: {str(e)}")
            return ""