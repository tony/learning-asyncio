#!/usr/bin/env python
"""
Task Internals and Debugging.

This lesson provides insight into how asyncio tasks operate behind the scenes...
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
            f"Inspecting Task: {task_name} - Done: {t.done()}, Cancelled: {t.cancelled()}",
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
