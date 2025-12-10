#!/usr/bin/env python
"""
Applying Timeouts and Task Cancellations.

Context
-------
This lesson demonstrates how to limit coroutine execution using both
`asyncio.wait_for()` and the modern `asyncio.timeout()` context manager, as well as
how to handle task cancellations gracefully. Timeouts prevent tasks from running
indefinitely, while explicit cancellation lets you stop work that is no longer needed.

Summary
-------
- Use `asyncio.wait_for()` to apply time limits to awaited coroutines.
- Leverage `asyncio.timeout()` / `timeout_at()` for structured timeout management that
  converts cancellations into `TimeoutError`.
- Demonstrate explicit cancellation with `task.cancel()` and how to handle
  `asyncio.CancelledError`.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#timeouts
- https://docs.python.org/3/library/asyncio-task.html#task-cancellation

Doctest Notes:
- We show success and timeout scenarios for both `wait_for()` and the timeout context.
- We also show a scenario with explicit cancellation.

"""

import asyncio


async def task_with_possible_delay(delay: float) -> str:
    """
    Simulate a task that may or may not complete before a timeout.

    Parameters
    ----------
    delay : float
        How long to sleep to simulate work.

    Returns
    -------
    str
        A success message if completed.

    Examples
    --------
    >>> # Completing before timeout using wait_for
    >>> asyncio.run(asyncio.wait_for(task_with_possible_delay(0.001), timeout=0.1))
    'Task completed'
    >>> # Completing before timeout using asyncio.timeout context manager
    >>> asyncio.run(run_with_timeout_context(0.001, 0.1))
    'Task completed'
    >>> # Timing out with wait_for
    >>> try:
    ...     asyncio.run(asyncio.wait_for(task_with_possible_delay(0.1), timeout=0.001))
    ... except asyncio.TimeoutError:
    ...     print("Task timed out")
    Task timed out
    >>> # Timing out with asyncio.timeout
    >>> try:
    ...     asyncio.run(run_with_timeout_context(0.1, 0.001))
    ... except TimeoutError:
    ...     print("Context timed out")
    Context timed out
    """
    await asyncio.sleep(delay)
    return "Task completed"


async def run_with_timeout_context(delay: float, timeout: float) -> str:
    """Run `task_with_possible_delay` inside an `asyncio.timeout()` context."""
    async with asyncio.timeout(timeout):
        return await task_with_possible_delay(delay)


async def main(
    timeout: bool = False,
    cancel: bool = False,
    use_context_timeout: bool = False,
) -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates four scenarios:
    1. Running a task successfully before the timeout (`wait_for` and context).
    2. Timing out a task by using `wait_for()` with a short timeout (`timeout=True`).
    3. Timing out a task with the timeout context manager (`use_context_timeout=True`).
    4. Explicitly cancelling a running task (`cancel=True`).

    Examples
    --------
    >>> asyncio.run(main())
    Wait-for result: Task completed
    Context manager result: Task completed
    >>> asyncio.run(main(timeout=True))
    Task timed out
    >>> asyncio.run(main(use_context_timeout=True))
    Context managed task timed out
    >>> asyncio.run(main(cancel=True))
    Task was cancelled
    """
    try:
        if cancel:
            # Demonstrate explicit cancellation.
            task = asyncio.create_task(task_with_possible_delay(0.1))
            await asyncio.sleep(0.001)  # Let the task start
            task.cancel()
            await task
        elif timeout:
            # This will likely raise asyncio.TimeoutError due to the short timeout.
            result = await asyncio.wait_for(
                task_with_possible_delay(0.002),
                timeout=0.001,
            )
            print(f"Wait-for result: {result}")
        elif use_context_timeout:
            async with asyncio.timeout(0.001):
                await task_with_possible_delay(0.002)
            print("Context manager result: Task completed")
        else:
            # Successful wait_for demonstration.
            wait_for_result = await asyncio.wait_for(
                task_with_possible_delay(0.001),
                timeout=0.1,
            )
            print(f"Wait-for result: {wait_for_result}")

            # Successful context manager demonstration.
            async with asyncio.timeout(0.1):
                context_result = await task_with_possible_delay(0.001)
            print(f"Context manager result: {context_result}")
    except TimeoutError:
        if use_context_timeout:
            print("Context managed task timed out")
        else:
            print("Task timed out")
    except asyncio.CancelledError:
        print("Task was cancelled")


if __name__ == "__main__":
    # Running without timeout or cancellation scenario:
    asyncio.run(main())

    # Running with timeout scenario:
    asyncio.run(main(timeout=True))

    # Running with timeout context scenario:
    asyncio.run(main(use_context_timeout=True))

    # Running with cancellation scenario:
    asyncio.run(main(cancel=True))
