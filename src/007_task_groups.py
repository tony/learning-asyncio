#!/usr/bin/env python
"""
Structured Concurrency with TaskGroup.

Context
-------
This lesson introduces `asyncio.TaskGroup`, providing structured concurrency for
coordinating related coroutines. Task groups ensure that child tasks share the same
lifecycle: if one task errors, the entire group is cancelled and exceptions surface as
an `ExceptionGroup`. This pattern is the recommended way to supervise collections of
async work in modern Python.

Summary
-------
- Create task groups with `asyncio.TaskGroup()` and schedule child tasks with
  `create_task()`.
- Wait for all subtasks to finish when the context manager exits.
- Observe how exceptions in one task propagate and cancel sibling tasks automatically.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#task-groups

Doctest Notes:
- We keep delays very short to maintain fast doctest execution.
- Examples demonstrate both successful completion and error handling semantics.
"""

import asyncio


async def fetch_data(name: str, delay: float) -> str:
    """Simulate fetching data asynchronously.

    Parameters
    ----------
    name : str
        Identifier for the data source.
    delay : float
        Artificial delay to simulate I/O latency.

    Examples
    --------
    >>> asyncio.run(fetch_data("alpha", 0.001))
    'alpha'
    """
    await asyncio.sleep(delay)
    return name


async def demonstrate_successful_group() -> list[str]:
    """Run multiple coroutines under a task group and collect their results.

    Returns
    -------
    list[str]
        Completed task results in the order tasks were created.

    Examples
    --------
    >>> asyncio.run(demonstrate_successful_group())
    ['alpha', 'beta']
    """
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(fetch_data("alpha", 0.001)),
            group.create_task(fetch_data("beta", 0.001)),
        ]

    return [task.result() for task in tasks]


async def demonstrate_failure_handling() -> None:
    """Show how TaskGroup cancels remaining tasks when one fails.

    Examples
    --------
    >>> asyncio.run(demonstrate_failure_handling())
    Traceback (most recent call last):
    ...
    ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
    """

    async def faulty() -> None:
        await asyncio.sleep(0.001)
        message = "boom"
        raise RuntimeError(message)

    async def slow() -> None:
        await asyncio.sleep(0.01)

    async with asyncio.TaskGroup() as group:
        group.create_task(faulty())
        group.create_task(slow())


async def main() -> None:
    """Run the main demonstration for this lesson.

    Examples
    --------
    >>> asyncio.run(main())
    TaskGroup results: ['alpha', 'beta']
    """
    results = await demonstrate_successful_group()
    print(f"TaskGroup results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
