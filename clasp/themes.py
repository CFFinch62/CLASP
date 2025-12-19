# clasp/themes.py

AMBER_BLUE_THEME = {
    'name': 'Amber Blue',
    'background': '#2E3440',       # Dark grey/blue (Nord-like)
    'accent': '#4C566A',           # Lighter grey/blue
    
    # Editor
    'editor_bg': '#2E3440',
    'editor_fg': '#D8DEE9',        # Off-white
    'editor_selection': '#434C5E',
    'editor_current_line': '#3B4252',
    
    # Line numbers
    'line_numbers_bg': '#2E3440',
    'line_numbers_fg': '#4C566A',
    
    # Syntax Highlighting
    'syntax_keyword': '#81A1C1',   # Blue
    'syntax_variable': '#A3BE8C',  # Green
    'syntax_string': '#D08770',    # Orange/Amber
    'syntax_number': '#B48EAD',    # Purple
    'syntax_comment': '#616E88',   # Grey
}

LIGHT_THEME = {
    'name': 'Light',
    'background': '#FAFAFA',       # Off-white
    'accent': '#E0E0E0',           # Light grey
    
    # Editor
    'editor_bg': '#FFFFFF',
    'editor_fg': '#212121',        # Near black
    'editor_selection': '#BBDEFB',
    'editor_current_line': '#F5F5F5',
    
    # Line numbers
    'line_numbers_bg': '#FAFAFA',
    'line_numbers_fg': '#9E9E9E',
    
    # Syntax Highlighting
    'syntax_keyword': '#1565C0',   # Blue
    'syntax_variable': '#2E7D32',  # Green
    'syntax_string': '#E65100',    # Orange
    'syntax_number': '#7B1FA2',    # Purple
    'syntax_comment': '#757575',   # Grey
}

MONOKAI_THEME = {
    'name': 'Monokai',
    'background': '#272822',       # Dark brown-grey
    'accent': '#3E3D32',           # Slightly lighter
    
    # Editor
    'editor_bg': '#272822',
    'editor_fg': '#F8F8F2',        # Off-white
    'editor_selection': '#49483E',
    'editor_current_line': '#3E3D32',
    
    # Line numbers
    'line_numbers_bg': '#272822',
    'line_numbers_fg': '#75715E',
    
    # Syntax Highlighting
    'syntax_keyword': '#F92672',   # Pink/Magenta
    'syntax_variable': '#A6E22E',  # Bright green
    'syntax_string': '#E6DB74',    # Yellow
    'syntax_number': '#AE81FF',    # Purple
    'syntax_comment': '#75715E',   # Brown-grey
}

SOLARIZED_DARK_THEME = {
    'name': 'Solarized Dark',
    'background': '#002B36',       # Base03
    'accent': '#073642',           # Base02
    
    # Editor
    'editor_bg': '#002B36',
    'editor_fg': '#839496',        # Base0
    'editor_selection': '#073642',
    'editor_current_line': '#073642',
    
    # Line numbers
    'line_numbers_bg': '#002B36',
    'line_numbers_fg': '#586E75',
    
    # Syntax Highlighting
    'syntax_keyword': '#268BD2',   # Blue
    'syntax_variable': '#859900',  # Green
    'syntax_string': '#CB4B16',    # Orange
    'syntax_number': '#D33682',    # Magenta
    'syntax_comment': '#586E75',   # Base01
}

# Theme registry for easy lookup
THEMES = {
    'amber_blue': AMBER_BLUE_THEME,
    'light': LIGHT_THEME,
    'monokai': MONOKAI_THEME,
    'solarized_dark': SOLARIZED_DARK_THEME,
}

DEFAULT_THEME = 'amber_blue'
