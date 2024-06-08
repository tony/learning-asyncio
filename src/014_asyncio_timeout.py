#!/usr/bin/env python
"""This example demonstrates how to use asyncio to apply timeouts to tasks.

It covers using asyncio.wait_for to set time limits on coroutines.
"""

import asyncio


async def task_with_timeout() -> str:
    """Asynchronously performs a task with a timeout.

    Returns
    -------
    str
        The result of the task or a timeout message.

    Examples
    --------
    >>> asyncio.run(main())
    Task completed
    >>> asyncio.run(main(timeout=True))
    Task timed out
    """
    try:
        await asyncio.sleep(0.002)
        return "Task completed"
    except TimeoutError:
        return "Task timed out"


async def main(timeout: bool = False) -> None:
    """Asynchronously runs a task with or without a timeout.

    Parameters
    ----------
    timeout : bool, optional
        Whether to enforce a timeout on the task, by default False.

    Examples
    --------
    >>> asyncio.run(main())
    Task completed
    >>> asyncio.run(main(timeout=True))
    Task timed out
    """
    if timeout:
        try:
            result = await asyncio.wait_for(task_with_timeout(), timeout=0.001)
        except TimeoutError:
            result = "Task timed out"
    else:
        result = await task_with_timeout()
    print(result)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
