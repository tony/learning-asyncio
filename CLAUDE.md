# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a structured learning repository for Python's asyncio module, consisting of 20 progressive lessons covering everything from basic async/await concepts to advanced event loop internals.

## Essential Commands

### Running Tests
```bash
uv run pytest                # Run all tests including doctests
uv run pytest-watcher        # Run tests in watch mode for continuous development
```

### Code Quality
```bash
uv run ruff check           # Run linter
uv run ruff format          # Format code
uv run mypy src/            # Type check source files
```

### Running Individual Lessons
```bash
python src/001_intro.py     # Run any lesson directly
```

## Architecture and Structure

### Lesson Organization
The codebase follows a strict lesson-based structure:
- **Part I (Lessons 1-5)**: Foundational async concepts
- **Part II (Lessons 6-11)**: Synchronization primitives (Lock, Semaphore, Queue, Event, Condition, Barrier)
- **Part III (Lessons 12-14)**: External integrations (Streams, Subprocess, Timeout)
- **Part IV (Lessons 15-20)**: Event loop internals and advanced techniques

### Lesson Pattern
Each lesson follows the template in `notes/lesson_template.py`:
1. Comprehensive docstring with Context, Summary, and References
2. `demonstrate_concept()` function showing the core concept
3. `main()` function orchestrating the demonstration
4. Extensive doctests serving as both documentation and tests
5. Executable entry point

### Key Development Patterns
- **Doctests**: All functionality is verified through doctests which pytest runs automatically
- **Minimal delays**: Use 0.001s delays to keep tests fast
- **Deterministic output**: Ensure consistent output for reliable doctests
- **Type hints**: Strict mypy configuration requires comprehensive type annotations
- **Self-contained**: Each lesson is independent and demonstrates a single concept

### Testing Strategy
- pytest is configured with `--doctest-modules` to run all doctests
- Tests are located within the lesson files themselves
- No separate test directory - lessons are both educational content and tests

## Important Notes
- This is a pure Python stdlib project - no external dependencies beyond asyncio
- Code style is enforced through extensive ruff rules including pydocstyle
- When modifying lessons, ensure doctests still pass and output remains deterministic