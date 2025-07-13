#!/usr/bin/env python
"""
Applying Timeouts and Task Cancellations.

Context
-------
This lesson demonstrates how to use `asyncio.wait_for()` to limit the execution time of a task,
as well as how to handle task cancellations gracefully. Timeouts are one way to stop a task
from running indefinitely, while explicit cancellation allows you to cancel tasks that are no
longer needed.

Summary
-------
- Use `asyncio.wait_for()` to apply time limits to tasks.
- Handle `asyncio.TimeoutError` to gracefully manage long-running tasks.
- Demonstrate explicit cancellation with `task.cancel()` and how to handle `asyncio.CancelledError`.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#timeouts
- https://docs.python.org/3/library/asyncio-task.html#task-cancellation

Doctest Notes:
- We show two scenarios with timeouts (one succeeds, one times out).
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

    Raises
    ------
    asyncio.TimeoutError
        If the task takes longer than the imposed timeout (when wrapped in `wait_for`).

    Examples
    --------
    >>> # Completing before timeout
    >>> asyncio.run(asyncio.wait_for(task_with_possible_delay(0.001), timeout=0.1))
    'Task completed'
    >>> # Timing out
    >>> try:
    ...     asyncio.run(asyncio.wait_for(task_with_possible_delay(0.1), timeout=0.001))
    ... except asyncio.TimeoutError:
    ...     print("Task timed out")
    Task timed out
    """
    await asyncio.sleep(delay)
    return "Task completed"


async def main(timeout: bool = False, cancel: bool = False) -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates three scenarios:
    1. Running a task successfully before the timeout (default).
    2. Timing out a task by using `wait_for()` with a short timeout (timeout=True).
    3. Explicitly cancelling a running task (cancel=True).

    Examples
    --------
    >>> asyncio.run(main())
    Task completed
    >>> asyncio.run(main(timeout=True))
    Task timed out
    >>> asyncio.run(main(cancel=True))
    Task was cancelled
    """
    try:
        if cancel:
            # Demonstrate explicit cancellation.
            task = asyncio.create_task(task_with_possible_delay(0.1))
            await asyncio.sleep(0.001)  # Let the task start
            task.cancel()  # Explicitly cancel the task
            await task
        elif timeout:
            # This will likely raise asyncio.TimeoutError due to the short timeout.
            result = await asyncio.wait_for(
                task_with_possible_delay(0.002),
                timeout=0.001,
            )
            print(result)
        else:
            # This should complete successfully.
            result = await asyncio.wait_for(
                task_with_possible_delay(0.001),
                timeout=0.1,
            )
            print(result)
    except TimeoutError:
        print("Task timed out")
    except asyncio.CancelledError:
        print("Task was cancelled")


if __name__ == "__main__":
    # Running without timeout or cancellation scenario:
    asyncio.run(main())

    # Running with timeout scenario:
    asyncio.run(main(timeout=True))

    # Running with cancellation scenario:
    asyncio.run(main(cancel=True))
