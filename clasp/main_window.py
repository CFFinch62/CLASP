# clasp/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QSplitter, QWidget, QVBoxLayout,
    QMenuBar, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QActionGroup

from .terminal import LogoTerminal
from .editor import LogoEditor
from .file_browser import LogoFileBrowser
from .interpreter import LogoInterpreter, check_pylogo
from .themes import THEMES, DEFAULT_THEME
from .graphics import TurtleGraphicsManager


class MainWindow(QMainWindow):
    """CLASP main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLASP IDE")
        self.resize(1200, 800)
        
        self.theme = THEMES[DEFAULT_THEME]
        
        # Check PyLogo
        if not check_pylogo():
            # In a real GUI we would show a message box, but for headless/agent testing
            # we might want to just log it or continue with disabled functionality.
            # However, per spec, we show a critical message.
            # Note: QTimer.singleShot could be used to avoid blocking __init__ if needed,
            # but for now we follow the plan.
            pass
            # We defer the message box to show() or after init to ensure window is ready?
            # Or just show it.
        
        # Initialize interpreter
        # If pylogo is missing, interpreter init raises ImportError, handling needed?
        # The checks inside interpreter.py raise ImportError.
        # We should handle it gracefully.
        try:
            self.graphics_manager = TurtleGraphicsManager()
            self.graphics_manager.set_callback(self._on_graphics_state_change)
            self.interpreter = LogoInterpreter(graphics_manager=self.graphics_manager)
        except ImportError:
            self.interpreter = None # Fallback or restricted mode
            self.graphics_manager = None
        
        # Create widgets
        self._create_widgets()
        self._create_menus()
        self._apply_theme()
        
        if not check_pylogo():
             # We execute this later to ensure the loop is running if we used a signal,
             # but strictly here it's fine.
             # However, let's just use print for now if no GUI?
             # But this is a GUI app.
             pass

    def closeEvent(self, event):
        """Handle window close event."""
        if self.editor.is_modified:
            if self.editor._confirm_discard():
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def showEvent(self, event):
        super().showEvent(event)
        if not check_pylogo():
             QMessageBox.critical(
                self, "Missing Dependency",
                "PyLogo is not installed.\n\nRun: pip install pylogo"
            )

    def _create_widgets(self):
        """Create main UI widgets."""
        # Main splitter (horizontal)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # File browser (left)
        self.file_browser = LogoFileBrowser(self.theme)
        self.file_browser.file_selected.connect(self._on_file_selected)
        main_splitter.addWidget(self.file_browser)
        
        # Editor/Terminal splitter (right, vertical)
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Editor (top)
        self.editor = LogoEditor(self.theme)
        right_splitter.addWidget(self.editor)
        
        # Terminal (bottom)
        # Handle case where interpreter is None
        class DummyInterpreter:
            def execute(self, code):
                return {'success': False, 'stdout': '', 'stderr': 'Interpreter not available (PyLogo missing).'}
            def reset(self): pass
            
        term_interp = self.interpreter if self.interpreter else DummyInterpreter()
        self.terminal = LogoTerminal(term_interp, self.theme)
        right_splitter.addWidget(self.terminal)
        
        right_splitter.setSizes([500, 300])
        main_splitter.addWidget(right_splitter)
        
        main_splitter.setSizes([200, 1000])
        self.setCentralWidget(main_splitter)
        
    def _create_menus(self):
        """Create application menus."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.editor.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.editor.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.editor.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.editor.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Logo menu
        logo_menu = menubar.addMenu("&Logo")
        
        run_file_action = QAction("&Run File", self)
        run_file_action.setShortcut("F5")
        run_file_action.triggered.connect(self._run_file)
        logo_menu.addAction(run_file_action)
        
        run_selection_action = QAction("Run &Selection", self)
        run_selection_action.setShortcut("F9")
        run_selection_action.triggered.connect(self._run_selection)
        logo_menu.addAction(run_selection_action)
        
        logo_menu.addSeparator()
        
        clear_action = QAction("&Clear Terminal", self)
        clear_action.triggered.connect(self.terminal.clear)
        logo_menu.addAction(clear_action)
        
        reset_action = QAction("R&eset Interpreter", self)
        reset_action.triggered.connect(self._reset_interpreter)
        logo_menu.addAction(reset_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        self.graphics_action = QAction("&Graphics Window", self)
        self.graphics_action.setShortcut("Ctrl+G")
        self.graphics_action.setCheckable(True)
        self.graphics_action.toggled.connect(self._toggle_graphics)
        view_menu.addAction(self.graphics_action)
        
        view_menu.addSeparator()
        
        # Themes submenu
        themes_menu = view_menu.addMenu("&Themes")
        self.theme_actions = {}
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)
        
        for theme_key, theme_dict in THEMES.items():
            action = QAction(theme_dict['name'], self)
            action.setCheckable(True)
            action.setData(theme_key)
            action.triggered.connect(lambda checked, key=theme_key: self._switch_theme(key))
            theme_group.addAction(action)
            themes_menu.addAction(action)
            self.theme_actions[theme_key] = action
            
            # Check the current theme
            if theme_key == DEFAULT_THEME:
                action.setChecked(True)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About CLASP", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
    def _apply_theme(self):
        """Apply theme to main window."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme['background']};
            }}
            QSplitter::handle {{
                background-color: {self.theme['accent']};
            }}
            QMenuBar {{
                background-color: {self.theme['background']};
                color: {self.theme['editor_fg']};
            }}
            QMenuBar::item:selected {{
                background-color: {self.theme['accent']};
            }}
            QMenu {{
                background-color: {self.theme['background']};
                color: {self.theme['editor_fg']};
            }}
            QMenu::item:selected {{
                background-color: {self.theme['editor_selection']};
            }}
        """)
    
    def _switch_theme(self, theme_key):
        """Switch to a different theme."""
        self.theme = THEMES[theme_key]
        
        # Update all components
        self._apply_theme()
        self.editor.set_theme(self.theme)
        self.terminal.set_theme(self.theme)
        self.file_browser.set_theme(self.theme)
        
        # Update the checked state
        if theme_key in self.theme_actions:
            self.theme_actions[theme_key].setChecked(True)
        
    def _on_file_selected(self, path):
        """Handle file selection from browser."""
        self.editor.load_file(path)
        
    def _run_file(self):
        """Run current file."""
        code = self.editor.toPlainText()
        if code.strip():
            self.terminal.clear()
            self.terminal.execute_code(code)
            
    def _run_selection(self):
        """Run selected text or current line."""
        cursor = self.editor.textCursor()
        code = cursor.selectedText()
        
        if not code:
            cursor.select(cursor.SelectionType.LineUnderCursor)
            code = cursor.selectedText()
            
        if code.strip():
            # Convert paragraph separator to newline
            code = code.replace('\u2029', '\n')
            self.terminal.clear()
            self.terminal.execute_code(code)
            
    def _reset_interpreter(self):
        """Reset the Logo interpreter."""
        if self.interpreter:
            self.interpreter.reset()
            self.terminal.append_output("\n--- Interpreter Reset ---\n")
            self.terminal.show_prompt()
        
    def _toggle_graphics(self, checked):
        """Toggle turtle graphics window."""
        if not self.graphics_manager:
            return
            
        if checked:
            self.graphics_manager.initialize()
            self.graphics_manager.show()
        else:
            self.graphics_manager.hide()
        
    def _on_graphics_state_change(self, visible):
        """Handle state change from graphics manager."""
        if visible != self.graphics_action.isChecked():
            self.graphics_action.blockSignals(True)
            self.graphics_action.setChecked(visible)
            self.graphics_action.blockSignals(False)

    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About CLASP",
            "<h2>CLASP</h2>"
            "<p><b>Coding in Logo to Attack Serious Problems</b></p>"
            "<p>A modern IDE for Logo programming.</p>"
            "<p>Honoring the work of Professor Brian Harvey "
            "and the Logo community.</p>"
            "<p>©2025 Chuck Finch - Fragillidae Software</p>"
        )
