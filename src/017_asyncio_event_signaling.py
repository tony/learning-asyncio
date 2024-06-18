#!/usr/bin/env python

"""
This example demonstrates how to use asyncio.Event for signaling between coroutines.

It covers setting an event in one coroutine and waiting for the event in another coroutine.
"""

import asyncio


async def setter(event: asyncio.Event) -> None:
    """
    Asynchronously sets an event after a delay.

    Parameters
    ----------
    event : asyncio.Event
        The event to set.

    Examples
    --------
    >>> asyncio.run(main())
    Waiting for the event to be set...
    Event has been set.
    """
    await asyncio.sleep(0.001)
    event.set()
    print("Event has been set.")


async def waiter(event: asyncio.Event) -> None:
    """
    Asynchronously waits for an event to be set.

    Parameters
    ----------
    event : asyncio.Event
        The event to wait for.

    Examples
    --------
    >>> asyncio.run(main())
    Waiting for the event to be set...
    Event has been set.
    """
    print("Waiting for the event to be set...")
    await event.wait()
    print("Event has been set.")


async def main() -> None:
    """
    Asynchronously sets and waits for an event.

    Examples
    --------
    >>> asyncio.run(main())
    Waiting for the event to be set...
    Event has been set.
    Event has been set.
    """
    event = asyncio.Event()
    setter_task = asyncio.create_task(setter(event))
    waiter_task = asyncio.create_task(waiter(event))

    await asyncio.gather(setter_task, waiter_task)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
