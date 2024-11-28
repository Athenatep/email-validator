import logging
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

class DragDropWidget(QWidget):
    """Widget that handles file drag and drop."""
    
    fileDropped = pyqtSignal(str)  # Signal emitted when file is dropped
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the widget UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create drop area
        self.drop_label = QLabel("Drag and drop email list file here\nor click to select")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 8px;
                padding: 30px;
                background: #f8f9fa;
                color: #666;
            }
        """)
        layout.addWidget(self.drop_label)
        
        # Enable drop
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.accept()
            self.drop_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #2196F3;
                    border-radius: 8px;
                    padding: 30px;
                    background: #E3F2FD;
                    color: #1976D2;
                }
            """)
        else:
            event.ignore()
            
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 8px;
                padding: 30px;
                background: #f8f9fa;
                color: #666;
            }
        """)
        
    def dropEvent(self, event: QDropEvent):
        """Handle file drop event."""
        try:
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                self.fileDropped.emit(file_path)
                self.drop_label.setText(f"Selected: {file_path.split('/')[-1]}")
        except Exception as e:
            self.logger.error(f"Error handling file drop: {str(e)}")
            
        self.drop_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 8px;
                padding: 30px;
                background: #f8f9fa;
                color: #666;
            }
        """)