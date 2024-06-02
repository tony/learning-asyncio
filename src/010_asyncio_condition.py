#!/usr/bin/env python

import asyncio


class SharedState:
    def __init__(self) -> None:
        self.state = 0
        self.condition = asyncio.Condition()

    async def increment(self) -> None:
        async with self.condition:
            self.state += 1
            self.condition.notify_all()

    async def wait_for_value(self, value: int) -> None:
        async with self.condition:
            await self.condition.wait_for(lambda: self.state >= value)


async def main() -> None:
    """
    Asynchronously uses a condition to synchronize coroutines.

    Examples
    --------
    >>> asyncio.run(main())
    State reached the target value: 3
    """
    shared_state = SharedState()

    async def incrementer() -> None:
        for _ in range(3):
            await asyncio.sleep(0.1)
            await shared_state.increment()

    async def waiter() -> None:
        await shared_state.wait_for_value(3)
        print(f"State reached the target value: {shared_state.state}")

    await asyncio.gather(incrementer(), waiter())


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
