#!/usr/bin/env python
"""
Task Internals and Debugging.

Context
-------
Understanding how asyncio Tasks work internally helps you write better async code
and debug issues effectively. A Task is asyncio's way of scheduling a coroutine
to run on the event loop. When you call ``asyncio.create_task()``, asyncio wraps
your coroutine in a Task object that manages its execution state.

**Key Concepts:**

- **Task State Machine**: Tasks track their state (pending, running, done,
  cancelled) and transition between states as the event loop progresses.

- **The __step() Method**: Internally, Tasks use a ``__step()`` method that the
  event loop calls to advance the coroutine. Each ``__step()`` call resumes the
  coroutine until it hits the next ``await``, then schedules itself to be called
  again when the awaited object completes.

- **Task/Future Relationship**: Task inherits from Future. While Futures represent
  eventual results, Tasks actively drive coroutine execution. A Task sets its own
  Future result when the wrapped coroutine completes.

- **Handle/TimerHandle**: The event loop schedules Task steps using Handle objects.
  When you create a task, the event loop creates a Handle pointing to the task's
  ``__step()`` method and adds it to the ready queue.

- **C Acceleration**: CPython optimizes Task and Future with C implementations in
  ``_asynciomodule.c`` for better performance. The pure Python versions in
  ``asyncio/tasks.py`` and ``asyncio/futures.py`` serve as reference implementations.

**CPython Internals References:**

- ``Lib/asyncio/tasks.py``: Task implementation, ``__step()`` at line ~266
- ``Lib/asyncio/futures.py``: Future base class
- ``Lib/asyncio/events.py``: Handle/TimerHandle callback system (lines ~34, ~141)
- ``Lib/asyncio/base_events.py``: Event loop's ``_run_once()`` at line ~1966
- ``Modules/_asynciomodule.c``: C-accelerated Task/Future implementations

**Debugging Tools:**

- ``asyncio.current_task()``: Get the currently running Task
- ``asyncio.all_tasks()``: List all tasks in the event loop
- ``task.get_name()`` / ``task.set_name()``: Task identification
- ``task.get_stack()`` / ``task.print_stack()``: Inspect task call stack
- ``task.get_coro()``: Access the underlying coroutine
- ``task.done()`` / ``task.cancelled()``: Check task state

Summary
-------
This lesson demonstrates practical debugging techniques:

- Creating named tasks for easier identification in debug output
- Using ``asyncio.all_tasks()`` to enumerate running tasks
- Inspecting task state (done, cancelled) during execution
- Understanding that debugging tools access Task internals like state and coro

By understanding Task internals, you can better diagnose issues like:

- Tasks not completing (stuck in ``__step()`` loop)
- Unexpected cancellation (cancelled state propagation)
- Performance problems (too many scheduled Handles)
- Memory leaks (uncollected Tasks in the event loop)

Official Documentation:
    https://docs.python.org/3/library/asyncio-task.html#asyncio.Task

CPython Source:
    https://github.com/python/cpython/blob/main/Lib/asyncio/tasks.py

Doctest Notes:
    This lesson has no doctests in the code but demonstrates debugging by printing
    task information. The output shows task names, state, and provides a foundation
    for using more advanced debugging tools like ``get_stack()`` and ``print_stack()``
    in real debugging scenarios.
"""

import asyncio
from typing import Any


async def worker_task(task_id: int) -> str:
    """Simulate a simple worker task that completes after a short delay."""
    await asyncio.sleep(0.001)
    return f"Worker {task_id} completed"


async def inspect_tasks(main_task: asyncio.Task[Any]) -> None:
    """Inspect and print information about all running tasks."""
    current_tasks = asyncio.all_tasks()
    # Sort tasks for deterministic output: main first, then by name
    sorted_tasks = sorted(
        current_tasks,
        key=lambda t: (t is not main_task, t.get_name() or ""),
    )

    for t in sorted_tasks:
        task_name = "main" if t is main_task else (t.get_name() or "unnamed")
        print(
            f"Inspecting Task: {task_name} - Done: {t.done()}, "
            f"Cancelled: {t.cancelled()}",
        )
    print(f"Total tasks currently: {len(current_tasks)}")


async def main() -> None:
    """Run the main demonstration for this lesson.

    Demonstrates:
    - Creating multiple tasks named for easier identification.
    - Using `asyncio.all_tasks()` to list them for debugging.
    - Waiting for tasks to complete and inspecting their results.
    """
    # current_task() returns Optional[Task[Any]]
    main_task: asyncio.Task[Any] | None = asyncio.current_task()
    # We are inside an async function called by asyncio.run(), so main_task is not None
    assert main_task is not None

    task1: asyncio.Task[str] = asyncio.create_task(worker_task(0), name="worker-0")
    task2: asyncio.Task[str] = asyncio.create_task(worker_task(1), name="worker-1")

    await inspect_tasks(main_task)

    result1 = await task1
    result2 = await task2

    print(f"Worker 0 result: {result1}")
    print(f"Worker 1 result: {result2}")


if __name__ == "__main__":
    asyncio.run(main())
