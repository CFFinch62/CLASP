# Phase 3: Syntax Highlighting & Bracket Matching - Changelog

## Completed Tasks
- [x] **Syntax Highlighter**: Created `LogoHighlighter` using `QSyntaxHighlighter`.
- [x] **Rules Definition**:
    - **Keywords**: Blue/Bold (e.g., `to`, `end`, `fd`).
    - **Variables**: Green (e.g., `:count`).
    - **Strings**: Orange (e.g., `"hello`).
    - **Numbers**: Purple.
    - **Comments**: Grey Italic.
- [x] **Bracket Matching**:
    - Implemented logic to find matching `[]` or `()` relative to cursor.
    - Added visual highlighting for matched pairs.

## Technical Details
- **Regex**: Used `QRegularExpression` for efficient token matching.
- **Integration**: Highlighter applied automatically to `LogoEditor` document.
