#!/usr/bin/env python

import asyncio


async def waiter(event: asyncio.Event) -> None:
    """Asynchronously waits for an event to be set.

    Parameters
    ----------
    event : asyncio.Event
        The event to wait for.

    Examples
    --------
    >>> asyncio.run(main())
    Waiting for event to be set...
    Event is set!
    Event triggered!
    """
    print("Waiting for event to be set...")
    await event.wait()
    print("Event triggered!")


async def main() -> None:
    """Asynchronously sets and waits for an event.

    Examples
    --------
    >>> asyncio.run(main())
    Waiting for event to be set...
    Event is set!
    Event triggered!
    """
    event = asyncio.Event()
    waiter_task = asyncio.create_task(waiter(event))

    await asyncio.sleep(0.001)  # Simulate a delay
    print("Event is set!")
    event.set()

    await waiter_task


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
