# CLASP Technical Specification

**Version:** 1.1  
**Date:** December 2024

---

## 1. System Architecture

### 1.1 High-Level Design

CLASP uses a pure-Python architecture with PyLogo as the interpreter and Python's turtle module for graphics. This eliminates subprocess management complexity and provides cross-platform compatibility out of the box.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLASP Main Window                           │
│  ┌──────────────┬────────────────────────┬───────────────────────┐  │
│  │              │                        │                       │  │
│  │    File      │      Code Editor       │     REPL Terminal     │  │
│  │   Browser    │                        │                       │  │
│  │              │   - Syntax highlight   │   - PyLogo interpreter│  │
│  │   - Tree     │   - Bracket matching   │   - In-process exec   │  │
│  │   - CRUD     │   - Line numbers       │   - Output capture    │  │
│  │              │   - Logo awareness     │                       │  │
│  │              │                        │                       │  │
│  └──────────────┴────────────────────────┴───────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   Turtle Graphics Window  │
                  │   (Python turtle module)  │
                  └───────────────────────────┘
```

### 1.2 Component Overview

| Component | Responsibility | Technology |
|-----------|----------------|------------|
| Main Window | Layout, menu, coordination | PyQt6 QMainWindow |
| File Browser | Project navigation, file ops | QTreeView + QFileSystemModel |
| Code Editor | Logo editing with syntax support | QPlainTextEdit + QSyntaxHighlighter |
| REPL Terminal | Interactive Logo session | QPlainTextEdit + PyLogo |
| Graphics Window | Turtle graphics display | Python turtle module |
| Logo Interpreter | Execute Logo code | PyLogo |
| Config Manager | User preferences persistence | JSON files |

### 1.3 Why This Architecture

**Previous approach (UCBLogo wrapper):**
- Required PTY subprocess management
- Complex I/O handling
- Graphics interception challenges
- Platform-specific PTY code

**Current approach (PyLogo + turtle):**
- Pure Python, no subprocesses
- In-process interpreter calls
- Native turtle graphics
- Cross-platform from day one
- Faster development cycle

---

## 2. PyLogo Integration

### 2.1 About PyLogo

PyLogo is a Logo interpreter written in Python. It provides:
- Standard Logo primitives
- Procedure definitions
- List operations
- Variable scoping
- Turtle graphics integration

**Installation:**
```bash
pip install pylogo
```

### 2.2 Interpreter Integration

The REPL executes Logo code by passing it to PyLogo:

```python
from pylogo import Logo

class LogoInterpreter:
    """Wrapper around PyLogo for REPL integration."""
    
    def __init__(self):
        self.logo = Logo()
        self.output_buffer = []
        
    def execute(self, code):
        """Execute Logo code and capture output."""
        try:
            # Redirect print output
            result = self.logo.execute(code)
            return {
                'success': True,
                'output': result,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'output': None,
                'error': str(e)
            }
    
    def reset(self):
        """Reset interpreter state."""
        self.logo = Logo()
```

### 2.3 Output Capture

PyLogo's print statements need to be captured and redirected to the REPL terminal:

```python
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

class LogoInterpreter:
    def execute(self, code):
        """Execute with output capture."""
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
```

---

## 3. Turtle Graphics Integration

### 3.1 Python turtle Module

Python's built-in `turtle` module provides:
- Full turtle graphics primitives
- Cross-platform rendering
- Standalone window management
- Well-documented API

### 3.2 Connecting PyLogo to turtle

PyLogo can be configured to use Python's turtle module for graphics commands:

```python
import turtle

class TurtleGraphicsManager:
    """Manages turtle graphics window."""
    
    def __init__(self):
        self.screen = None
        self.turtle = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize turtle graphics window."""
        if self.is_initialized:
            return
            
        self.screen = turtle.Screen()
        self.screen.title("CLASP Graphics")
        self.screen.setup(600, 600)
        self.screen.bgcolor("white")
        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)  # Fastest
        self.is_initialized = True
        
    def forward(self, distance):
        self._ensure_initialized()
        self.turtle.forward(distance)
        
    def right(self, angle):
        self._ensure_initialized()
        self.turtle.right(angle)
        
    def left(self, angle):
        self._ensure_initialized()
        self.turtle.left(angle)
        
    def penup(self):
        self._ensure_initialized()
        self.turtle.penup()
        
    def pendown(self):
        self._ensure_initialized()
        self.turtle.pendown()
        
    def home(self):
        self._ensure_initialized()
        self.turtle.home()
        
    def clear(self):
        self._ensure_initialized()
        self.turtle.clear()
        self.turtle.home()
        
    def hideturtle(self):
        self._ensure_initialized()
        self.turtle.hideturtle()
        
    def showturtle(self):
        self._ensure_initialized()
        self.turtle.showturtle()
        
    def setpencolor(self, color):
        self._ensure_initialized()
        self.turtle.pencolor(color)
        
    def setpensize(self, size):
        self._ensure_initialized()
        self.turtle.pensize(size)
        
    def _ensure_initialized(self):
        if not self.is_initialized:
            self.initialize()
            
    def close(self):
        """Close graphics window."""
        if self.screen:
            try:
                self.screen.bye()
            except:
                pass
            self.is_initialized = False
```

### 3.3 Turtle + PyQt6 Coordination

The turtle module uses tkinter internally. To avoid conflicts with PyQt6:

**Option A: Separate Windows**
- Let turtle manage its own window
- PyQt6 manages the IDE
- Simple, minimal coordination needed

**Option B: Embed turtle canvas** (more complex)
- Use `turtle.RawTurtle` with a tkinter canvas
- Embed tkinter in PyQt6 (possible but messy)
- Not recommended

**Recommendation:** Use Option A. The turtle window floats separately, which matches the original design intent anyway.

### 3.4 Managing the turtle Event Loop

turtle uses tkinter's mainloop. With PyQt6 also running an event loop, we need coordination:

```python
import turtle

# Don't let turtle start its own mainloop
turtle.tracer(0)  # Turn off animation

# After drawing commands, update manually
turtle.update()

# Or use turtle.done() only when closing
```

Alternative using `turtle.RawTurtle` for more control:

```python
import tkinter as tk
import turtle

class TurtleManager:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.screen = None
        self.t = None
        
    def create_window(self):
        self.root = tk.Tk()
        self.root.title("CLASP Graphics")
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.screen)
        
    def process_events(self):
        """Call periodically from PyQt6 to process tkinter events."""
        if self.root:
            self.root.update_idletasks()
            self.root.update()
```

---

## 4. Code Editor

### 4.1 Logo Syntax Highlighting

Logo syntax elements to highlight:

| Element | Examples | Suggested Color |
|---------|----------|-----------------|
| Primitives | `print`, `make`, `if`, `repeat`, `to`, `end` | Blue |
| Operators | `+`, `-`, `*`, `/`, `=`, `<`, `>` | Amber |
| Variables | `:varname` (colon prefix) | Green |
| Quoted Words | `"hello` | Orange |
| Lists | `[item1 item2]` | Default (brackets highlighted) |
| Comments | `; comment text` | Gray/Italic |
| Numbers | `42`, `3.14` | Purple |
| Procedure Defs | `to procname` | Bold Blue |

### 4.2 Highlighter Implementation

```python
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class LogoHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Logo code."""
    
    def __init__(self, document, theme):
        super().__init__(document)
        self.theme = theme
        self.rules = []
        self._build_rules()
        
    def _build_rules(self):
        # Primitives
        primitives = [
            'to', 'end', 'output', 'op', 'stop', 'local', 'localmake',
            'make', 'name', 'thing',
            'print', 'pr', 'show', 'type', 'readword', 'readlist',
            'if', 'ifelse', 'test', 'iftrue', 'ift', 'iffalse', 'iff',
            'repeat', 'while', 'until', 'for', 'foreach',
            'first', 'last', 'butfirst', 'bf', 'butlast', 'bl',
            'item', 'fput', 'lput', 'list', 'sentence', 'se', 'word',
            'count', 'emptyp', 'wordp', 'listp', 'numberp', 'memberp',
            'sum', 'difference', 'product', 'quotient', 'remainder',
            'and', 'or', 'not', 'equalp', 'lessp', 'greaterp',
            'forward', 'fd', 'back', 'bk', 'right', 'rt', 'left', 'lt',
            'penup', 'pu', 'pendown', 'pd', 'home', 'clearscreen', 'cs',
            'hideturtle', 'ht', 'showturtle', 'st',
            'setpencolor', 'setpc', 'setpensize',
            'run', 'load', 'save', 'bye',
        ]
        
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor(self.theme['syntax_keyword']))
        keyword_fmt.setFontWeight(QFont.Weight.Bold)
        
        for word in primitives:
            pattern = QRegularExpression(
                rf'\b{word}\b',
                QRegularExpression.PatternOption.CaseInsensitiveOption
            )
            self.rules.append((pattern, keyword_fmt))
        
        # Variables (:varname)
        var_fmt = QTextCharFormat()
        var_fmt.setForeground(QColor(self.theme['syntax_variable']))
        self.rules.append((
            QRegularExpression(r':[a-zA-Z_][a-zA-Z0-9_]*'),
            var_fmt
        ))
        
        # Quoted words ("word)
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

### 4.3 Bracket Matching

```python
def highlight_matching_bracket(self, cursor_position):
    """Find and highlight the matching bracket."""
    text = self.toPlainText()
    
    if cursor_position >= len(text):
        return None
    
    char = text[cursor_position]
    brackets = {'[': ']', ']': '[', '(': ')', ')': '('}
    
    if char not in brackets:
        return None
    
    # Determine search direction
    if char in '[(':
        direction = 1
        target = brackets[char]
    else:
        direction = -1
        target = brackets[char]
    
    # Search for match
    depth = 1
    pos = cursor_position + direction
    
    while 0 <= pos < len(text) and depth > 0:
        if text[pos] == char:
            depth += 1
        elif text[pos] == target:
            depth -= 1
        if depth > 0:
            pos += direction
    
    if depth == 0:
        return pos
    return None
```

---

## 5. REPL Terminal

### 5.1 Terminal Widget

```python
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtCore import Qt, pyqtSignal

class LogoTerminal(QPlainTextEdit):
    """Terminal widget for Logo REPL."""
    
    command_entered = pyqtSignal(str)
    
    def __init__(self, interpreter):
        super().__init__()
        self.interpreter = interpreter
        self.prompt = "? "
        self.prompt_position = 0
        self.history = []
        self.history_index = 0
        
        # Appearance
        self.setFont(QFont("Monospace", 11))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        # Show initial prompt
        self.show_prompt()
        
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
        result = self.interpreter.execute(command)
        
        if result['stdout']:
            self.appendPlainText(result['stdout'].rstrip())
            
        if not result['success']:
            self.appendPlainText(f"Error: {result['stderr']}")
            
        self.show_prompt()
        
    def append_output(self, text):
        """Append output text (for use by interpreter callbacks)."""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
```

---

## 6. File Browser

### 6.1 Implementation

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from pathlib import Path
import os

class LogoFileBrowser(QWidget):
    """File browser for Logo project navigation."""
    
    file_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.path_label = QLabel()
        self.path_label.setStyleSheet("padding: 4px;")
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
        
        self.tree.doubleClicked.connect(self._on_double_click)
        layout.addWidget(self.tree)
        
        # Set initial directory
        self.set_root(str(Path.home()))
        
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
```

---

## 7. Configuration System

### 7.1 Config Location

```
~/.config/clasp/
├── config.json        # User preferences
├── recent.json        # Recent files
└── session.json       # Window state
```

### 7.2 Configuration Schema

```json
{
  "editor": {
    "font_family": "Monospace",
    "font_size": 12,
    "tab_width": 2,
    "show_line_numbers": true,
    "highlight_current_line": true,
    "word_wrap": false
  },
  "terminal": {
    "font_family": "Monospace",
    "font_size": 11,
    "scrollback_lines": 10000
  },
  "graphics": {
    "window_width": 600,
    "window_height": 600,
    "background_color": "#FFFFFF",
    "auto_open": false
  },
  "theme": {
    "name": "amber-blue"
  },
  "file_browser": {
    "show_hidden": false,
    "default_directory": "~"
  }
}
```

### 7.3 Config Manager

```python
import json
from pathlib import Path

class ConfigManager:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        "editor": {
            "font_family": "Monospace",
            "font_size": 12,
            "tab_width": 2,
            "show_line_numbers": True,
            "highlight_current_line": True
        },
        "terminal": {
            "font_family": "Monospace",
            "font_size": 11
        },
        "graphics": {
            "window_width": 600,
            "window_height": 600,
            "auto_open": False
        },
        "theme": {
            "name": "amber-blue"
        }
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "clasp"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load()
        
    def _load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    return self._merge(self.DEFAULT_CONFIG, loaded)
            except (json.JSONDecodeError, IOError):
                pass
        return self.DEFAULT_CONFIG.copy()
    
    def _merge(self, default, loaded):
        """Merge loaded config with defaults."""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict):
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def save(self):
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def get(self, *keys):
        """Get nested config value."""
        value = self.config
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value
    
    def set(self, *keys_and_value):
        """Set nested config value."""
        *keys, value = keys_and_value
        target = self.config
        for key in keys[:-1]:
            target = target.setdefault(key, {})
        target[keys[-1]] = value
```

---

## 8. Theme System

### 8.1 Amber/Blue Theme (Default)

```python
AMBER_BLUE_THEME = {
    'name': 'amber-blue',
    
    # Base colors
    'background': '#1a1a2e',
    'foreground': '#d4a556',
    'accent': '#2874A6',
    
    # Editor
    'editor_bg': '#1a1a2e',
    'editor_fg': '#d4a556',
    'editor_selection': '#3d3d5c',
    'editor_current_line': '#252542',
    'line_numbers_bg': '#16162a',
    'line_numbers_fg': '#5a5a7a',
    
    # Syntax highlighting
    'syntax_keyword': '#2874A6',
    'syntax_variable': '#27AE60',
    'syntax_string': '#E67E22',
    'syntax_comment': '#7F8C8D',
    'syntax_number': '#8E44AD',
    
    # Terminal
    'terminal_bg': '#1a1a2e',
    'terminal_fg': '#d4a556',
    
    # Graphics
    'graphics_bg': '#FFFFFF',
    'turtle_color': '#2874A6',
}
```

---

## 9. Dependencies

### 9.1 Python Packages

```
PyQt6>=6.4.0
pylogo>=0.5.0
```

### 9.2 System Requirements

- Python 3.10+
- No external interpreters required (PyLogo is pure Python)
- Works on Linux, macOS, Windows

---

## 10. Error Handling

| Condition | Detection | Response |
|-----------|-----------|----------|
| PyLogo import failure | ImportError | Show installation instructions |
| Logo syntax error | PyLogo exception | Display error in terminal |
| File read error | IOError | Show error dialog |
| File write error | IOError | Show error, keep buffer |
| Invalid config JSON | JSONDecodeError | Use defaults, log warning |
| Turtle window closed | TclError | Reinitialize on next graphics command |
