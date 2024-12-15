#!/usr/bin/env python
"""
Running Coroutines Concurrently.

Context
-------
This lesson introduces running multiple coroutines concurrently using `asyncio.gather()`.
While async code does not run tasks in parallel on multiple CPU cores, it can efficiently
interleave I/O-bound operations. By concurrently waiting for multiple asynchronous tasks,
your code can handle more tasks in the same amount of time compared to running them sequentially.

Summary
-------
- Demonstrates how to use `asyncio.gather()` to run multiple tasks at once.
- Explains the difference between concurrency (interleaving tasks) and parallelism (executing tasks simultaneously).
- Shows how async code excels at handling I/O-bound operations.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#asyncio.gather

Doctest Notes:
- The output order is deterministic because we print results after `gather()` completes.
- We’ll await multiple coroutines and then iterate over the results.

"""

import asyncio


async def greet(name: str) -> str:
    """
    Asynchronously returns a personalized greeting string.

    Parameters
    ----------
    name : str
        The name to greet.

    Examples
    --------
    >>> asyncio.run(greet("Alice"))
    'Hello, Alice!'
    """
    await asyncio.sleep(0.001)  # Simulate I/O-bound task
    return f"Hello, {name}!"


async def main() -> None:
    """
    Main entrypoint for this lesson.

    Uses `asyncio.gather()` to run multiple greet coroutines concurrently. Each coroutine
    simulates an I/O wait via `sleep()`, but running them together allows the event loop
    to interleave their execution. Once all are completed, we print their results.

    Examples
    --------
    >>> asyncio.run(main())
    Hello, Alice!
    Hello, Bob!
    Hello, Charlie!
    """
    names = ["Alice", "Bob", "Charlie"]
    greetings = await asyncio.gather(*(greet(name) for name in names))
    for greeting in greetings:
        print(greeting)


if __name__ == "__main__":
    asyncio.run(main())
