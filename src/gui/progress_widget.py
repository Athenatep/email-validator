import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QProgressBar,
    QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt

class ProgressWidget(QWidget):
    """Widget for displaying validation progress."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the widget UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Status layout
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        
        self.count_label = QLabel("0/0")
        status_layout.addWidget(self.count_label, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(status_layout)
        
        # Stats layout
        stats_layout = QHBoxLayout()
        
        self.valid_label = QLabel("Valid: 0")
        stats_layout.addWidget(self.valid_label)
        
        self.invalid_label = QLabel("Invalid: 0")
        stats_layout.addWidget(self.invalid_label)
        
        self.avg_score_label = QLabel("Avg Score: 0")
        stats_layout.addWidget(self.avg_score_label)
        
        layout.addLayout(stats_layout)
        
    def update_progress(self, current: int, total: int):
        """Update progress display."""
        try:
            percentage = int(current * 100 / total) if total else 0
            self.progress_bar.setValue(percentage)
            self.count_label.setText(f"{current}/{total}")
            
        except Exception as e:
            self.logger.error(f"Error updating progress: {str(e)}")
            
    def update_stats(self, stats: dict):
        """Update validation statistics."""
        try:
            self.valid_label.setText(f"Valid: {stats.get('valid_count', 0)}")
            self.invalid_label.setText(f"Invalid: {stats.get('invalid_count', 0)}")
            self.avg_score_label.setText(f"Avg Score: {stats.get('avg_score', 0):.1f}")
            
        except Exception as e:
            self.logger.error(f"Error updating stats: {str(e)}")
            
    def set_status(self, status: str):
        """Update status message."""
        self.status_label.setText(status)