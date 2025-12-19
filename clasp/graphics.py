# clasp/graphics.py

import turtle

class TurtleGraphicsManager:
    """Manages turtle graphics window."""
    
    def __init__(self):
        self.screen = None
        self.t = None
        self.is_initialized = False
        self.is_visible = False
        self.on_state_change = None
        self.root = None

    def set_callback(self, callback):
        """Set callback for state changes (visible/hidden)."""
        self.on_state_change = callback

    def initialize(self):
        """Initialize turtle graphics."""
        if self.is_initialized:
            return
            
        # Setup screen
        try:
            self.screen = turtle.Screen()
            self.screen.title("CLASP Graphics")
            self.screen.setup(600, 600)
            self.screen.bgcolor("white")
            
            # Get the Tk root window
            cv = self.screen.getcanvas()
            self.root = cv.winfo_toplevel()
            
            # Handle window closing - hide instead of destroy
            self.root.protocol("WM_DELETE_WINDOW", self._on_close_request)
            
            # Setup turtle
            self.t = turtle.Turtle()
            self.t.speed(0)  # Fastest
            self.t.shape("turtle")
            
            self.is_initialized = True
        except turtle.Terminator:
            # Handle case where turtle was closed and we try to init again
            self.is_initialized = False
    
    def _on_close_request(self):
        """Handle window X button click - hide instead of destroy."""
        self.hide()
    
    def _notify_state_change(self, visible):
        """Notify callback of visibility change."""
        if self.on_state_change:
            self.on_state_change(visible)

    def show(self):
        """Show the graphics window."""
        self._ensure_init()
        try:
            if self.root:
                self.root.deiconify()
                self.root.lift()
                self.is_visible = True
                self._notify_state_change(True)
        except (AttributeError, turtle.Terminator):
            pass

    def hide(self):
        """Hide the graphics window."""
        if self.is_initialized and self.root:
            try:
                self.root.withdraw()
                self.is_visible = False
                self._notify_state_change(False)
            except (AttributeError, turtle.Terminator):
                pass
             
    def clear(self):
        """Clear the graphics."""
        if self.is_initialized and self.t:
            self.t.clear()
            self.t.home()
            
    def _ensure_init(self):
        if not self.is_initialized:
            self.initialize()
    
    def ensure_visible(self):
        """Ensure graphics window is visible - for auto-show on turtle commands."""
        if not self.is_visible:
            self.show()
            
    # Forwarding common commands if manual control is needed outside PyLogo
    # PyLogo should handle most, but having direct access is useful.
    def forward(self, distance):
        self._ensure_init()
        self.ensure_visible()
        self.t.forward(distance)
