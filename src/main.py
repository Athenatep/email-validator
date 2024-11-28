import sys
import logging
from PyQt6.QtWidgets import QApplication
from src.utils.logger import setup_logger
from src.utils.settings_manager import SettingsManager
from src.gui.main_window import MainWindow

def main():
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize Qt application
        app = QApplication(sys.argv)
        
        # Initialize settings
        settings = SettingsManager()
        
        # Create and show main window
        window = MainWindow(settings)
        window.show()
        
        # Start event loop
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()