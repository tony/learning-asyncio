#!/usr/bin/env python
"""
Awaiting and Returning Values.

Context
-------
This lesson builds on the initial introduction to asynchronous programming by showing
how to await other coroutines and handle returned values. By passing arguments to
async functions and awaiting their results, we can create chains of dependent tasks,
allowing for more complex and dynamic async workflows.

Summary
-------
- Introduce calling one async function from another.
- Show how to pass arguments to async functions and await their results.
- Demonstrate how the return value of an awaited coroutine can be used to influence
  subsequent logic.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html

Doctest Notes:
- The output is deterministic.
- We rely on a simple async function that returns a greeting message, which can be
  awaited multiple times with different inputs.
"""

import asyncio


async def greet(name: str) -> str:
    """Return a personalized greeting message asynchronously.

    Parameters
    ----------
    name : str
        The name to greet.

    Examples
    --------
    >>> asyncio.run(greet("Alice"))
    'Hello, Alice!'
    """
    await asyncio.sleep(0.001)  # Simulate async I/O or waiting
    return f"Hello, {name}!"


async def main() -> None:
    """Run the main demonstration for this lesson.

    Demonstrates calling `greet()` from another async function multiple times with
    different arguments. By awaiting each call, we can confirm that the returned values
    are immediately available to use or print, effectively chaining async calls.

    Examples
    --------
    >>> asyncio.run(main())
    Hello, Alice!
    Hello, Bob!
    """
    result_alice = await greet("Alice")
    print(result_alice)

    result_bob = await greet("Bob")
    print(result_bob)


if __name__ == "__main__":
    asyncio.run(main())
