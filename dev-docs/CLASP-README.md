# CLASP - Coding in Logo to Attack Serious Problems

**A Modern IDE for Logo Programming**

---

## Overview

CLASP is a modern integrated development environment for Logo programming, built to present Logo as the serious problem-solving language it truly is. This project honors the vision of Professor Brian Harvey and the Logo community by providing a contemporary interface that emphasizes Logo's computational power beyond turtle graphics.

Logo is a Lisp dialect with genuine capabilities—recursion, symbolic computation, list processing—but decades of "turtle first" pedagogy have unfairly pigeonholed it as a children's drawing language. CLASP aims to change that perception.

---

## Philosophy

Logo deserves better than its reputation. Professor Harvey's *Computer Science Logo Style* trilogy demonstrates what Logo can do as a serious tool:

- Recursive programming
- Symbolic computation  
- List processing (Logo is a Lisp dialect)
- Data structures and algorithms
- Genuine problem-solving

CLASP supports that vision with a modern interface. Graphics are available when needed, but they're not the focus.

---

## Architecture

CLASP uses **PyLogo** (a Python Logo interpreter) and Python's built-in **turtle** module for a simple, pure-Python architecture:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLASP Main Window                           │
│  ┌──────────────┬────────────────────────┬───────────────────────┐  │
│  │              │                        │                       │  │
│  │    File      │      Code Editor       │     REPL Terminal     │  │
│  │   Browser    │                        │                       │  │
│  │              │   - Syntax highlight   │   - PyLogo interpreter│  │
│  │   - Tree     │   - Bracket matching   │   - In-process exec   │  │
│  │   - CRUD     │   - Line numbers       │   - Output capture    │  │
│  │              │   - Logo awareness     │                       │  │
│  │              │                        │                       │  │
│  └──────────────┴────────────────────────┴───────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                  ┌───────────────────────────┐
                  │   Turtle Graphics Window  │
                  │   (Python turtle module)  │
                  └───────────────────────────┘
```

This approach provides:

- **Simplicity** — No subprocess management or PTY complexity
- **Cross-platform** — Pure Python works everywhere
- **Fast development** — Focus on the IDE, not plumbing
- **Reliable graphics** — turtle module is battle-tested

---

## Key Features

- **File Browser** — Navigate and organize Logo projects
- **Code Editor** — Syntax highlighting, bracket matching for Logo
- **REPL Terminal** — Interactive Logo session (PyLogo interpreter)
- **Turtle Graphics** — Available when needed, not the focus
- **Cross-Platform** — Linux, macOS, Windows

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| GUI Framework | PyQt6 |
| Logo Interpreter | PyLogo |
| Graphics | Python turtle module |
| Configuration | JSON (~/.config/clasp/) |

---

## Documentation

| Document | Purpose |
|----------|---------|
| `CLASP-README.md` | This file — overview and orientation |
| `CLASP-TECHNICAL.md` | Architecture, component specs, data flow |
| `CLASP-IMPLEMENTATION.md` | Phased development plan with checkpoints |
| `CLASP-AGENT-PROMPT.md` | Comprehensive prompt for AI-assisted development |

---

## Name

**CLASP** — Coding in Logo to Attack Serious Problems

The name emphasizes Logo as a real problem-solving language, not just a drawing toy.

---

## Acknowledgments

This project honors **Professor Brian Harvey** and the Logo community. His decades of work demonstrating Logo's true capabilities as a serious programming language inspired this project.

---

## License

MIT License

---

## Author

Chuck / Fragillidae Software
