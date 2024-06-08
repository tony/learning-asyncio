#!/usr/bin/env python

"""
This example demonstrates how to use asyncio.Condition for implementing
a producer-consumer pattern.

It covers using conditions to synchronize the producer and consumer coroutines.
"""

import asyncio


class SharedResource:
    def __init__(self) -> None:
        self.queue: list[int] = []
        self.condition = asyncio.Condition()

    async def produce(self, item: int) -> None:
        """
        Asynchronously adds an item to the shared resource.

        Parameters
        ----------
        item : int
            The item to add.

        Examples
        --------
        >>> asyncio.run(main())
        Produced 1
        Consumed 1
        Produced 2
        Consumed 2
        """
        async with self.condition:
            self.queue.append(item)
            print(f"Produced {item}")
            self.condition.notify_all()

    async def consume(self) -> int:
        """
        Asynchronously consumes an item from the shared resource.

        Returns
        -------
        int
            The consumed item.

        Examples
        --------
        >>> asyncio.run(main())
        Produced 1
        Consumed 1
        Produced 2
        Consumed 2
        """
        async with self.condition:
            while not self.queue:
                await self.condition.wait()
            item = self.queue.pop(0)
            print(f"Consumed {item}")
            return item


async def main() -> None:
    """
    Asynchronously runs producer and consumer coroutines.

    Examples
    --------
    >>> asyncio.run(main())
    Produced 1
    Consumed 1
    Produced 2
    Consumed 2
    """
    resource = SharedResource()

    async def producer() -> None:
        for i in range(1, 3):
            await resource.produce(i)
            await asyncio.sleep(0.5)

    async def consumer() -> None:
        for _ in range(2):
            await resource.consume()
            await asyncio.sleep(1)

    await asyncio.gather(producer(), consumer())


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
