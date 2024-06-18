#!/usr/bin/env python

"""
This example demonstrates how to use asyncio.Condition for multiple producers and consumers.

It covers using conditions to synchronize multiple producers and consumers.
"""

import asyncio


class SharedQueue:
    def __init__(self) -> None:
        self.queue: list[str | None] = []
        self.condition = asyncio.Condition()

    async def produce(self, item: str) -> None:
        """Asynchronously adds an item to the shared queue.

        Parameters
        ----------
        item : int
            The item to add.

        Examples
        --------
        >>> asyncio.run(main())
        Produced Producer ... item ...
        Produced Producer ... item ...
        ... ... item ...
        ... ... item ...
        ... ... item ...
        ... ... item ...
        ... ... item ...
        """
        async with self.condition:
            self.queue.append(item)
            print(f"Produced {item}")
            self.condition.notify_all()

    async def consume(self) -> str | None:
        """Asynchronously consumes an item from the shared queue.

        Returns
        -------
        int
            The consumed item.

        Examples
        --------
        >>> asyncio.run(main())
        Produced Producer ... item ...
        Produced Producer ... item ...
        ... ... item ...
        ... ... item ...
        ... ... item ...
        ... ... item ...
        ... ... item ...
        """
        async with self.condition:
            while not self.queue:
                await self.condition.wait()
            item = self.queue.pop(0)
            print(f"Consumed {item}")
            return item


async def main() -> None:
    """Asynchronously runs multiple producers and consumers using a shared queue.

    Examples
    --------
    >>> asyncio.run(main())
    Produced Producer ... item ...
    Produced Producer ... item ...
    ... ... item ...
    ... ... item ...
    ... ... item ...
    ... ... item ...
    ... ... item ...
    """
    shared_queue = SharedQueue()

    async def producer(id: int) -> None:
        for i in range(2):
            await shared_queue.produce(f"Producer {id} item {i}")
            await asyncio.sleep(0.001)

    async def consumer(id: int) -> None:
        for _ in range(2):
            await shared_queue.consume()
            await asyncio.sleep(0.001)

    producers = [asyncio.create_task(producer(i)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(i)) for i in range(2)]

    await asyncio.gather(*producers)
    await asyncio.gather(*consumers)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
