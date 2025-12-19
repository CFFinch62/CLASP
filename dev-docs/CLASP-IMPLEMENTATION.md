# CLASP Implementation Guide

**Version:** 1.1  
**Date:** December 2024

---

## Overview

This document provides a phased implementation plan for CLASP using PyLogo and Python's turtle module. Each phase builds on the previous, with verification checkpoints.

---

## Phase 1: Foundation

**Goal:** Minimal working application with PyLogo integration

### 1.1 Tasks

1. **Project structure setup**
   ```
   clasp/
   ├── clasp/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── main_window.py
   │   ├── terminal.py
   │   ├── editor.py
   │   ├── file_browser.py
   │   ├── interpreter.py
   │   ├── graphics.py
   │   ├── config.py
   │   └── themes.py
   ├── tests/
   │   └── __init__.py
   ├── examples/
   │   ├── hello.logo
   │   ├── square.logo
   │   └── factorial.logo
   ├── docs/
   ├── requirements.txt
   ├── setup.py
   └── README.md
   ```

2. **Main window shell**
   - QMainWindow with menu bar
   - Three-pane layout using QSplitter
   - Basic menus: File, Edit, View, Logo, Help

3. **PyLogo interpreter wrapper**
   - Import and initialize PyLogo
   - Execute code method
   - Capture stdout/stderr

4. **Terminal widget (basic)**
   - Display output
   - Accept input
   - Execute via PyLogo

### 1.2 Verification Checkpoint

- [ ] Application launches without errors
- [ ] PyLogo initializes successfully
- [ ] Can type `print "hello` and see output
- [ ] Can type `print sum 2 3` and see `5`
- [ ] Can define a procedure with `to` / `end`
- [ ] Application exits cleanly

### 1.3 Key Code: Interpreter Wrapper

```python
# clasp/interpreter.py

import io
import sys
from contextlib import redirect_stdout, redirect_stderr

try:
    from pylogo import Logo
    PYLOGO_AVAILABLE = True
except ImportError:
    PYLOGO_AVAILABLE = False


class LogoInterpreter:
    """Wrapper around PyLogo interpreter."""
    
    def __init__(self, graphics_manager=None):
        if not PYLOGO_AVAILABLE:
            raise ImportError("PyLogo not installed. Run: pip install pylogo")
        
        self.logo = Logo()
        self.graphics = graphics_manager
        
    def execute(self, code):
        """Execute Logo code and return results."""
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                result = self.logo.execute(code)
            
            return {
                'success': True,
                'result': result,
                'stdout': stdout_capture.getvalue(),
                'stderr': stderr_capture.getvalue()
            }
            
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'stdout': stdout_capture.getvalue(),
                'stderr': str(e)
            }
    
    def reset(self):
        """Reset interpreter state."""
        self.logo = Logo()


def check_pylogo():
    """Check if PyLogo is available."""
    return PYLOGO_AVAILABLE
```

### 1.4 Key Code: Main Window Shell

```python
# clasp/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QSplitter, QWidget, QVBoxLayout,
    QMenuBar, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from .terminal import LogoTerminal
from .editor import LogoEditor
from .file_browser import LogoFileBrowser
from .interpreter import LogoInterpreter, check_pylogo
from .themes import AMBER_BLUE_THEME


class MainWindow(QMainWindow):
    """CLASP main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLASP - Coding in Logo to Attack Serious Problems")
        self.resize(1200, 800)
        
        self.theme = AMBER_BLUE_THEME
        
        # Check PyLogo
        if not check_pylogo():
            QMessageBox.critical(
                self, "Missing Dependency",
                "PyLogo is not installed.\n\nRun: pip install pylogo"
            )
        
        # Initialize interpreter
        self.interpreter = LogoInterpreter()
        
        # Create widgets
        self._create_widgets()
        self._create_menus()
        self._apply_theme()
        
    def _create_widgets(self):
        """Create main UI widgets."""
        # Main splitter (horizontal)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # File browser (left)
        self.file_browser = LogoFileBrowser()
        self.file_browser.file_selected.connect(self._on_file_selected)
        main_splitter.addWidget(self.file_browser)
        
        # Editor/Terminal splitter (right, vertical)
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Editor (top)
        self.editor = LogoEditor(self.theme)
        right_splitter.addWidget(self.editor)
        
        # Terminal (bottom)
        self.terminal = LogoTerminal(self.interpreter)
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
        
        graphics_action = QAction("&Graphics Window", self)
        graphics_action.setShortcut("Ctrl+G")
        graphics_action.triggered.connect(self._show_graphics)
        view_menu.addAction(graphics_action)
        
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
        """)
        
    def _on_file_selected(self, path):
        """Handle file selection from browser."""
        self.editor.load_file(path)
        
    def _run_file(self):
        """Run current file."""
        code = self.editor.toPlainText()
        if code.strip():
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
            self.terminal.execute_code(code)
            
    def _reset_interpreter(self):
        """Reset the Logo interpreter."""
        self.interpreter.reset()
        self.terminal.append_output("\n--- Interpreter Reset ---\n")
        self.terminal.show_prompt()
        
    def _show_graphics(self):
        """Show turtle graphics window."""
        # Will be implemented in Phase 4
        pass
        
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
            "<p>© Fragillidae Software</p>"
        )
```

---

## Phase 2: Editor & File Operations

**Goal:** Functional code editing with file management

### 2.1 Tasks

1. **Code editor implementation**
   - QPlainTextEdit subclass
   - Line numbers widget
   - Current line highlighting
   - Load/save files

2. **File operations**
   - New file
   - Open file dialog
   - Save / Save As
   - Modified indicator in title

3. **Editor-Terminal integration**
   - Run File (F5)
   - Run Selection (F9)

### 2.2 Verification Checkpoint

- [ ] Can create new file
- [ ] Can open existing .logo file
- [ ] Line numbers display correctly
- [ ] Current line is highlighted
- [ ] Modified files show asterisk in title
- [ ] F5 runs entire file
- [ ] F9 runs selection or current line
- [ ] Save prompts for filename if new

### 2.3 Key Code: Editor with Line Numbers

```python
# clasp/editor.py

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QFileDialog, QMessageBox
from PyQt6.QtGui import QFont, QPainter, QColor, QTextFormat
from PyQt6.QtCore import Qt, QRect, QSize
from pathlib import Path

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
        """Highlight the current line."""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QPlainTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(self.theme['editor_current_line']))
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
            
        self.setExtraSelections(extra_selections)
        
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
```

---

## Phase 3: Syntax Highlighting & Bracket Matching

**Goal:** Logo-aware editor with visual feedback

### 3.1 Tasks

1. **Logo syntax highlighter**
   - Keywords/primitives
   - Variables (`:varname`)
   - Quoted words (`"word`)
   - Comments (`; comment`)
   - Numbers

2. **Bracket matching**
   - Match `[]` pairs
   - Match `()` pairs
   - Highlight matching bracket

### 3.2 Verification Checkpoint

- [ ] Keywords like `to`, `repeat`, `if` in blue
- [ ] Variables like `:x` in green
- [ ] Comments in gray italic
- [ ] Quoted words in orange
- [ ] Numbers in purple
- [ ] Cursor on `[` highlights matching `]`

### 3.3 Key Code: Highlighter

```python
# clasp/highlighter.py

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression


class LogoHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Logo code."""
    
    PRIMITIVES = [
        # Definitions
        'to', 'end', 'output', 'op', 'stop', 'local', 'localmake', 'make', 'name', 'thing',
        # I/O
        'print', 'pr', 'show', 'type', 'readword', 'readlist', 'readchar',
        # Control
        'if', 'ifelse', 'test', 'iftrue', 'ift', 'iffalse', 'iff',
        'repeat', 'while', 'until', 'for', 'foreach',
        'run', 'runresult', 'apply', 'catch', 'throw',
        # Lists
        'first', 'last', 'butfirst', 'bf', 'butlast', 'bl', 'item',
        'fput', 'lput', 'list', 'sentence', 'se', 'word',
        'count', 'emptyp', 'wordp', 'listp', 'numberp', 'memberp',
        # Math
        'sum', 'difference', 'product', 'quotient', 'remainder', 'modulo',
        'int', 'round', 'sqrt', 'power', 'sin', 'cos', 'tan', 'arctan',
        'random', 'rerandom',
        # Logic
        'and', 'or', 'not', 'equalp', 'lessp', 'greaterp',
        # Turtle
        'forward', 'fd', 'back', 'bk', 'right', 'rt', 'left', 'lt',
        'penup', 'pu', 'pendown', 'pd', 'home', 'clearscreen', 'cs', 'clean',
        'hideturtle', 'ht', 'showturtle', 'st',
        'setpos', 'setxy', 'setx', 'sety', 'setheading', 'seth',
        'setpencolor', 'setpc', 'setpensize', 'setbackground', 'setbg',
        'pos', 'xcor', 'ycor', 'heading', 'towards',
        # Workspace
        'load', 'save', 'edit', 'ed', 'bye',
    ]
    
    def __init__(self, document, theme):
        super().__init__(document)
        self.theme = theme
        self.rules = []
        self._build_rules()
        
    def _build_rules(self):
        # Keywords
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor(self.theme['syntax_keyword']))
        keyword_fmt.setFontWeight(QFont.Weight.Bold)
        
        for word in self.PRIMITIVES:
            pattern = QRegularExpression(
                rf'\b{word}\b',
                QRegularExpression.PatternOption.CaseInsensitiveOption
            )
            self.rules.append((pattern, keyword_fmt))
        
        # Variables
        var_fmt = QTextCharFormat()
        var_fmt.setForeground(QColor(self.theme['syntax_variable']))
        self.rules.append((
            QRegularExpression(r':[a-zA-Z_][a-zA-Z0-9_]*'),
            var_fmt
        ))
        
        # Quoted words
        quoted_fmt = QTextCharFormat()
        quoted_fmt.setForeground(QColor(self.theme['syntax_string']))
        self.rules.append((
            QRegularExpression(r'"[^\s\[\]()]+'),
            quoted_fmt
        ))
        
        # Numbers
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor(self.theme['syntax_number']))
        self.rules.append((
            QRegularExpression(r'\b-?[0-9]+\.?[0-9]*\b'),
            num_fmt
        ))
        
        # Comments
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor(self.theme['syntax_comment']))
        comment_fmt.setFontItalic(True)
        self.rules.append((
            QRegularExpression(r';[^\n]*'),
            comment_fmt
        ))
        
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
```

---

## Phase 4: Turtle Graphics

**Goal:** Integrated turtle graphics using Python's turtle module

### 4.1 Tasks

1. **Graphics manager**
   - Initialize turtle window
   - Map Logo commands to turtle
   - Handle window lifecycle

2. **PyLogo-turtle bridge**
   - Connect interpreter graphics calls to turtle
   - Coordinate updates

3. **View menu integration**
   - Show/hide graphics window
   - Clear graphics command

### 4.2 Verification Checkpoint

- [ ] Graphics window opens from View menu
- [ ] `forward 100` draws a line
- [ ] `right 90` turns turtle
- [ ] `repeat 4 [forward 50 right 90]` draws square
- [ ] `clearscreen` clears and resets
- [ ] `hideturtle` / `showturtle` work

### 4.3 Key Code: Graphics Manager

```python
# clasp/graphics.py

import turtle


class TurtleGraphicsManager:
    """Manages turtle graphics window."""
    
    def __init__(self):
        self.screen = None
        self.t = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize turtle graphics."""
        if self.is_initialized:
            return
            
        # Setup screen
        self.screen = turtle.Screen()
        self.screen.title("CLASP Graphics")
        self.screen.setup(600, 600)
        self.screen.bgcolor("white")
        
        # Setup turtle
        self.t = turtle.Turtle()
        self.t.speed(0)  # Fastest
        self.t.shape("turtle")
        
        self.is_initialized = True
        
    def _ensure_init(self):
        if not self.is_initialized:
            self.initialize()
            
    # Turtle commands
    def forward(self, distance):
        self._ensure_init()
        self.t.forward(distance)
        
    def fd(self, distance):
        self.forward(distance)
        
    def back(self, distance):
        self._ensure_init()
        self.t.back(distance)
        
    def bk(self, distance):
        self.back(distance)
        
    def right(self, angle):
        self._ensure_init()
        self.t.right(angle)
        
    def rt(self, angle):
        self.right(angle)
        
    def left(self, angle):
        self._ensure_init()
        self.t.left(angle)
        
    def lt(self, angle):
        self.left(angle)
        
    def penup(self):
        self._ensure_init()
        self.t.penup()
        
    def pu(self):
        self.penup()
        
    def pendown(self):
        self._ensure_init()
        self.t.pendown()
        
    def pd(self):
        self.pendown()
        
    def home(self):
        self._ensure_init()
        self.t.home()
        
    def clearscreen(self):
        self._ensure_init()
        self.t.clear()
        self.t.home()
        self.t.pendown()
        
    def cs(self):
        self.clearscreen()
        
    def hideturtle(self):
        self._ensure_init()
        self.t.hideturtle()
        
    def ht(self):
        self.hideturtle()
        
    def showturtle(self):
        self._ensure_init()
        self.t.showturtle()
        
    def st(self):
        self.showturtle()
        
    def setpencolor(self, *args):
        self._ensure_init()
        if len(args) == 1:
            self.t.pencolor(args[0])
        elif len(args) == 3:
            self.t.pencolor(args[0], args[1], args[2])
            
    def setpc(self, *args):
        self.setpencolor(*args)
        
    def setpensize(self, size):
        self._ensure_init()
        self.t.pensize(size)
        
    def setpos(self, x, y):
        self._ensure_init()
        self.t.setpos(x, y)
        
    def setxy(self, x, y):
        self.setpos(x, y)
        
    def setheading(self, angle):
        self._ensure_init()
        self.t.setheading(angle)
        
    def seth(self, angle):
        self.setheading(angle)
        
    def pos(self):
        self._ensure_init()
        return list(self.t.pos())
        
    def xcor(self):
        self._ensure_init()
        return self.t.xcor()
        
    def ycor(self):
        self._ensure_init()
        return self.t.ycor()
        
    def heading(self):
        self._ensure_init()
        return self.t.heading()
        
    def close(self):
        """Close graphics window."""
        if self.screen:
            try:
                self.screen.bye()
            except turtle.Terminator:
                pass
            self.is_initialized = False
            self.screen = None
            self.t = None
```

---

## Phase 5: Polish & Configuration

**Goal:** Production-ready application

### 5.1 Tasks

1. **Configuration system**
   - Load/save JSON config
   - Remember window state

2. **Session management**
   - Recent files list
   - Restore open files

3. **Keyboard shortcuts**
   - All standard shortcuts working

4. **Error handling**
   - Graceful error display
   - Recovery from graphics crashes

5. **Final theming**
   - Consistent appearance throughout

### 5.2 Verification Checkpoint

- [ ] Settings persist between sessions
- [ ] Recent files menu populated
- [ ] All shortcuts work
- [ ] Errors display gracefully
- [ ] Application looks polished

### 5.3 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New File | Ctrl+N |
| Open File | Ctrl+O |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Quit | Ctrl+Q |
| Run File | F5 |
| Run Selection | F9 |
| Graphics Window | Ctrl+G |
| Find | Ctrl+F |

---

## Testing Logo Code

```logo
; Test 1: Basic output
print "Hello
print [Hello World]

; Test 2: Variables
make "x 10
print :x

; Test 3: Arithmetic
print sum 2 3
print product 4 5

; Test 4: Procedure
to square :size
  repeat 4 [forward :size right 90]
end
square 50

; Test 5: Recursion (non-graphics)
to factorial :n
  if :n = 0 [output 1]
  output :n * factorial :n - 1
end
print factorial 5

; Test 6: List operations
print first [a b c]
print butfirst [a b c]
print fput "x [a b c]

; Test 7: Spiral (graphics)
to spiral :size :angle
  if :size > 100 [stop]
  forward :size
  right :angle
  spiral :size + 2 :angle
end
spiral 1 91
```

---

## Dependencies

### requirements.txt

```
PyQt6>=6.4.0
pylogo>=0.5.0
```

### Installation

```bash
pip install -r requirements.txt
```

No external interpreters needed—everything is pure Python.
