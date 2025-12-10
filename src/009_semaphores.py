#!/usr/bin/env python
"""
Limiting Concurrent Work with Semaphores.

Context
-------
This lesson demonstrates how to use `asyncio.Semaphore` to limit the number of
concurrent tasks running at the same time. Sometimes, running too many coroutines
concurrently can overwhelm resources or degrade performance. By using a semaphore,
you can control concurrency and maintain a balance between throughput and resource
usage.

Summary
-------
- Introduce `asyncio.Semaphore` for controlling concurrency.
- Show how only a limited number of tasks can "enter" a critical section at once.
- Help tune concurrency levels to achieve optimal performance without oversaturating
  resources.
- Pair with the TaskGroup supervisor lesson (`src/007_task_groups.py`) to manage
  worker lifetimes cleanly.

Official Documentation:
- https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore

Doctest Notes:
- Because concurrency introduces non-deterministic timing, the exact order of
  "working"/"done" messages can vary. We use ellipses to match variable parts of the
  output and focus on the pattern rather than exact order.
"""

import asyncio


async def limited_worker(semaphore: asyncio.Semaphore, worker_id: int) -> None:
    """
    Asynchronously performs a task while respecting a concurrency limit.

    Parameters
    ----------
    semaphore : asyncio.Semaphore
        The semaphore controlling concurrency.
    worker_id : int
        The ID of the worker, used for demonstration output.

    No direct doctest here, since we rely on `main` to demonstrate the pattern.
    """
    async with semaphore:
        print(f"Worker {worker_id} is working.")
        await asyncio.sleep(0.001)  # Simulate some work
        print(f"Worker {worker_id} is done.")


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Creates several workers and uses a semaphore to ensure only two tasks run
    concurrently while a TaskGroup supervises their lifecycle. We use ellipses
    in the doctest to allow for variations in which worker finishes first and in
    what order tasks complete.

    The general pattern is:
    - Two workers start working simultaneously.
    - As soon as one finishes, the next worker can start.
    - Eventually, all three workers complete.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Worker ... is working.
    Worker ... is working.
    Worker ... is done.
    Worker ... is done.
    Worker ... is working.
    Worker ... is done.
    """
    semaphore = asyncio.Semaphore(2)  # Limit concurrency to 2 tasks
    async with asyncio.TaskGroup() as group:
        for i in range(3):
            group.create_task(limited_worker(semaphore, i))


if __name__ == "__main__":
    asyncio.run(main())
