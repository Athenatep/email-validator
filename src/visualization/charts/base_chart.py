import logging
from typing import Dict, Any
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

class BaseChart:
    """Base class for all chart generators"""
    
    def __init__(self, output_dir: Path):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self.default_config = {
            'figsize': (12, 6),
            'dpi': 100,
            'style': 'seaborn',
            'palette': 'husl'
        }
        
    def setup_plot(self, config: Dict[str, Any] = None) -> None:
        """Set up plot with configuration."""
        plot_config = {**self.default_config, **(config or {})}
        plt.style.use(plot_config['style'])
        plt.figure(figsize=plot_config['figsize'], dpi=plot_config['dpi'])
        
    def save_plot(self, filename: str) -> str:
        """Save plot to file."""
        try:
            filepath = self.output_dir / filename
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error saving plot: {str(e)}")
            return ""
            
    def validate_data(self, df: pd.DataFrame, required_columns: list) -> bool:
        """Validate DataFrame has required columns."""
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.logger.error(f"Missing required columns: {missing_columns}")
            return False
        return True