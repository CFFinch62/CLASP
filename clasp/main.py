# clasp/main.py

import sys
import os
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow

def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("CLASP")
    app.setOrganizationName("Fragillidae Software")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
