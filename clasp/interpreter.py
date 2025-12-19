# clasp/interpreter.py

import io
import sys
import re
from contextlib import redirect_stdout, redirect_stderr

try:
    from .pylogo.interpreter import RootFrame
    from .pylogo.common import LogoError
    from .pylogo import builtins, oobuiltins, turtle_builtins
    PYLOGO_AVAILABLE = True
except ImportError:
    RootFrame = None
    LogoError = None
    builtins = None
    oobuiltins = None
    turtle_builtins = None
    PYLOGO_AVAILABLE = False

# Turtle graphics commands that should auto-show graphics window
TURTLE_COMMANDS = {
    'forward', 'fd', 'back', 'bk', 'backward',
    'right', 'rt', 'left', 'lt',
    'penup', 'pu', 'pendown', 'pd',
    'home', 'clearscreen', 'cs', 'clean',
    'hideturtle', 'ht', 'showturtle', 'st',
    'setpos', 'setxy', 'setx', 'sety', 'setheading', 'seth',
    'setpencolor', 'setpc', 'setpensize', 'setbackground', 'setbg',
    'arc', 'circle', 'dot', 'stamp', 'fill',
    'towards', 'distance',
}


class LogoInterpreter:
    """Wrapper around PyLogo interpreter."""
    
    def __init__(self, graphics_manager=None):
        if not PYLOGO_AVAILABLE:
            raise ImportError("PyLogo is not installed or available.")
        
        self.logo = RootFrame()
        self.logo.import_module(builtins)
        self.logo.import_module(oobuiltins)
        self.logo.import_module(turtle_builtins)
        self.graphics = graphics_manager
    
    def _has_turtle_commands(self, code):
        """Check if code contains any turtle graphics commands."""
        # Simple regex to find word boundaries for commands
        code_lower = code.lower()
        for cmd in TURTLE_COMMANDS:
            # Match command as whole word (not part of variable name, etc.)
            if re.search(rf'\b{cmd}\b', code_lower):
                return True
        return False
        
    def execute(self, code):
        """Execute Logo code and return results."""
        # Auto-show graphics window if code contains turtle commands
        if self.graphics and self._has_turtle_commands(code):
            self.graphics.ensure_visible()
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            # Wrap code string in a StringIO stream for PyLogo
            code_stream = io.StringIO(code)
            code_stream.name = '<string>'  # PyLogo's TrackingStream expects a name attribute
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                self.logo.import_logo_stream(code_stream)
            
            return {
                'success': True,
                'result': None,
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
        self.logo = RootFrame()
        self.logo.import_module(builtins)
        self.logo.import_module(oobuiltins)
        self.logo.import_module(turtle_builtins)


def check_pylogo():
    """Check if PyLogo is available."""
    return PYLOGO_AVAILABLE
