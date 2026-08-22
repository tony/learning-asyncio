# Learning Asyncio

A structured, hands-on study of Python's `asyncio` module: each lesson is a
self-contained, doctested script under `src/`, progressing from a first
coroutine to event-loop internals.

## What is this?

Every lesson is one file: a module docstring giving context and further
reading, a `demonstrate_concept()` function with a doctested example, and
a `main()` you can run directly.

## Quick Start

Clone the repository:

```console
$ git clone https://github.com/tony/learning-asyncio.git && cd learning-asyncio
```

Install the development dependencies:

```console
$ uv sync --all-extras --dev
```

Run a lesson — no install required, the lessons use only the standard
library:

```console
$ python src/001_intro.py
```

Run all tests, including every lesson's doctests:

```console
$ uv run pytest
```

## Lesson Overview

### Part I: Foundations (Lessons 1-6)

- **Lesson 1**: Your first async function
- **Lesson 2**: Returning values from coroutines
- **Lesson 3**: Running multiple tasks concurrently
- **Lesson 4**: Handling exceptions in async code
- **Lesson 5**: Managing tasks explicitly
- **Lesson 6**: Blocking calls and cooperative yielding

### Part II: Synchronization (Lessons 7-13)

- **Lesson 7**: Task groups - structured concurrency
- **Lesson 8**: Locks - preventing race conditions
- **Lesson 9**: Semaphores - limiting concurrent access
- **Lesson 10**: Queues - producer/consumer patterns
- **Lesson 11**: Events - signaling between tasks
- **Lesson 12**: Conditions - complex coordination
- **Lesson 13**: Barriers - synchronizing task groups

### Part III: Real-World I/O (Lessons 14-16, 23)

- **Lesson 14**: Network streams and protocols
- **Lesson 15**: Running subprocesses
- **Lesson 16**: Timeouts and cancellation
- **Lesson 23**: Asynchronous file I/O patterns

### Part IV: Event Loop Internals (Lessons 17-22)

- **Lesson 17**: How the event loop works
- **Lesson 18**: Task internals and debugging
- **Lesson 19**: Custom event loops
- **Lesson 20**: Thread executors and scheduling
- **Lesson 21**: Selectors, transports, and protocols
- **Lesson 22**: Performance profiling and optimization

### Part V: Observability & Diagnostics (Lessons 24-26)

Built on introspection added in Python 3.14: `asyncio.tools` (lessons 24
and 26) and the top-level `asyncio.capture_call_graph` /
`asyncio.print_call_graph` (lesson 25).

- **Lesson 24**: Inspect running tasks with `asyncio.tools`
- **Lesson 25**: Capture async call graphs programmatically
- **Lesson 26**: Observe tasks across threads and loops

## Learning Approach

- Each lesson is self-contained and teaches one concept.
- Doctests are the tests: run `pytest` on any lesson to check your
  understanding, or run the file directly to see it work.
- Delays in the examples are 0.001 seconds — long enough to demonstrate
  suspension, short enough to keep the suite fast.
- Lessons build on each other; start from Part I even if you know some
  async.

## Development

Lint:

```console
$ uv run ruff check .
```

Format:

```console
$ uv run ruff format .
```

Type-check:

```console
$ uv run mypy .
```

Watch mode, re-running affected tests on save:

```console
$ uv run pytest-watcher
```

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for the full gate list CI
enforces.

## Requirements

- Python `>=3.14,<4.0`
- No external dependencies for the lessons themselves
- Development tools — pytest, ruff, mypy — installed via
  `uv sync --all-extras --dev`

## Notes

There are doctests generated based on CPython's `asyncio` module. You can
access them directly via [uvx] / [pipx] ([gp-libs] is required to parse
doctest from markdown):

uvx:

```console
$ uvx --from gp-libs python -m doctest_docutils notes/libs/cpython-asyncio-doctest.md -v
```

pipx:

```console
$ pipx run --spec gp-libs -- python -m doctest_docutils notes/libs/cpython-asyncio-doctest.md -v
```

[uvx]: https://docs.astral.sh/uv/guides/tools/
[pipx]: https://pipx.pypa.io/stable/examples/
[gp-libs]: https://github.com/git-pull/gp-libs

## Contributing

Found an issue or have a suggestion? Open an issue or a pull request — see
[CONTRIBUTING.md](.github/CONTRIBUTING.md) for the environment and gates.

## License

MIT License

Copyright (c) Tony Narlock 2024-
