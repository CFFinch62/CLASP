# PyLogo Porting / Vendoring - Changelog

## Overview
The `pylogo` library was found to be unmaintained and incompatible with Python 3 (last updated for Python 2). To use it in CLASP, it has been **vendored** into the project (`clasp/pylogo`) and **ported** to Python 3.

## Changes Made
- **Vendoring**: Copied `pylogo` 0.4 source into `clasp/pylogo`.
- **Syntax Modernization**:
    - Converted `print ...` to `print(...)`.
    - Converted `except Exception, e:` to `except Exception as e:`.
    - Converted `raise Type, Value, Traceback` to `raise Type(Value).with_traceback(Traceback)`.
    - Converted `raise Error, Msg` to `raise Error(Msg)`.
- **Python 3 Compat**:
    - Replaced `basestring` with `str`.
    - Replaced `ClassType` with `type`.
    - Replaced `raw_input` with `input`.
    - Replaced `xrange` with `range`.
    - Replaced `iteritems()` with `items()`.
    - Replaced `dict.has_key(k)` with `k in dict`.
    - Replaced `from sets import Set` with `Set = set`.
- **Module Replacements**:
    - `StringIO` -> `io.StringIO`.
    - `Queue` -> `queue`.
    - `Tkinter` -> `tkinter`.
    - Removed `imp` module usage (deprecated).
- **Introspection**:
    - Updated function attributes: `.func_name` -> `.__name__`, `.func_dict` -> `.__dict__`, etc.
- **Imports**:
    - Converted all implicit relative imports to explicit relative imports (e.g. `from . import interpreter`).

## Status
The vendored `pylogo` package now imports correctly in a Python 3.10+ environment.

## Additional Fixes (2024-12)
- **reader.py line 50**: Replaced `type(f) is file` with `hasattr(f, 'read')` check (Python 3 has no `file` type).
- **reader.py line 91**: Replaced `self.generator.next()` with `next(self.generator)` (Python 3 iterator syntax).
- **interpreter.py line 770**: Replaced `inspect.getargspec()` with `inspect.getfullargspec()` (removed in Python 3.11+).
- **common.py line 8**: Added `description = 'Logo error'` default attribute to `LogoError` base class.
- **common.py line 19**: Changed `' '.join(args)` to `' '.join(str(arg) for arg in args)` to handle non-string args.
- **builtins.py line 68-76**: Updated `logo_soft_repr()` to convert non-list/non-string types to string.
- **builtins.py line 92**: Changed `result.write(arg)` to `result.write(str(arg))` in `_join()`.
