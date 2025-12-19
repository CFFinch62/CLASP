# clasp/file_browser.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QPushButton, QLabel, QSizePolicy, QHeaderView
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from pathlib import Path
import os

class LogoFileBrowser(QWidget):
    """File browser for Logo project navigation."""
    
    file_selected = pyqtSignal(str)
    
    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        
        # Prevent auto-expansion when root changes - keep user-set width
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        # Set minimum width to prevent browser from disappearing
        self.setMinimumWidth(100)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.path_label = QLabel()
        self.up_button = QPushButton("↑")
        self.up_button.setFixedWidth(30)
        self.up_button.clicked.connect(self.go_up)
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setFixedWidth(30)
        self.refresh_button.clicked.connect(self.refresh)
        toolbar.addWidget(self.path_label, 1)
        toolbar.addWidget(self.up_button)
        toolbar.addWidget(self.refresh_button)
        layout.addLayout(toolbar)
        
        # Tree view
        self.tree = QTreeView()
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.logo", "*.lg", "*.lgo"])
        self.model.setNameFilterDisables(False)
        
        self.tree.setModel(self.model)
        
        # Hide unnecessary columns
        self.tree.hideColumn(1)  # Size
        self.tree.hideColumn(2)  # Type
        self.tree.hideColumn(3)  # Date
        
        # Set header to stretch mode so column width doesn't drive widget width
        # This prevents the browser from expanding when navigating to deeper paths
        header = self.tree.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.tree.doubleClicked.connect(self._on_double_click)
        layout.addWidget(self.tree)
        
        # Apply theme
        self._apply_theme()
        
        # Set initial directory
        self.set_root(str(Path.home()))
    
    def _apply_theme(self):
        """Apply current theme to file browser."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['background']};
                color: {self.theme['editor_fg']};
            }}
            QTreeView {{
                background-color: {self.theme['editor_bg']};
                color: {self.theme['editor_fg']};
                border: none;
            }}
            QTreeView::item:selected {{
                background-color: {self.theme['editor_selection']};
            }}
            QLabel {{
                padding: 4px;
                color: {self.theme['editor_fg']};
            }}
            QPushButton {{
                background-color: {self.theme['accent']};
                color: {self.theme['editor_fg']};
                border: none;
                padding: 4px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['editor_selection']};
            }}
        """)
    
    def set_theme(self, theme):
        """Switch to a new theme."""
        self.theme = theme
        self._apply_theme()
        
    def set_root(self, path):
        """Set the root directory."""
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.path_label.setText(self._shorten_path(path))
        self.current_path = path
        
    def _shorten_path(self, path):
        """Shorten path for display."""
        home = str(Path.home())
        if path.startswith(home):
            return "~" + path[len(home):]
        return path
        
    def go_up(self):
        """Navigate to parent directory."""
        parent = str(Path(self.current_path).parent)
        self.set_root(parent)
        
    def refresh(self):
        """Refresh current directory."""
        self.model.setRootPath("")
        self.model.setRootPath(self.current_path)
        
    def _on_double_click(self, index):
        """Handle double-click."""
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.file_selected.emit(path)
        elif os.path.isdir(path):
            self.set_root(path)
