#!/usr/bin/env python

import asyncio


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
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    """
    async with semaphore:
        print(f"Worker {worker_id} is working.")
        await asyncio.sleep(0.001)  # Simulate a task
        print(f"Worker {worker_id} is done.")


async def main() -> None:
    """
    Asynchronously runs multiple workers with limited concurrent access.

    Examples
    --------
    >>> asyncio.run(main())
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    Worker ... is ....
    """
    semaphore = asyncio.Semaphore(2)  # Limit to 2 concurrent workers
    tasks = [asyncio.create_task(limited_worker(semaphore, i)) for i in range(3)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
