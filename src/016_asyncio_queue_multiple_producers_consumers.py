#!/usr/bin/env python

"""
This example demonstrates how to use asyncio.Queue with multiple producers and consumers.

It covers creating multiple producers and consumers that work concurrently.
"""

import asyncio
import random


async def producer(queue: asyncio.Queue[str | None], n: int) -> None:
    """
    Asynchronously produces items and puts them in the queue.

    Parameters
    ----------
    queue : asyncio.Queue
        The queue to put items into.
    n : int
        The producer ID.

    Examples
    --------
    >>> asyncio.run(main())
    Producer ... produced ...
    Producer ... produced ...
    Consumer ... consumed Producer ... item ...
    Producer ... produced ...
    Producer ... produced ...
    """
    for i in range(5):
        await asyncio.sleep(random.uniform(0.001, 0.005))
        item = f"Producer {n} item {i}"
        await queue.put(item)
        print(f"Producer {n} produced {i}")


async def consumer(queue: asyncio.Queue[str | None], n: int) -> None:
    """
    Asynchronously consumes items from the queue.

    Parameters
    ----------
    queue : asyncio.Queue
        The queue to consume items from.
    n : int
        The consumer ID.

    Examples
    --------
    >>> asyncio.run(main())
    Producer ... produced ...
    Producer ... produced ...
    Consumer ... consumed Producer ... item ...
    Producer ... produced ...
    Producer ... produced ...
    """
    while True:
        item = await queue.get()
        if item is None:
            break
        await asyncio.sleep(random.uniform(0.001, 0.005))
        print(f"Consumer {n} consumed {item}")
        queue.task_done()


async def main() -> None:
    """
    Asynchronously runs multiple producers and consumers.

    Examples
    --------
    >>> asyncio.run(main())
    Producer ... produced ...
    Producer ... produced ...
    Consumer ... consumed Producer ... item ...
    Producer ... produced ...
    Producer ... produced ...
    """
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    producers = [asyncio.create_task(producer(queue, i)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(2)]

    await asyncio.gather(*producers)
    for _ in consumers:
        await queue.put(None)

    await asyncio.gather(*consumers)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
