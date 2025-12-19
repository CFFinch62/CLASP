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
