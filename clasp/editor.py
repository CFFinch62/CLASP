# clasp/editor.py

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QFileDialog, QMessageBox, QTextEdit
from PyQt6.QtGui import QFont, QPainter, QColor, QTextFormat, QTextCursor
from PyQt6.QtCore import Qt, QRect, QSize
from pathlib import Path

# Note: highlighter import commented out until implemented in Phase 3
from .highlighter import LogoHighlighter


class LineNumberArea(QWidget):
    """Widget for displaying line numbers."""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        
    def sizeHint(self):
        return QSize(self.editor.line_number_width(), 0)
        
    def paintEvent(self, event):
        self.editor.line_number_paint(event)


class LogoEditor(QPlainTextEdit):
    """Code editor with Logo support."""
    
    def __init__(self, theme):
        super().__init__()
        self.theme = theme
        self.current_file = None
        self.is_modified = False
        
        # Font
        font = QFont("Monospace", 12)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Line numbers
        self.line_numbers = LineNumberArea(self)
        self.blockCountChanged.connect(self._update_line_number_width)
        self.updateRequest.connect(self._update_line_numbers)
        self._update_line_number_width()
        
        # Current line highlight
        self.cursorPositionChanged.connect(self._highlight_current_line)
        
        # Track modifications
        self.textChanged.connect(self._on_text_changed)
        
        # Syntax highlighter
        self.highlighter = LogoHighlighter(self.document(), theme)
        
        # Bracket matching
        self.cursorPositionChanged.connect(self._match_brackets)
        
        # Apply theme
        self._apply_theme()
        self._highlight_current_line()
        
    def _apply_theme(self):
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
        # Recreate highlighter with new theme colors
        self.highlighter = LogoHighlighter(self.document(), theme)
        # Force repaint of line numbers
        self.line_numbers.update()
        self._highlight_current_line()
        
    def line_number_width(self):
        """Calculate width needed for line numbers."""
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
        
    def _update_line_number_width(self):
        self.setViewportMargins(self.line_number_width(), 0, 0, 0)
        
    def _update_line_numbers(self, rect, dy):
        if dy:
            self.line_numbers.scroll(0, dy)
        else:
            self.line_numbers.update(0, rect.y(), self.line_numbers.width(), rect.height())
            
        if rect.contains(self.viewport().rect()):
            self._update_line_number_width()
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_numbers.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_width(), cr.height())
        )
        
    def line_number_paint(self, event):
        """Paint line numbers."""
        painter = QPainter(self.line_numbers)
        painter.fillRect(event.rect(), QColor(self.theme['line_numbers_bg']))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        
        painter.setPen(QColor(self.theme['line_numbers_fg']))
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0, top,
                    self.line_numbers.width() - 5,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, number
                )
            
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1
            
    def _highlight_current_line(self):
        """Highlight the current line and matching brackets."""
        extra_selections = []
        
        if not self.isReadOnly():
            # Current line
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(self.theme['editor_current_line']))
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
            
            # Match brackets
            match_pos = self._find_matching_bracket()
            if match_pos is not None:
                match_selection = QTextEdit.ExtraSelection()
                match_selection.format.setBackground(QColor(self.theme['syntax_keyword'])) # Reuse match color or define a new one?
                # Usually editors underline or bold match. Let's make it bold/colored background?
                # Using a distinct color for bracket match would be better, but we only have theme so far.
                # Let's use syntax_variable color for now or hardcode a light touch.
                match_selection.format.setBackground(QColor("#4C566A")) # Light grey accent
                match_selection.format.setFontWeight(QFont.Weight.Bold)
                
                cursor = self.textCursor()
                cursor.setPosition(match_pos)
                cursor.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor)
                match_selection.cursor = cursor
                extra_selections.append(match_selection)
            
        self.setExtraSelections(extra_selections)

    def _match_brackets(self):
        # Just re-trigger highlight which includes matching logic
        self._highlight_current_line()
        
    def _find_matching_bracket(self):
        """Find the matching bracket position."""
        cursor = self.textCursor()
        position = cursor.position()
        text = self.toPlainText()
        
        if position >= len(text) and position > 0:
             # If at end, check previous char
             char = text[position - 1]
             if char in '])':
                 position -= 1
             else:
                 # Check current pos if valid? no, cursor is between chars.
                 # Usually editors match char to the right of cursor unless at end or it's a closing bracket?
                 match_right = False
        
        # Simple logic: check char to Right of cursor, if not bracket, check Left.
        if position < len(text) and text[position] in '[]()':
            target_pos = position
        elif position > 0 and text[position - 1] in '[]()':
            target_pos = position - 1
        else:
            return None
            
        char = text[target_pos]
        brackets = {'[': ']', ']': '[', '(': ')', ')': '('}
        
        if char not in brackets:
            return None
            
        # Direction
        if char in '[(':
            direction = 1
            start = target_pos + 1
            target_char = brackets[char]
        else:
            direction = -1
            start = target_pos - 1
            target_char = brackets[char]
            
        # Search
        depth = 1
        pos = start
        
        while 0 <= pos < len(text):
            if text[pos] == char:
                depth += 1
            elif text[pos] == target_char:
                depth -= 1
                
            if depth == 0:
                return pos
                
            pos += direction
            
        return None
        
    def _on_text_changed(self):
        """Track modifications."""
        self.is_modified = True
        self._update_title()
        
    def _update_title(self):
        """Update window title with file info."""
        title = "CLASP"
        if self.current_file:
            title = f"{Path(self.current_file).name} - CLASP"
        if self.is_modified:
            title = "* " + title
        # Signal to main window to update title
        if self.window():
            self.window().setWindowTitle(title)
            
    def new_file(self):
        """Create new file."""
        if self.is_modified:
            if not self._confirm_discard():
                return
        self.clear()
        self.current_file = None
        self.is_modified = False
        self._update_title()
        
    def open_file(self):
        """Open file dialog."""
        if self.is_modified:
            if not self._confirm_discard():
                return
                
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Logo File",
            str(Path.home()),
            "Logo Files (*.logo *.lg *.lgo);;All Files (*)"
        )
        
        if path:
            self.load_file(path)
            
    def load_file(self, path):
        """Load file into editor."""
        try:
            with open(path, 'r') as f:
                self.setPlainText(f.read())
            self.current_file = path
            self.is_modified = False
            self._update_title()
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")
            
    def save_file(self):
        """Save current file."""
        if self.current_file:
            self._save_to_path(self.current_file)
        else:
            self.save_file_as()
            
    def save_file_as(self):
        """Save with new filename."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Logo File",
            str(Path.home()),
            "Logo Files (*.logo);;All Files (*)"
        )
        
        if path:
            if not path.endswith(('.logo', '.lg', '.lgo')):
                path += '.logo'
            self._save_to_path(path)
            
    def _save_to_path(self, path):
        """Save content to path."""
        try:
            with open(path, 'w') as f:
                f.write(self.toPlainText())
            self.current_file = path
            self.is_modified = False
            self._update_title()
        except IOError as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")
            
    def _confirm_discard(self):
        """Ask user to confirm discarding changes."""
        reply = QMessageBox.question(
            self, "Unsaved Changes",
            "You have unsaved changes. Discard them?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
