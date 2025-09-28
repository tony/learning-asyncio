#!/usr/bin/env python
"""
Synchronizing Tasks with Barriers.

Context
-------
This lesson demonstrates how to use `asyncio.Barrier` to synchronize a fixed
number of tasks. A barrier allows a group of coroutines to run independently
until they all reach the same "barrier" point. Once all tasks have arrived at
the barrier, they are simultaneously allowed to proceed, ensuring that certain
parts of your workflow happen in well-defined phases.

Summary
-------
- Introduce `asyncio.Barrier` for coordinated task synchronization.
- Show how multiple tasks can run freely until they reach the barrier.
- Once all tasks are waiting at the barrier, they proceed together.
- Suggest combining barriers with structured supervisors from
  `src/006_task_groups.py` to manage participating tasks.

Official Documentation:
- https://docs.python.org/3/library/asyncio-sync.html#asyncio.Barrier

Doctest Notes:
- The order in which tasks print their "waiting" messages may vary, but they
  must all print before the barrier is passed.
- Once all tasks reach the barrier, they pass it and print their "passed" messages.
- Use ellipses for flexibility in output order if necessary.
"""

import asyncio


async def worker(barrier: asyncio.Barrier, worker_id: int) -> None:
    """
    Asynchronously waits at a barrier.

    Parameters
    ----------
    barrier : asyncio.Barrier
        The barrier to wait at.
    worker_id : int
        The ID of the worker.

    We'll rely on `main` for the doctest demonstration.
    """
    print(f"Worker {worker_id} waiting at the barrier.")
    # Wait until all tasks reach the barrier
    await barrier.wait()
    print(f"Worker {worker_id} passed the barrier.")


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Creates a barrier for a fixed number of tasks and runs them. A TaskGroup
    supervises the workers as each waits at the barrier until all have arrived,
    ensuring they all reach this synchronization point before proceeding.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Worker ... waiting at the barrier.
    Worker ... waiting at the barrier.
    Worker ... waiting at the barrier.
    Worker ... passed the barrier.
    Worker ... passed the barrier.
    Worker ... passed the barrier.
    All workers have reached the barrier.
    """
    barrier = asyncio.Barrier(3)
    async with asyncio.TaskGroup() as group:
        for i in range(3):
            group.create_task(worker(barrier, i))
    print("All workers have reached the barrier.")


if __name__ == "__main__":
    asyncio.run(main())
