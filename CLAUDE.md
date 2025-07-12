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

### Lesson Template Structure
Each lesson strictly follows the template in `notes/lesson_template.py` with these sections:

1. **Module Docstring** with:
   - Clear title
   - Context section (concept, prerequisites, references)
   - Summary section (learning outcomes)
   - Doctest notes

2. **Standard imports** (only stdlib, primarily asyncio)

3. **`demonstrate_concept()` function**:
   - Core demonstration of the lesson's concept
   - Comprehensive docstring with Examples section
   - Minimal async sleep (0.001s) for testing speed
   - Returns demonstrable results

4. **`main()` function**:
   - Orchestrates the demonstration
   - Handles multiple tasks for concurrency lessons
   - Prints results for direct execution

5. **Executable entry point**: `if __name__ == "__main__"`

### Key Development Patterns
- **Doctests**: All functionality is verified through doctests which pytest runs automatically
- **Minimal delays**: Use 0.001s delays to keep tests fast
- **Deterministic output**: Ensure consistent output for reliable doctests
- **Type hints**: Strict mypy configuration requires comprehensive type annotations
- **Self-contained**: Each lesson is independent and demonstrates a single concept
- **Educational focus**: Comments explain tricky parts, no external dependencies

### Testing Strategy
- pytest is configured with `--doctest-modules` to run all doctests
- Tests are located within the lesson files themselves
- No separate test directory - lessons are both educational content and tests
- Use `# doctest: +ELLIPSIS` for non-deterministic output (concurrency)

## Known Issues (from recommendations.md)

### Critical Issues
- **Lesson 11 missing**: No `011_barriers.py` file (content is in `012_streams.py`)
- **Lesson 12 incorrect**: Contains barriers content instead of streams
- **Streams not covered**: Network I/O with streams is completely missing

### File Naming
- Lesson 20 is `020_profiling_and_optimizing.py` (should be `020_performance_tuning.py`)

### Content Balance
- Over-emphasis on synchronization primitives (25% of content)
- Under-representation of practical I/O examples
- Missing topics: file I/O, HTTP clients, testing async code

## CPython Asyncio Internals Reference

For advanced lessons (15-20), key CPython internals to reference:

### Core Files in CPython
- `Lib/asyncio/base_events.py` - BaseEventLoop implementation
- `Lib/asyncio/events.py` - Abstract interfaces
- `Lib/asyncio/tasks.py` - Task implementation
- `Lib/asyncio/futures.py` - Future implementation
- `Modules/_asynciomodule.c` - C acceleration

### Key Concepts to Cover
- Event loop's `_run_once()` method and execution model
- Task state machine and `__step` mechanism
- Handle/TimerHandle callback system
- Selector-based I/O and platform differences
- Future/Task relationship and C optimization

## Important Notes
- This is a pure Python stdlib project - no external dependencies beyond asyncio
- Code style is enforced through extensive ruff rules including pydocstyle
- When modifying lessons, ensure doctests still pass and output remains deterministic
- Maintain educational value - each lesson should teach one concept clearly
