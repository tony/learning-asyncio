#!/usr/bin/env python
"""
Creating and Managing Tasks Explicitly.

Context
-------
This lesson shows how to create and manage tasks directly using `asyncio.create_task()`.
Instead of just awaiting coroutines directly, we can schedule them as tasks that run
concurrently. By managing tasks, we can control their lifecycle, await their completion
at a later point, or cancel them if needed.

Summary
-------
- Introduce `asyncio.create_task()` for scheduling coroutines.
- Show how to await tasks for results.
- Demonstrate concurrent execution of multiple tasks and collecting their outcomes.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task

Doctest Notes:
- Output is deterministic.
- We create multiple tasks and await them in order, printing their results.

"""

import asyncio


async def greet(name: str) -> str:
    """
    Asynchronously returns a personalized greeting string.

    Parameters
    ----------
    name : str
        The name to greet.

    Returns
    -------
    str
        A greeting message.

    Examples
    --------
    >>> asyncio.run(greet("Alice"))
    'Hello, Alice!'
    """
    await asyncio.sleep(0.001)  # Simulate I/O-bound operation
    return f"Hello, {name}!"


async def main() -> None:
    """
    Main entrypoint for this lesson.

    Demonstrates creating multiple tasks to run concurrently. We schedule greetings
    for multiple names, then await each task. By using `create_task()`, we give the
    event loop control to manage these coroutines as concurrent tasks, allowing them
    to run simultaneously.

    Examples
    --------
    >>> asyncio.run(main())
    Hello, Alice!
    Hello, Bob!
    Hello, Charlie!
    """
    names = ["Alice", "Bob", "Charlie"]
    tasks = [asyncio.create_task(greet(name)) for name in names]

    # Await each task and print its result as it completes.
    for task in tasks:
        greeting = await task
        print(greeting)


if __name__ == "__main__":
    asyncio.run(main())
