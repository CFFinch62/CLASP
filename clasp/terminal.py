# clasp/terminal.py

from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtCore import Qt, pyqtSignal

class LogoTerminal(QPlainTextEdit):
    """Terminal widget for Logo REPL."""
    
    command_entered = pyqtSignal(str)
    
    def __init__(self, interpreter, theme):
        super().__init__()
        self.interpreter = interpreter
        self.theme = theme
        self.prompt = "? "
        self.prompt_position = 0
        self.history = []
        self.history_index = 0
        
        # Appearance
        self.setFont(QFont("Monospace", 11))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        # Apply theme
        self._apply_theme()
        
        # Show initial prompt
        self.show_prompt()
    
    def _apply_theme(self):
        """Apply current theme to terminal."""
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {self.theme['editor_bg']};
                color: {self.theme['editor_fg']};
                selection-background-color: {self.theme['editor_selection']};
                border: none;
            }}
        """)
    
    def set_theme(self, theme):
        """Switch to a new theme."""
        self.theme = theme
        self._apply_theme()
        
    def show_prompt(self):
        """Display the Logo prompt."""
        self.appendPlainText(self.prompt)
        self.prompt_position = self.textCursor().position()
        
    def keyPressEvent(self, event):
        cursor = self.textCursor()
        
        # Prevent editing before prompt
        if cursor.position() < self.prompt_position:
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            
        key = event.key()
        
        if key == Qt.Key.Key_Return:
            command = self._get_current_input()
            self.appendPlainText("")  # New line
            
            if command.strip():
                self.history.append(command)
                self.history_index = len(self.history)
                self._execute_command(command)
            else:
                self.show_prompt()
                
        elif key == Qt.Key.Key_Up:
            self._history_previous()
            
        elif key == Qt.Key.Key_Down:
            self._history_next()
            
        elif key == Qt.Key.Key_Home:
            # Go to start of input, not start of line
            cursor.setPosition(self.prompt_position)
            self.setTextCursor(cursor)
            
        elif key == Qt.Key.Key_Backspace:
            # Don't backspace past prompt
            if cursor.position() > self.prompt_position:
                super().keyPressEvent(event)
                
        else:
            super().keyPressEvent(event)
            
    def _get_current_input(self):
        """Get text after prompt."""
        text = self.toPlainText()
        return text[self.prompt_position:]
    
    def _replace_current_input(self, text):
        """Replace current input with text."""
        cursor = self.textCursor()
        cursor.setPosition(self.prompt_position)
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(text)
        
    def _history_previous(self):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self._replace_current_input(self.history[self.history_index])
            
    def _history_next(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._replace_current_input(self.history[self.history_index])
        elif self.history_index == len(self.history) - 1:
            self.history_index = len(self.history)
            self._replace_current_input("")
            
    def _execute_command(self, command):
        """Execute Logo command and display result."""
        # Handle clear command manually if not handled by interpreter
        cmd_stripped = command.strip().lower()
        if cmd_stripped in ('clear', 'ct'):
            self.clear()
            self.show_prompt()
            return

        result = self.interpreter.execute(command)
        
        if result['stdout']:
            self.appendPlainText(result['stdout'].rstrip())
            
        if not result['success']:
            self.appendPlainText(f"Error: {result['stderr']}")
            
        self.show_prompt()

    def execute_code(self, code):
        """Execute code from editor."""
        self.appendPlainText(f"\nRunning code...\n")
        self._execute_command(code)
        
    def append_output(self, text):
        """Append output text (for use by interpreter callbacks)."""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
