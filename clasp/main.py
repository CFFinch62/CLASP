# clasp/main.py

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from .main_window import MainWindow

def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("CLASP")
    app.setOrganizationName("Fragillidae Software")
    
    # Set application icon
    # Get the path relative to this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "images", "clasp-icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
