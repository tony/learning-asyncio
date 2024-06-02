#!/usr/bin/env python

import asyncio


async def producer(queue: asyncio.Queue, n: int) -> None:
    """
    Asynchronously produces items and puts them in the queue.

    Parameters
    ----------
    queue : asyncio.Queue
        The queue to put items into.
    n : int
        The number of items to produce.

    Examples
    --------
    >>> asyncio.run(main())
    Produced 0
    Produced 1
    Consumed 0
    Produced 2
    Consumed 1
    Consumed 2
    """
    for i in range(n):
        await asyncio.sleep(0.001)  # Simulate a delay in producing
        await queue.put(i)
        print(f"Produced {i}")


async def consumer(queue: asyncio.Queue, n: int) -> None:
    """
    Asynchronously consumes items from the queue.

    Parameters
    ----------
    queue : asyncio.Queue
        The queue to consume items from.
    n : int
        The number of items to consume.

    Examples
    --------
    >>> asyncio.run(main())
    Produced 0
    Produced 1
    Consumed 0
    Produced 2
    Consumed 1
    Consumed 2
    """
    for _ in range(n):
        item = await queue.get()
        await asyncio.sleep(0.001)  # Simulate a delay in consuming
        print(f"Consumed {item}")
        queue.task_done()


async def main() -> None:
    """
    Asynchronously runs the producer and consumer coroutines.

    Examples
    --------
    >>> asyncio.run(main())
    Produced 0
    Produced 1
    Consumed 0
    Produced 2
    Consumed 1
    Consumed 2
    """
    queue = asyncio.Queue()
    n = 3
    producer_task = asyncio.create_task(producer(queue, n))
    consumer_task = asyncio.create_task(consumer(queue, n))
    await asyncio.gather(producer_task, consumer_task)
    await queue.join()  # Wait until the queue is fully processed


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
