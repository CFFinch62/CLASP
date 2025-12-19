# clasp/pylogo/turtle_builtins.py
"""
Turtle graphics builtins for PyLogo using Python's standard turtle module.
This provides Logo turtle commands (forward, back, right, left, etc.)
"""

import turtle

# Logo-aware function decorator
def logofunc(aliases=None, arity=None, aware=False):
    """Decorator to mark functions as Logo builtins."""
    def decorator(func):
        if aliases:
            func.aliases = aliases
        if arity is not None:
            func.arity = arity
        if aware:
            func.logo_aware = True
        return func
    return decorator

# Global turtle instance
_turtle = None
_screen = None

def _get_turtle():
    """Get or create the global turtle instance."""
    global _turtle, _screen
    if _turtle is None:
        _screen = turtle.Screen()
        _screen.title("CLASP Graphics")
        _turtle = turtle.Turtle()
        _turtle.shape("turtle")
    return _turtle

def _get_screen():
    """Get or create the screen."""
    global _screen
    if _screen is None:
        _get_turtle()  # This initializes both
    return _screen

# Movement commands
@logofunc(aliases=['fd'])
def forward(distance):
    """Move turtle forward by distance."""
    _get_turtle().forward(distance)

@logofunc(aliases=['bk', 'backward'])
def back(distance):
    """Move turtle backward by distance."""
    _get_turtle().backward(distance)

@logofunc(aliases=['rt'])
def right(angle):
    """Turn turtle right by angle degrees."""
    _get_turtle().right(angle)

@logofunc(aliases=['lt'])
def left(angle):
    """Turn turtle left by angle degrees."""
    _get_turtle().left(angle)

# Pen control
@logofunc(aliases=['pu'])
def penup():
    """Lift the pen (stop drawing)."""
    _get_turtle().penup()

@logofunc(aliases=['pd'])
def pendown():
    """Lower the pen (start drawing)."""
    _get_turtle().pendown()

# Position
@logofunc()
def home():
    """Move turtle to origin and reset heading."""
    _get_turtle().home()

@logofunc(aliases=['cs'])
def clearscreen():
    """Clear screen and reset turtle."""
    t = _get_turtle()
    t.clear()
    t.home()

@logofunc()
def clean():
    """Clear drawings but keep turtle position."""
    _get_turtle().clear()

@logofunc()
def setpos(x, y):
    """Move turtle to position (x, y)."""
    _get_turtle().goto(x, y)

@logofunc()
def setxy(x, y):
    """Move turtle to position (x, y)."""
    _get_turtle().goto(x, y)

@logofunc()
def setx(x):
    """Set turtle's x coordinate."""
    _get_turtle().setx(x)

@logofunc()
def sety(y):
    """Set turtle's y coordinate."""
    _get_turtle().sety(y)

@logofunc(aliases=['seth'])
def setheading(angle):
    """Set turtle's heading to angle."""
    _get_turtle().setheading(angle)

# Turtle visibility
@logofunc(aliases=['ht'])
def hideturtle():
    """Hide the turtle."""
    _get_turtle().hideturtle()

@logofunc(aliases=['st'])
def showturtle():
    """Show the turtle."""
    _get_turtle().showturtle()

# Pen properties
@logofunc(aliases=['setpc'])
def setpencolor(color):
    """Set pen color."""
    _get_turtle().pencolor(color)

@logofunc()
def setpensize(size):
    """Set pen size/width."""
    _get_turtle().pensize(size)

@logofunc(aliases=['setbg'])
def setbackground(color):
    """Set background color."""
    _get_screen().bgcolor(color)

# Query commands
@logofunc()
def pos():
    """Return turtle's current position."""
    return list(_get_turtle().position())

@logofunc()
def xcor():
    """Return turtle's x coordinate."""
    return _get_turtle().xcor()

@logofunc()
def ycor():
    """Return turtle's y coordinate."""
    return _get_turtle().ycor()

@logofunc()
def heading():
    """Return turtle's heading."""
    return _get_turtle().heading()

@logofunc()
def towards(x, y):
    """Return angle towards point (x, y)."""
    return _get_turtle().towards(x, y)

# Additional useful commands
@logofunc()
def circle(radius):
    """Draw a circle with given radius."""
    _get_turtle().circle(radius)

@logofunc()
def dot(size=None):
    """Draw a dot at current position."""
    if size:
        _get_turtle().dot(size)
    else:
        _get_turtle().dot()

@logofunc()
def stamp():
    """Stamp turtle shape at current position."""
    _get_turtle().stamp()

@logofunc()
def distance(x, y):
    """Return distance to point (x, y)."""
    return _get_turtle().distance(x, y)
