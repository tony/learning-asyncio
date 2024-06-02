#!/usr/bin/env python

import asyncio


class SharedQueue:
    def __init__(self) -> None:
        self.queue = []
        self.condition = asyncio.Condition()

    async def produce(self, item: int) -> None:
        async with self.condition:
            self.queue.append(item)
            print(f"Produced {item}")
            self.condition.notify()

    async def consume(self) -> None:
        async with self.condition:
            while not self.queue:
                await self.condition.wait()
            item = self.queue.pop(0)
            print(f"Consumed {item}")


async def producer(shared_queue: SharedQueue, items: int) -> None:
    for i in range(items):
        await asyncio.sleep(0.001)
        await shared_queue.produce(i)


async def consumer(shared_queue: SharedQueue, items: int) -> None:
    for _ in range(items):
        await shared_queue.consume()


async def main() -> None:
    """
    Asynchronously runs producer and consumer coroutines with a shared condition.

    Examples
    --------
    >>> asyncio.run(main())
    Produced 0
    Consumed 0
    Produced 1
    Consumed 1
    Produced 2
    Consumed 2
    """
    shared_queue = SharedQueue()
    items = 3
    producer_task = asyncio.create_task(producer(shared_queue, items))
    consumer_task = asyncio.create_task(consumer(shared_queue, items))
    await asyncio.gather(producer_task, consumer_task)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
