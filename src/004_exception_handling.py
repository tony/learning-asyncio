#!/usr/bin/env python
"""
Handling Exceptions in Async Code.

Context
-------
This lesson demonstrates how to handle exceptions in asynchronous code. Instead of
letting errors crash your program, you can use `try/except` blocks around `await`
calls to catch and handle exceptions gracefully. This is especially important when
dealing with multiple tasks, where a single failing coroutine shouldn't necessarily
stop the entire async workflow.

Summary
-------
- Show how a coroutine can raise exceptions.
- Demonstrate wrapping `await` calls in `try/except` to handle errors.
- Illustrate graceful recovery or logging of errors without halting other tasks.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#task-exceptions
- https://docs.python.org/3/tutorial/errors.html

Doctest Notes:
- The doctest shows successful handling of a passing scenario and catching an
  exception from a failing scenario.
- Output is deterministic and minimal.

"""

import asyncio


async def may_fail(succeed: bool) -> str:
    """
    Asynchronously returns a success message or raises an exception based on the input.

    Parameters
    ----------
    succeed : bool
        Determines if the coroutine should succeed or fail.

    Returns
    -------
    str
        'Success!' if succeed is True.

    Raises
    ------
    ValueError
        If succeed is False.

    Examples
    --------
    >>> asyncio.run(may_fail(True))
    'Success!'
    >>> asyncio.run(may_fail(False))
    Traceback (most recent call last):
    ...
    ValueError: Failure!
    """
    if succeed:
        return "Success!"
    msg = "Failure!"
    raise ValueError(msg)


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates exception handling by calling `may_fail()` twice:
    - First with succeed=True, which should print "Success!"
    - Then with succeed=False, which we catch and print a custom error message for,
      preventing the exception from crashing our entire async code.

    Examples
    --------
    >>> asyncio.run(main())
    Success!
    Caught an exception: Failure!
    """
    try:
        result = await may_fail(True)
        print(result)
        # The next call is expected to fail, so we handle it gracefully.
        result = await may_fail(False)
        print(result)
    except ValueError as e:
        print(f"Caught an exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
