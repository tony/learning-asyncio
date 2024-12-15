#!/usr/bin/env python
"""
Introduction to Asynchronous Programming.

Context
-------
This lesson introduces the basic concepts of asynchronous programming in Python using `async` functions and the `await` keyword.
You will learn how to define a simple asynchronous function and execute it using `asyncio.run()`. The goal is to understand the
fundamental building blocks of Python’s async/await syntax before moving on to more complex scenarios.

Summary
-------
- Learn how to define an `async` function.
- Use `await` to pause execution until a coroutine completes.
- Run the coroutine using `asyncio.run()`.
- Observe how async code differs from synchronous code by allowing the event loop to manage execution flow.

Official Documentation:
- https://docs.python.org/3/library/asyncio.html

Doctest Notes:
- The output is deterministic and minimal.
- We rely on a basic async function that returns a value after a small delay.
"""

import asyncio


async def demonstrate_concept() -> str:
    """
    Demonstrates a simple asynchronous function that returns a greeting.

    Unlike a synchronous function which would execute blocking code directly,
    an async function uses `await` to suspend execution until an awaited
    coroutine completes, allowing the event loop to run other tasks in the meantime.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'Hello, async world!'
    """
    await asyncio.sleep(0.001)  # Simulate async I/O or waiting
    return "Hello, async world!"


async def main() -> None:
    """
    Main entrypoint for this lesson.

    Runs the async demonstration function and prints the result.
    This showcases how `asyncio.run()` invokes the event loop, executes `demonstrate_concept()`,
    and returns its result. By using `await`, `main()` can orchestrate asynchronous calls
    without blocking the entire program.

    Examples
    --------
    >>> asyncio.run(main())
    Hello, async world!
    """
    result = await demonstrate_concept()
    print(result)


if __name__ == "__main__":
    # Running the main coroutine to allow standalone execution from the command line.
    asyncio.run(main())
