import logging
from typing import Dict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from .base_chart import BaseChart

class ScoreDistributionChart(BaseChart):
    """Generates score distribution histogram"""
    
    def generate(self, df: pd.DataFrame, config: Dict = None) -> str:
        """Create histogram of validation scores."""
        try:
            if not self.validate_data(df, ['score']):
                return ""
                
            self.setup_plot(config)
            sns.histplot(data=df, x='score', bins=20)
            plt.title('Distribution of Validation Scores')
            plt.xlabel('Score')
            plt.ylabel('Count')
            
            return self.save_plot('score_distribution.png')
            
        except Exception as e:
            self.logger.error(f"Error creating score distribution: {str(e)}")
            return ""