from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ChartConfig:
    """Configuration for chart generation"""
    
    figsize: tuple = (12, 6)
    dpi: int = 100
    style: str = 'seaborn'
    palette: str = 'husl'
    title_fontsize: int = 14
    label_fontsize: int = 12
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'figsize': self.figsize,
            'dpi': self.dpi,
            'style': self.style,
            'palette': self.palette,
            'title_fontsize': self.title_fontsize,
            'label_fontsize': self.label_fontsize
        }