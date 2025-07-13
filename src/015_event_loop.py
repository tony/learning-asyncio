#!/usr/bin/env python
"""
Understanding the Event Loop.

Context
-------
This lesson dives into the internals of the asyncio event loop. The event loop is the core
of asyncio, orchestrating the execution of coroutines, scheduling callbacks, handling I/O events,
and integrating with lower-level OS primitives such as selectors.

Key concepts:
- The event loop runs the “event loop cycle”: selecting which tasks are ready to run,
  running them until they block (e.g., await I/O), and then switching to other pending tasks.
- `asyncio.get_running_loop()` gives you direct access to the currently running loop.
- Event loop policies and custom loops allow you to replace or configure the default loop.
- Low-level APIs let you add callbacks, integrate with OS-level asynchronous I/O, or customize event handling.

Summary
-------
- Learn how to get the running event loop with `asyncio.get_running_loop()`.
- Understand that the event loop manages tasks, callbacks, and I/O asynchronously.
- Explore event loop methods like `call_soon()` and `call_later()` for scheduling callbacks.
- Demonstrate how the event loop selects tasks to run and how they are interleaved.

Official Documentation:
- https://docs.python.org/3/library/asyncio-eventloop.html
- https://docs.python.org/3/library/asyncio-policy.html

Doctest Notes:
- We will show how to access the current event loop and schedule a callback.
- The exact timing of callbacks can vary, so we may use ellipses in doctests.
- Because this lesson involves internal mechanisms, some outputs may be more illustrative than strictly tested.

"""

import asyncio


async def simple_coroutine() -> str:
    """
    Return a fixed message after a short delay.

    This gives the event loop time to run and potentially execute scheduled callbacks.

    Examples
    --------
    >>> result = asyncio.run(simple_coroutine())
    >>> result
    'Completed'
    """
    await asyncio.sleep(0.001)
    return "Completed"


def callback_function() -> None:
    """Print a message when scheduled on the event loop."""
    print("Callback executed.")


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates:
    1. Accessing the running event loop.
    2. Scheduling callbacks that run soon, after the current iteration of the loop.
    3. Running a coroutine to observe interplay between scheduled callbacks and coroutine execution.
    4. Inspecting event loop methods.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Event loop: <_UnixSelectorEventLoop ...>
    Scheduling a callback...
    Callback executed.
    Coroutine result: Completed
    """
    loop = asyncio.get_running_loop()
    print(f"Event loop: {loop!r}")

    print("Scheduling a callback...")
    # Schedule a callback to be executed at the next iteration of the event loop.
    loop.call_soon(callback_function)

    # Run a coroutine to show how the loop manages both coroutines and callbacks.
    result = await simple_coroutine()
    print(f"Coroutine result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
