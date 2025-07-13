#!/usr/bin/env python
"""
Queue-Based Producer-Consumer Patterns.

Context
-------
This lesson demonstrates how to implement producer-consumer patterns using `asyncio.Queue`.
Queues provide a safe, built-in way to transfer data between coroutines without manual
synchronization. By using an `asyncio.Queue`, we can have multiple producers enqueueing
items and multiple consumers dequeuing them, all concurrently. As workloads grow, we can
easily scale up the number of producers and consumers to handle larger demands.

Summary
-------
- Introduce `asyncio.Queue` for producer-consumer communication.
- Show how multiple producers and consumers can run concurrently, feeding and draining the queue.
- Understand how queues simplify synchronization in asynchronous workflows.

Official Documentation:
- https://docs.python.org/3/library/asyncio-queue.html

Doctest Notes:
- Due to concurrency, the exact sequence of produced and consumed items may vary.
- We will use ellipses in each line of the doctest output to allow for any order of production and consumption.
- The key is that there will be four "Produced" lines and four "Consumed by ..." lines, but their interleaving may differ.
"""

import asyncio


async def producer(
    queue: asyncio.Queue[tuple[int, int] | None],
    n: int,
    producer_id: int,
) -> None:
    """Produce items and put them into the queue."""
    for i in range(n):
        await asyncio.sleep(0.001)  # Simulate production time
        item = (producer_id, i)
        await queue.put(item)
        print(f"Produced {item}")


async def consumer(
    queue: asyncio.Queue[tuple[int, int] | None],
    consumer_id: int,
) -> None:
    """Consume items from the queue until None is received."""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        await asyncio.sleep(0.001)  # Simulate consumption time
        print(f"Consumed by {consumer_id}: {item}")
        queue.task_done()


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Creates multiple producers and consumers. After all producers finish,
    sends a sentinel (None) to signal consumers to stop. The output lines
    may appear in various orders due to concurrency.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Produced ...
    Produced ...
    Produced ...
    Produced ...
    Consumed by ...
    Consumed by ...
    Consumed by ...
    Consumed by ...
    """
    # Updated queue annotation to accept tuples or None
    queue: asyncio.Queue[tuple[int, int] | None] = asyncio.Queue()

    producer_count = 2
    consumer_count = 2
    items_per_producer = 2

    producers = [
        asyncio.create_task(producer(queue, items_per_producer, pid))
        for pid in range(producer_count)
    ]
    consumers = [
        asyncio.create_task(consumer(queue, cid)) for cid in range(consumer_count)
    ]

    await asyncio.gather(*producers)

    # Signal consumers to stop
    for _ in range(consumer_count):
        await queue.put(None)

    await queue.join()

    # Cancel any consumer tasks if still running (they should have exited after sentinel)
    for c in consumers:
        if not c.done():
            c.cancel()

    await asyncio.gather(*consumers, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
