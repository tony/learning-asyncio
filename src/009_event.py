#!/usr/bin/env python
"""
Event Signaling Between Coroutines.

Context
-------
This lesson illustrates how to use `asyncio.Event` to signal state changes
between coroutines. An `Event` allows one coroutine to wait for a certain
condition to occur, while another coroutine, when it completes its work or
reaches a certain state, can set the event. This enables event-driven
synchronization patterns where tasks can efficiently wait for signals instead
of constantly polling.

Summary
-------
- Introduce `asyncio.Event` for signaling between coroutines.
- Show how one task can block until another sets the event, effectively
  "waking" the waiting task.
- Demonstrate a simple event-driven workflow where the timing and order of
  tasks are controlled by events.

Official Documentation:
- https://docs.python.org/3/library/asyncio-sync.html#asyncio.Event

Doctest Notes:
- The order of printed messages is deterministic here because the waiter will
  always print first, then block, and only after the setter sets the event will
  the waiter proceed. We use a short sleep in the setter to simulate delay.
"""

import asyncio


async def setter(event: asyncio.Event) -> None:
    """
    Asynchronously sets an event after a brief delay.

    This simulates another task that, after completing some work, signals that
    the waiting task can proceed by calling `event.set()`.

    We'll rely on `main` for the doctest demonstration.
    """
    await asyncio.sleep(0.001)  # Simulate asynchronous work before signaling
    print("Setter: Event is now set.")
    event.set()


async def waiter(event: asyncio.Event) -> None:
    """
    Asynchronously waits for an event to be set before proceeding.

    The waiter blocks until `event.set()` is called, demonstrating how tasks can wait
    for signals without busy-waiting.

    We'll rely on `main` for the doctest demonstration.
    """
    print("Waiter: Waiting for the event...")
    await event.wait()
    print("Waiter: Event was set, continuing!")


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates event signaling by creating a waiter task that waits on an event,
    and a setter task that sets the event after a delay. Once the event is set,
    the waiter proceeds.

    Examples
    --------
    >>> asyncio.run(main())
    Waiter: Waiting for the event...
    Setter: Event is now set.
    Waiter: Event was set, continuing!
    """
    event = asyncio.Event()

    waiter_task = asyncio.create_task(waiter(event))
    setter_task = asyncio.create_task(setter(event))

    # Wait for both tasks to complete
    await asyncio.gather(waiter_task, setter_task)


if __name__ == "__main__":
    asyncio.run(main())
