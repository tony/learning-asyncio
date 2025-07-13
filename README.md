# Learning Asyncio 🚀

A friendly, hands-on tutorial series for mastering Python's asyncio library through 20 progressive lessons.

## What is this?

This repository contains a structured learning path for Python's asyncio module. Each lesson is a self-contained Python file that demonstrates a specific async concept - from basic coroutines to advanced event loop internals.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/tony/learning-asyncio.git
cd learning-asyncio

# Install development dependencies
pip install -e .

# Run a lesson
python src/001_intro.py

# Run all tests
uv run pytest
```

## Lesson Overview

### 🌱 Part I: Foundations (Lessons 1-5)
Start here if you're new to async programming!

- **Lesson 1**: Your first async function
- **Lesson 2**: Returning values from coroutines  
- **Lesson 3**: Running multiple tasks concurrently
- **Lesson 4**: Handling exceptions in async code
- **Lesson 5**: Managing tasks explicitly

### 🔧 Part II: Synchronization (Lessons 6-11)
Learn to coordinate async tasks safely.

- **Lesson 6**: Locks - preventing race conditions
- **Lesson 7**: Semaphores - limiting concurrent access
- **Lesson 8**: Queues - producer/consumer patterns
- **Lesson 9**: Events - signaling between tasks
- **Lesson 10**: Conditions - complex coordination
- **Lesson 11**: Barriers - synchronizing task groups

### 🌐 Part III: Real-World I/O (Lessons 12-14)
Connect to the outside world asynchronously.

- **Lesson 12**: Network streams and protocols
- **Lesson 13**: Running subprocesses
- **Lesson 14**: Timeouts and cancellation

### 🔬 Part IV: Advanced Topics (Lessons 15-20)
Deep dive into asyncio internals.

- **Lesson 15**: How the event loop works
- **Lesson 16**: Task internals and debugging
- **Lesson 17**: Custom event loops
- **Lesson 18**: Thread executors and scheduling
- **Lesson 19**: Low-level I/O primitives
- **Lesson 20**: Performance profiling and optimization

## Learning Approach

Each lesson follows a consistent structure:

1. **Clear explanations** - Concepts are introduced with context
2. **Working examples** - Run the code to see it in action
3. **Built-in tests** - All examples include doctests
4. **Progressive difficulty** - Each lesson builds on the previous

## Development

```bash
# Run tests in watch mode (great for learning!)
uv run pytest-watcher

# Check code style
uv run ruff check
uv run ruff format

# Type checking
uv run mypy src/
```

## Requirements

- Python 3.12 or higher
- No external dependencies for the lessons themselves
- Development tools: pytest, ruff, mypy (installed via pip install -e .)

## Tips for Learning

1. **Start from the beginning** - Even if you know some async, the lessons build on each other
2. **Run the code** - Each lesson is executable: `python src/001_intro.py`
3. **Experiment** - Modify the examples and see what happens
4. **Use the tests** - Run `pytest` on individual files to verify your understanding

## Philosophy

This tutorial series believes in:
- **Learning by doing** - All concepts are demonstrated with runnable code
- **Minimal complexity** - Examples use only Python's standard library
- **Fast feedback** - Tests run quickly (0.001s delays)
- **Clear progression** - Each lesson teaches one concept well

## Contributing

Found an issue or have a suggestion? Feel free to open an issue or submit a PR!

## License

MIT License

Copyright (c) Tony Narlock 2024-

---

Happy async coding! 🎉 Remember: async programming is powerful but takes practice. Take your time with each lesson and don't hesitate to revisit earlier concepts.
