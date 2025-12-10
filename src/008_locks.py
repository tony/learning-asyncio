#!/usr/bin/env python
"""
Ensuring Safe Access with Locks.

Context
-------
This lesson demonstrates how to use `asyncio.Lock` to safely protect shared state
accessed by multiple coroutines. When multiple tasks try to read or write shared data
concurrently, race conditions can occur. By using a Lock, you can guarantee that only
one coroutine modifies the shared resource at a time, preserving data integrity.

Summary
-------
- Introduce `asyncio.Lock` to control concurrent access to a shared resource.
- Show that multiple tasks incrementing a shared counter without a lock can cause
  race conditions.
- Demonstrate how locking ensures consistent final values by serializing access.
- Reference `src/007_task_groups.py` for supervising these workers with
  structured concurrency.

Official Documentation:
- https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock

Doctest Notes:
- The final result should be deterministic when using a lock.
- We rely on minimal sleeps and await calls to simulate concurrent work.

"""

import asyncio


class SharedResource:
    """A shared resource with thread-safe access via an async lock."""

    def __init__(self) -> None:
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self) -> None:
        """Increment the shared value in a thread-safe manner."""
        # Acquire the lock before modifying the shared state.
        async with self.lock:
            # Simulate a brief pause to highlight the need for locking.
            await asyncio.sleep(0.001)
            current = self.value
            # Another task could run here if not locked, causing a race condition.
            self.value = current + 1


async def worker(resource: SharedResource, increments: int) -> None:
    """
    Asynchronously increments a shared resource a given number of times.

    Parameters
    ----------
    resource : SharedResource
        The shared resource to increment.
    increments : int
        Number of increments to perform.

    Examples
    --------
    >>> res = SharedResource()
    >>> asyncio.run(worker(res, 10))
    >>> res.value
    10
    """
    for _ in range(increments):
        await resource.increment()


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Runs multiple workers that increment a shared counter. A TaskGroup supervises
    the workers, and using a lock ensures that the final counter value matches the
    total expected increments (e.g., 2 workers * 100 increments each = 200).

    Examples
    --------
    >>> asyncio.run(main())
    200
    """
    resource = SharedResource()
    increments = 100
    async with asyncio.TaskGroup() as group:
        group.create_task(worker(resource, increments))
        group.create_task(worker(resource, increments))
    print(resource.value)


if __name__ == "__main__":
    asyncio.run(main())
