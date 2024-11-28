import logging
from typing import Dict
import matplotlib.pyplot as plt
import pandas as pd
from .base_chart import BaseChart

class ValidationTimelineChart(BaseChart):
    """Generates validation timeline charts"""
    
    def generate(self, df: pd.DataFrame, config: Dict = None) -> str:
        """Create line chart of validation results over time."""
        try:
            if not self.validate_data(df, ['is_valid']):
                return ""
                
            self.setup_plot(config)
            
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
            
            return self.save_plot('validation_timeline.png')
            
        except Exception as e:
            self.logger.error(f"Error creating validation timeline: {str(e)}")
            return ""