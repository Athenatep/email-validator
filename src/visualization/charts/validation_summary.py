import logging
from typing import Dict
import matplotlib.pyplot as plt
import pandas as pd
from .base_chart import BaseChart

class ValidationSummaryChart(BaseChart):
    """Generates validation summary pie chart"""
    
    def generate(self, df: pd.DataFrame, config: Dict = None) -> str:
        """Create pie chart of validation results."""
        try:
            if not self.validate_data(df, ['is_valid']):
                return ""
                
            self.setup_plot(config)
            valid_counts = df['is_valid'].value_counts()
            
            plt.pie(
                valid_counts,
                labels=['Valid', 'Invalid'],
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c']
            )
            plt.title('Email Validation Results')
            
            return self.save_plot('validation_summary.png')
            
        except Exception as e:
            self.logger.error(f"Error creating validation summary: {str(e)}")
            return ""