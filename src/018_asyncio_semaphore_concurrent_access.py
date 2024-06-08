#!/usr/bin/env python

"""
This example demonstrates how to use asyncio.Semaphore to limit concurrent access to a resource.

It covers creating tasks that are limited by a semaphore to control the number of concurrent executions.
"""

import asyncio
import random


async def limited_worker(semaphore: asyncio.Semaphore, worker_id: int) -> None:
    """
    Asynchronously performs a task with limited concurrent access.

    Parameters
    ----------
    semaphore : asyncio.Semaphore
        The semaphore to control access.
    worker_id : int
        The ID of the worker.

    Examples
    --------
    >>> asyncio.run(main())
    Worker 0 is working.
    Worker 1 is working.
    Worker 2 is working.
    Worker 0 is done.
    Worker 1 is done.
    Worker 2 is done.
    """
    async with semaphore:
        print(f"Worker {worker_id} is working.")
        await asyncio.sleep(random.uniform(0.1, 0.5))
        print(f"Worker {worker_id} is done.")


async def main() -> None:
    """
    Asynchronously runs multiple workers with limited concurrent access.

    Examples
    --------
    >>> asyncio.run(main())
    Worker 0 is working.
    Worker 1 is working.
    Worker 2 is working.
    Worker 0 is done.
    Worker 1 is done.
    Worker 2 is done.
    """
    semaphore = asyncio.Semaphore(2)
    tasks = [asyncio.create_task(limited_worker(semaphore, i)) for i in range(3)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
