# CLASP User Guide

**CLASP** (Coding in Logo to Attack Serious Problems) is a modern IDE for the Logo programming language, built with Python and PyQt6. It provides a rich environment for learning and experimenting with Logo, featuring a syntax-highlighting editor, an interactive terminal, and integrated turtle graphics.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### dependencies
CLASP relies on `PyLogo` and `PyQt6`.

1. Install the required packages:
   ```bash
   pip install pylogo PyQt6
   ```

2. Clone or download the CLASP repository.

3. Run CLASP:
   ```bash
   python3 -m clasp.main
   ```

## Getting Started

When you launch CLASP, you will see the main window divided into three sections:
- **Left Panel**: File Browser
- **Top Right Panel**: Code Editor
- **Bottom Right Panel**: Interactive Terminal

### The Code Editor
The editor is where you write your Logo programs. It supports:
- **Syntax Highlighting**: Keywords, comments, and strings are colored for readability.
- **Line Numbers**: displayed on the left margin.
- **Bracket Matching**: Highlights matching parentheses and brackets.

**Key Shortcuts:**
- `Ctrl+N`: New File
- `Ctrl+O`: Open File
- `Ctrl+S`: Save File
- `Ctrl+Shift+S`: Save As
- `F5`: Run current file
- `F9`: Run selected text (or current line)

### The Terminal
The terminal provides a REPL (Read-Eval-Print Loop) for executing Logo commands immediately. You can type commands like `print "Hello` or `forward 100` and see the results instantly.

**Commands:**
- `clear`: Clears the terminal output.
- `reset`: Resets the interpreter state (clears variables and functions).

### Turtle Graphics
CLASP includes a built-in turtle graphics window.

- **Toggle Window**: Go to `View > Graphics Window` or press `Ctrl+G` to show/hide the turtle window.
- **Drawing**: Use standard turtle commands to draw.
  ```logo
  forward 100
  right 90
  forward 100
  ```

## Logo Language Reference

CLASP uses `PyLogo` as its interpreter. It supports standard UCBLogo-style syntax.

### Basic Commands
- `print "word`: Print a word.
- `print [list of words]`: Print a list.
- `make "variable 10`: Set a variable.
- `print :variable`: Access a variable.

### Control Structures
- `repeat 4 [fd 100 rt 90]`: Repeat loop.
- `if :x > 10 [print "Big]`: Conditional.

### Functions
Define functions using `to` ... `end`:
```logo
to square :size
  repeat 4 [forward :size right 90]
end

square 50
```

## Troubleshooting

### Interpreter Not Found
If you see a "Interpreter not available" message, ensure `pylogo` is installed correctly (`pip install pylogo`).

### Graphics Window Issues
If the graphics window becomes unresponsive, try closing it via `Ctrl+G` and re-opening it. Note that using the interpreter `reset` command explicitly clears the turtle state.

### Startup Errors
If CLASP fails to start, check the console output for error messages. Common issues include missing dependencies (`PyQt6`).
