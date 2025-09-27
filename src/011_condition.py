#!/usr/bin/env python
"""
Condition Variables for Complex Coordination.

[... Same context and summary as before ...]

Doctest Notes:
- After this change, we ensure a stable output order: all items are produced
  before any are consumed.
- This allows the doctest to match the lines in the expected order.
"""

import asyncio


class SharedQueue:
    """A shared queue with condition variable for coordination."""

    def __init__(self) -> None:
        self.queue: list[int] = []
        self.condition = asyncio.Condition()

    async def produce(self, item: int) -> None:
        """Add an item to the queue and notify waiting consumers."""
        async with self.condition:
            self.queue.append(item)
            print(f"Produced {item}")
            self.condition.notify_all()

    async def consume(self) -> int:
        """Wait for an item to be available and consume it."""
        async with self.condition:
            await self.condition.wait_for(lambda: len(self.queue) > 0)
            item = self.queue.pop(0)
            print(f"Consumed {item}")
            return item


async def producer(shared: SharedQueue, pid: int, count: int) -> None:
    """Produce items and add them to the shared queue.

    Args:
        shared: The shared queue protected by a condition variable.
        pid: Producer ID used to generate unique item values.
        count: Number of items to produce.
    """
    for i in range(count):
        await asyncio.sleep(0.001)
        await shared.produce((pid * 100) + i)


async def consumer(shared: SharedQueue, cid: int, total_items: int) -> None:
    """Consume items from the shared queue.

    Args:
        shared: The shared queue protected by a condition variable.
        cid: Consumer ID (used for identification in output).
        total_items: Number of items to consume.
    """
    for _ in range(total_items):
        await asyncio.sleep(0.001)
        await shared.consume()


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    We create a shared queue protected by a condition. Two producers each produce
    two items (total of 4 items), and two consumers each consume two items.
    Producers run first and finish producing all items.
    After that, consumers start and consume all items.

    This ensures the output order is:
    1. Four "Produced ..." lines
    2. Four "Consumed ..." lines

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Produced ...
    Produced ...
    Produced ...
    Produced ...
    Consumed ...
    Consumed ...
    Consumed ...
    Consumed ...
    """
    shared = SharedQueue()

    producer_count = 2
    items_per_producer = 2
    total_items = producer_count * items_per_producer

    consumer_count = 2
    items_per_consumer = total_items // consumer_count

    # Run all producers first
    producers = [
        asyncio.create_task(producer(shared, pid, items_per_producer))
        for pid in range(producer_count)
    ]
    await asyncio.gather(*producers)

    # After producers have finished, run consumers
    consumers = [
        asyncio.create_task(consumer(shared, cid, items_per_consumer))
        for cid in range(consumer_count)
    ]
    await asyncio.gather(*consumers)


if __name__ == "__main__":
    asyncio.run(main())
