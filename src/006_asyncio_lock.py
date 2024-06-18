#!/usr/bin/env python

import asyncio


class SharedResource:
    def __init__(self) -> None:
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self) -> None:
        async with self.lock:
            temp = self.value
            await asyncio.sleep(0.001)  # Simulate some processing
            self.value = temp + 1


async def worker(resource: SharedResource, increments: int) -> None:
    """Asynchronously increments a shared resource.

    Parameters
    ----------
    resource : SharedResource
        The shared resource to increment.
    increments : int
        The number of increments to perform.

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
    """Asynchronously runs multiple workers to increment a shared resource.

    Examples
    --------
    >>> asyncio.run(main())
    200
    """
    resource = SharedResource()
    increments = 100
    await asyncio.gather(worker(resource, increments), worker(resource, increments))
    print(resource.value)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
