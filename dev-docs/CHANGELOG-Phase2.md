# Phase 2: Editor & File Operations - Changelog

## Completed Tasks
- [x] **Editor Widget**: Implemented `LogoEditor` (subclass of `QPlainTextEdit`).
- [x] **Line Numbers**: Added `LineNumberArea` widget synced with editor scrolling.
- [x] **File Operations**:
    - **New**: Clear editor and reset state.
    - **Open**: Load `.logo` files from disk.
    - **Save / Save As**: Write content to disk.
- [x] **UI Integration**: Connected File menu actions to editor methods.
- [x] **State Tracking**: Added modification flag (`*` in titlebar) and unsaved changes warning.
- [x] **Run Integration**: Added `Run File` and `Run Selection` features connecting Editor to Terminal.

## Technical Details
- **Fonts**: Configured Monospace font for code editing.
- **Painting**: Custom `paintEvent` for line numbers bar.
