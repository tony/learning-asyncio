#!/usr/bin/env python

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

    Examples
    --------
    >>> asyncio.run(main())
    Worker 0 waiting at the barrier.
    Worker 1 waiting at the barrier.
    Worker 2 waiting at the barrier.
    Worker ... passed the barrier.
    Worker ... passed the barrier.
    Worker ... passed the barrier.
    All workers have reached the barrier.
    """
    print(f"Worker {worker_id} waiting at the barrier.")
    await barrier.wait()
    print(f"Worker {worker_id} passed the barrier.")


async def main() -> None:
    """
    Asynchronously synchronizes coroutines at a barrier.

    Examples
    --------
    >>> asyncio.run(main())
    Worker 0 waiting at the barrier.
    Worker 1 waiting at the barrier.
    Worker 2 waiting at the barrier.
    Worker ... passed the barrier.
    Worker ... passed the barrier.
    Worker ... passed the barrier.
    All workers have reached the barrier.
    """
    barrier = asyncio.Barrier(3)
    tasks = [asyncio.create_task(worker(barrier, i)) for i in range(3)]
    await asyncio.gather(*tasks)
    print("All workers have reached the barrier.")


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
