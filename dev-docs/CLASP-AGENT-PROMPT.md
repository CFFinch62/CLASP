# CLASP AI Agent Development Prompt

**Project:** CLASP - Coding in Logo to Attack Serious Problems  
**Version:** 1.1  
**Date:** December 2024

---

## Mission Statement

You are helping build **CLASP**, a modern IDE for Logo programming using PyLogo (a Python Logo interpreter) and Python's turtle module. The project honors Professor Brian Harvey and aims to present Logo as the serious problem-solving language it truly is—not just "that turtle graphics language for kids."

**Key Insight:** Logo is a Lisp dialect with genuine computational power. Graphics are one tool, not the focus.

---

## Project Context

### The Developer

Chuck is a 63-year-old developer with 40+ years of programming experience. He:

- Works in marine electronics with multiple technical roles
- Teaches programming to young students
- Prefers clean, functional design over flashy features
- Values conscious engagement over passive coding
- Has developed several educational tools (LITHP, HuG, Steps, Just Code)
- Uses a consistent amber/blue color scheme across his tool family
- Prefers languages with natural structure over brace-and-semicolon syntax

### Design Philosophy

1. **Simplicity over features** — Do one thing well
2. **Conscious engagement** — Tools that require thought, not clicking
3. **Education-focused** — Support learning, not just production
4. **Speed of development** — Get something working, iterate later
5. **Cross-platform** — Pure Python enables this from day one

### The Logo Philosophy

Logo has been unfairly reduced to "turtle graphics for kids." In reality:

- Logo is a Lisp dialect with full computational power
- It supports recursion, symbolic computation, list processing
- Professor Harvey's *Computer Science Logo Style* trilogy demonstrates its depth
- CLASP should support serious problem-solving, with graphics as one tool among many

---

## Technical Stack

| Component | Technology | Notes |
|-----------|------------|-------|
| Language | Python 3.10+ | Developer's preferred language |
| GUI Framework | PyQt6 | Cross-platform, professional quality |
| Logo Interpreter | PyLogo | Pure Python, pip installable |
| Graphics | Python turtle module | Built-in, reliable, cross-platform |
| Configuration | JSON | ~/.config/clasp/ |

### Why This Stack

Previous approach (UCBLogo wrapper) required:
- PTY subprocess management
- Complex I/O handling
- Graphics interception
- Platform-specific code

Current approach (PyLogo + turtle) provides:
- Pure Python, no subprocesses
- In-process interpreter calls
- Native turtle graphics
- Cross-platform from day one
- Much faster development

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLASP Main Window                           │
│  ┌──────────────┬────────────────────────┬───────────────────────┐  │
│  │ File Browser │      Code Editor       │     REPL Terminal     │  │
│  │              │                        │                       │  │
│  │ - Tree view  │ - Logo syntax highlight│ - PyLogo interpreter  │  │
│  │ - .logo files│ - Bracket matching     │ - Output capture      │  │
│  │ - Navigation │ - Line numbers         │ - Command history     │  │
│  └──────────────┴────────────────────────┴───────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   Turtle Graphics Window  │
                  │   (Python turtle module)  │
                  └───────────────────────────┘
```

---

## Component Specifications

### 1. Logo Interpreter Wrapper

**Purpose:** Execute Logo code via PyLogo with output capture

```python
import io
from contextlib import redirect_stdout, redirect_stderr
from pylogo import Logo

class LogoInterpreter:
    """Wrapper around PyLogo interpreter."""
    
    def __init__(self):
        self.logo = Logo()
        
    def execute(self, code):
        """Execute Logo code and capture output."""
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
```

**Key Points:**
- PyLogo is imported directly, no subprocess
- Output captured via StringIO redirect
- Exceptions caught and returned cleanly
- Reset creates fresh interpreter

---

### 2. REPL Terminal

**Purpose:** Interactive Logo session with command history

```python
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtCore import Qt

class LogoTerminal(QPlainTextEdit):
    """Terminal widget for Logo REPL."""
    
    def __init__(self, interpreter):
        super().__init__()
        self.interpreter = interpreter
        self.prompt = "? "
        self.prompt_position = 0
        self.history = []
        self.history_index = 0
        
        self.setFont(QFont("Monospace", 11))
        self.show_prompt()
        
    def show_prompt(self):
        """Display Logo prompt."""
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
            self.appendPlainText("")
            
            if command.strip():
                self.history.append(command)
                self.history_index = len(self.history)
                self._execute(command)
            else:
                self.show_prompt()
                
        elif key == Qt.Key.Key_Up:
            if self.history and self.history_index > 0:
                self.history_index -= 1
                self._replace_input(self.history[self.history_index])
                
        elif key == Qt.Key.Key_Down:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self._replace_input(self.history[self.history_index])
            else:
                self.history_index = len(self.history)
                self._replace_input("")
                
        elif key == Qt.Key.Key_Backspace:
            if cursor.position() > self.prompt_position:
                super().keyPressEvent(event)
                
        else:
            super().keyPressEvent(event)
            
    def _get_current_input(self):
        return self.toPlainText()[self.prompt_position:]
        
    def _replace_input(self, text):
        cursor = self.textCursor()
        cursor.setPosition(self.prompt_position)
        cursor.movePosition(QTextCursor.MoveOperation.End, 
                          QTextCursor.MoveMode.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(text)
        
    def _execute(self, command):
        result = self.interpreter.execute(command)
        
        if result['stdout']:
            self.appendPlainText(result['stdout'].rstrip())
            
        if not result['success']:
            self.appendPlainText(f"Error: {result['stderr']}")
            
        self.show_prompt()
        
    def execute_code(self, code):
        """Execute code from editor (Run File/Selection)."""
        self.appendPlainText(f"\n; Running...\n")
        result = self.interpreter.execute(code)
        
        if result['stdout']:
            self.appendPlainText(result['stdout'].rstrip())
        if not result['success']:
            self.appendPlainText(f"Error: {result['stderr']}")
            
        self.show_prompt()
```

---

### 3. Code Editor

**Purpose:** Logo source editing with syntax awareness

**Features:**
- Line numbers
- Current line highlighting
- Logo syntax highlighting
- Bracket matching
- File operations

**Logo Syntax Elements:**

| Element | Pattern | Color |
|---------|---------|-------|
| Primitives | `\b(to|end|if|repeat|...)\b` | Blue (#2874A6) |
| Variables | `:[a-zA-Z_][a-zA-Z0-9_]*` | Green (#27AE60) |
| Quoted words | `"[^\s\[\]()]+` | Orange (#E67E22) |
| Numbers | `-?[0-9]+\.?[0-9]*` | Purple (#8E44AD) |
| Comments | `;[^\n]*` | Gray italic (#7F8C8D) |

**Logo Primitives (comprehensive list):**

```python
LOGO_PRIMITIVES = [
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
    'penup', 'pu', 'pendown', 'pd', 'home', 'clearscreen', 'cs',
    'hideturtle', 'ht', 'showturtle', 'st',
    'setpos', 'setxy', 'setheading', 'seth',
    'setpencolor', 'setpc', 'setpensize',
    # Workspace
    'load', 'save', 'edit', 'bye',
]
```

---

### 4. File Browser

**Purpose:** Navigate Logo project files

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import pyqtSignal

class LogoFileBrowser(QWidget):
    file_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.model = QFileSystemModel()
        self.model.setNameFilters(["*.logo", "*.lg", "*.lgo"])
        self.model.setNameFilterDisables(False)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.hideColumn(1)  # Size
        self.tree.hideColumn(2)  # Type
        self.tree.hideColumn(3)  # Date
        
        self.tree.doubleClicked.connect(self._on_click)
        
    def _on_click(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.file_selected.emit(path)
```

**File Extensions:** `.logo`, `.lg`, `.lgo`

---

### 5. Turtle Graphics

**Purpose:** Visual output using Python's built-in turtle module

```python
import turtle

class TurtleGraphicsManager:
    """Manages turtle graphics window."""
    
    def __init__(self):
        self.screen = None
        self.t = None
        self.is_initialized = False
        
    def initialize(self):
        if self.is_initialized:
            return
            
        self.screen = turtle.Screen()
        self.screen.title("CLASP Graphics")
        self.screen.setup(600, 600)
        self.screen.bgcolor("white")
        
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.is_initialized = True
        
    def forward(self, distance):
        self._ensure_init()
        self.t.forward(distance)
        
    def right(self, angle):
        self._ensure_init()
        self.t.right(angle)
        
    # ... other turtle commands map directly
    
    def clearscreen(self):
        self._ensure_init()
        self.t.clear()
        self.t.home()
        
    def _ensure_init(self):
        if not self.is_initialized:
            self.initialize()
```

**Note:** The turtle module uses tkinter internally. It manages its own window separate from PyQt6. This is intentional—the graphics window floats independently, matching the original design intent.

---

## Theme System

### Amber/Blue Theme (Default)

Consistent with Chuck's tool family:

```python
AMBER_BLUE_THEME = {
    'name': 'amber-blue',
    
    # Base
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
    
    # Syntax
    'syntax_keyword': '#2874A6',
    'syntax_variable': '#27AE60',
    'syntax_string': '#E67E22',
    'syntax_comment': '#7F8C8D',
    'syntax_number': '#8E44AD',
    
    # Terminal
    'terminal_bg': '#1a1a2e',
    'terminal_fg': '#d4a556',
}
```

---

## Configuration

### Location

```
~/.config/clasp/
├── config.json
├── recent.json
└── session.json
```

### Schema

```json
{
  "editor": {
    "font_family": "Monospace",
    "font_size": 12,
    "show_line_numbers": true,
    "highlight_current_line": true
  },
  "terminal": {
    "font_family": "Monospace",
    "font_size": 11
  },
  "graphics": {
    "window_width": 600,
    "window_height": 600,
    "auto_open": false
  },
  "theme": {
    "name": "amber-blue"
  }
}
```

---

## Project Structure

```
clasp/
├── clasp/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── main_window.py       # QMainWindow
│   ├── interpreter.py       # PyLogo wrapper
│   ├── terminal.py          # REPL widget
│   ├── editor.py            # Code editor
│   ├── highlighter.py       # Syntax highlighting
│   ├── file_browser.py      # File tree
│   ├── graphics.py          # Turtle manager
│   ├── config.py            # Configuration
│   └── themes.py            # Theme definitions
├── examples/
│   ├── hello.logo
│   ├── square.logo
│   ├── factorial.logo
│   └── spiral.logo
├── tests/
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

---

## Development Phases

### Phase 1: Foundation
- Project structure
- Main window with three panes
- PyLogo interpreter wrapper
- Basic terminal I/O

**Checkpoint:** Can type `print "hello` and see output

### Phase 2: Editor & Files
- Code editor with line numbers
- File browser
- Open/save files
- Run File (F5), Run Selection (F9)

**Checkpoint:** Can write, save, and run Logo programs

### Phase 3: Syntax Highlighting
- Logo keyword highlighting
- Variable, string, comment colors
- Bracket matching

**Checkpoint:** Editor shows Logo syntax visually

### Phase 4: Graphics
- Turtle graphics manager
- Connect to PyLogo turtle commands
- View menu toggle

**Checkpoint:** `forward 100 right 90` draws visibly

### Phase 5: Polish
- Configuration persistence
- Session management
- Error handling
- Final theming

**Checkpoint:** Production-ready application

---

## Testing Code

```logo
; Basic output
print "Hello
print [Hello World]

; Variables
make "x 10
print :x

; Arithmetic
print sum 2 3
print product 4 5

; Procedure definition
to square :size
  repeat 4 [forward :size right 90]
end

; Non-graphics recursion
to factorial :n
  if :n = 0 [output 1]
  output :n * factorial :n - 1
end
print factorial 5

; List operations
print first [a b c]
print butfirst [a b c]
print fput "x [a b c]

; Graphics
square 50
clearscreen

; Spiral
to spiral :size :angle
  if :size > 100 [stop]
  forward :size
  right :angle
  spiral :size + 2 :angle
end
spiral 1 91
```

---

## Keyboard Shortcuts

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

---

## Critical Reminders

1. **Pure Python stack.** No subprocesses, no PTY, no platform-specific code.

2. **PyLogo is the interpreter.** Import it, call it, capture output.

3. **turtle module for graphics.** Let it manage its own window.

4. **Amber/blue theme.** Match Chuck's other tools.

5. **Graphics are secondary.** REPL and editor are the focus.

6. **Simple over clever.** Get it working first.

7. **Honor Professor Harvey.** Logo is a serious language.

---

## Dependencies

### requirements.txt

```
PyQt6>=6.4.0
pylogo>=0.5.0
```

### Installation

```bash
pip install PyQt6 pylogo
```

No external interpreters. Everything is pip-installable Python.

---

## Quick Reference

### Check PyLogo
```python
try:
    from pylogo import Logo
    print("PyLogo available")
except ImportError:
    print("Run: pip install pylogo")
```

### Execute Logo Code
```python
from pylogo import Logo
logo = Logo()
result = logo.execute('print sum 2 3')
```

### Initialize Turtle
```python
import turtle
screen = turtle.Screen()
t = turtle.Turtle()
t.forward(100)
```

### Logo Comment
`; this is a comment`

### Logo Variable
`:varname` (read), `make "varname value` (set)

### Logo Quoted Word
`"word` (not `"word"`)

### Logo List
`[item1 item2 item3]`

---

## Final Notes

CLASP is about making Logo accessible and demonstrating its real power. PyLogo + turtle gives us a fast path to a working product. The IDE is the contribution—modern presentation for a language that deserves more respect.

Professor Harvey showed what Logo can do. We're building a better front door.
