# CPython Asyncio Internals Reference

Source files and concepts backing lessons 15-20, which move from the
public `asyncio` API into the event loop's own implementation.

## Core files in CPython

- `Lib/asyncio/base_events.py` — `BaseEventLoop`, the concrete loop that
  `_run_once()` drives.
- `Lib/asyncio/events.py` — the abstract loop and handle interfaces.
- `Lib/asyncio/tasks.py` — `Task`, including the `__step` state machine.
- `Lib/asyncio/futures.py` — `Future`, the awaitable both `Task` and
  low-level callbacks build on.
- `Modules/_asynciomodule.c` — the C implementation of `Task` and
  `Future` that CPython uses by default.

## Key concepts

- `_run_once()`: one iteration of the event loop — poll for I/O, run
  ready callbacks, reschedule timers.
- Task state machine: how `__step` resumes a coroutine and reacts to a
  yielded `Future`, an exception, or completion.
- `Handle` and `TimerHandle`: the callback wrappers `call_soon` and
  `call_later` return, and how cancellation marks them.
- Selector-based I/O: how `BaseSelectorEventLoop` differs across
  platforms (`selectors.SelectSelector` vs `epoll`/`kqueue`).
- `Future`/`Task` relationship: why `Task` is a `Future` subclass, and
  what the C accelerator in `_asynciomodule.c` changes versus the pure
  Python implementation in `tasks.py`.
