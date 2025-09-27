#!/usr/bin/env python
"""
Advanced Scheduling and Executors.

Context
-------
This lesson shows how to integrate `asyncio` with executors to offload
CPU-bound tasks from the event loop and compares scheduling helpers for
coordinating async workloads. While asyncio excels at managing I/O-bound
concurrency, CPU-bound tasks can block the event loop and degrade
responsiveness. By running them in a thread or process pool, the event loop can
continue handling I/O while the CPU-bound work executes elsewhere. For
high-level coordination, we also contrast `asyncio.gather()`,
`asyncio.TaskGroup`, and the emerging `asyncio.staggered_race()` pattern so you
can choose the right supervision strategy.

Key Concepts:
- `asyncio.run_in_executor()` schedules a blocking function call in a thread or
  process pool.
- For CPU-bound tasks, a process pool may be more efficient (to avoid GIL contention).
- For I/O-bound tasks (like file or network I/O that isn't async), a thread
  pool might suffice.
- The event loop manages scheduling both coroutines and executor-backed tasks, ensuring
  the main thread remains responsive.

Summary
-------
- Demonstrate using `asyncio.run_in_executor()` to run a CPU-bound function.
- Show how to use both thread and process pools with asyncio.
- Compare `asyncio.gather()`, `asyncio.TaskGroup`, and a staggered race helper
  for supervising async workflows.
- Understand when to offload tasks to avoid blocking the event loop.

Official Documentation:
- https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
- https://docs.python.org/3/library/concurrent.futures.html
- https://docs.python.org/3/library/asyncio-task.html#asyncio.gather
- https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup
- https://docs.python.org/3/library/asyncio-task.html#asyncio.staggered_race

Doctest Notes:
- We'll show a CPU-bound function (like calculating Fibonacci numbers) running
  in executors.
- Output order may vary slightly, so we use ellipses to allow flexibility.
- Scheduling comparisons keep delays tiny to maintain fast doctests.
- The staggered race example falls back to a compatibility helper if
  `asyncio.staggered_race` is unavailable (e.g., Python 3.13).

"""

import asyncio
import concurrent.futures
import multiprocessing
from collections.abc import Callable, Coroutine, Iterable
from functools import partial
from typing import Any, cast

_HAS_STAGGERED_RACE = hasattr(asyncio, "staggered_race")


def cpu_bound_fib(n: int) -> int:
    """
    Calculate fibonacci number to simulate a heavy computation.

    Parameters
    ----------
    n : int
        The position in the Fibonacci sequence.

    Returns
    -------
    int
        The nth Fibonacci number.

    For demonstration, we use a slow, naive recursion:
    fib(0)=0, fib(1)=1, fib(n)=fib(n-1)+fib(n-2)
    """
    if n < 2:
        return n
    return cpu_bound_fib(n - 1) + cpu_bound_fib(n - 2)


async def simulate_service(name: str, delay: float, *, fail: bool = False) -> str:
    """Return a service name after a tiny delay, optionally raising.

    Examples
    --------
    >>> asyncio.run(simulate_service("primary", 0.001))
    'primary'
    >>> asyncio.run(simulate_service("primary", 0.001, fail=True))
    Traceback (most recent call last):
    ...
    RuntimeError: primary unavailable
    """
    await asyncio.sleep(delay)
    if fail:
        message = f"{name} unavailable"
        raise RuntimeError(message)
    return name


async def gather_service_statuses() -> list[str]:
    """Collect service responses with ``asyncio.gather``.

    Examples
    --------
    >>> asyncio.run(gather_service_statuses())
    ['primary', 'secondary', 'tertiary']
    """
    return list(
        await asyncio.gather(
            simulate_service("primary", 0.003),
            simulate_service("secondary", 0.002),
            simulate_service("tertiary", 0.001),
        ),
    )


async def taskgroup_service_statuses() -> list[str]:
    """Collect service responses with ``asyncio.TaskGroup``.

    Examples
    --------
    >>> asyncio.run(taskgroup_service_statuses())
    ['primary', 'secondary', 'tertiary']
    """
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(simulate_service("primary", 0.003)),
            group.create_task(simulate_service("secondary", 0.002)),
            group.create_task(simulate_service("tertiary", 0.001)),
        ]
    return [task.result() for task in tasks]


ServiceFactory = Callable[[], Coroutine[Any, Any, str]]


async def run_staggered_race(
    factories: Iterable[ServiceFactory],
    *,
    interval: float = 0.001,
) -> str:
    """Return the first successful result from staggered service attempts.

    Falls back to a compatibility helper when ``asyncio.staggered_race`` is not
    yet available (e.g., Python 3.13).

    Examples
    --------
    >>> # The fastest healthy service wins once the primary fails.
    >>> factories = [
    ...     partial(simulate_service, "primary", 0.001, fail=True),
    ...     partial(simulate_service, "secondary", 0.002),
    ...     partial(simulate_service, "tertiary", 0.003),
    ... ]
    >>> asyncio.run(run_staggered_race(factories))
    'secondary'
    """
    factory_list = list(factories)
    if not factory_list:
        message = "staggered race requires at least one candidate"
        raise ValueError(message)
    if _HAS_STAGGERED_RACE:
        awaitables = [factory() for factory in factory_list]
        staggered_race = cast(
            "Callable[..., Coroutine[Any, Any, str]]",
            asyncio.staggered_race,  # type: ignore[attr-defined]
        )
        return await staggered_race(*awaitables, interval=interval)
    return await _fallback_staggered_race(factory_list, interval=interval)


async def _fallback_staggered_race(
    factories: list[ServiceFactory],
    *,
    interval: float,
) -> str:
    """Minimal ``asyncio.staggered_race`` compatibility shim."""
    tasks: list[asyncio.Task[str]] = []
    for index, factory in enumerate(factories):
        tasks.append(asyncio.create_task(factory()))
        if index != len(factories) - 1:
            await asyncio.sleep(interval)

    pending: set[asyncio.Task[str]] = set(tasks)
    try:
        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in done:
                try:
                    result = task.result()
                except Exception:
                    continue
                for pending_task in pending:
                    pending_task.cancel()
                await asyncio.gather(*pending, return_exceptions=True)
                return result
        message = "All staggered tasks failed"
        raise RuntimeError(message)
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def demonstrate_scheduling_strategies() -> dict[str, str | list[str]]:
    """Return outcomes for gather, TaskGroup, and staggered race patterns.

    Examples
    --------
    >>> summary = asyncio.run(demonstrate_scheduling_strategies())
    >>> summary['gather']
    ['primary', 'secondary', 'tertiary']
    >>> summary['staggered_winner']
    'secondary'
    """
    gather_result = await gather_service_statuses()
    taskgroup_result = await taskgroup_service_statuses()
    factories = [
        partial(simulate_service, "primary", 0.001, fail=True),
        partial(simulate_service, "secondary", 0.002),
        partial(simulate_service, "tertiary", 0.003),
    ]
    winner = await run_staggered_race(factories)
    return {
        "gather": gather_result,
        "taskgroup": taskgroup_result,
        "staggered_winner": winner,
    }


async def run_in_thread_pool(func: Callable[[int], int], arg: int) -> int:
    """Run a CPU-bound function in a thread pool executor."""
    loop = asyncio.get_running_loop()
    # By default, run_in_executor() uses the default thread pool.
    return await loop.run_in_executor(None, func, arg)


async def run_in_process_pool(func: Callable[[int], int], arg: int) -> int:
    """Run a CPU-bound function in a process pool executor."""
    loop = asyncio.get_running_loop()
    # Create a dedicated process pool for demonstration.
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, arg)


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates running CPU-bound tasks in both a thread pool (default
    executor) and a process pool. By doing so, the event loop can remain
    responsive to async tasks.

    We calculate a Fibonacci number in both a thread pool and a process pool
    to show that the event loop is not blocked by these computations. Then we
    compare high-level scheduling helpers to show how supervision strategies
    differ.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Calculating fib(20) in thread pool...
    fib(20) = ...
    Calculating fib(20) in process pool...
    fib(20) = ...
    Comparing scheduling strategies...
    gather(): ['primary', 'secondary', 'tertiary']
    TaskGroup: ['primary', 'secondary', 'tertiary']
    Staggered race winner: secondary
    """
    n = 20  # a value large enough to simulate some CPU load, but not too large.
    print(f"Calculating fib({n}) in thread pool...")
    thread_result = await run_in_thread_pool(cpu_bound_fib, n)
    print(f"fib({n}) = {thread_result}")

    print(f"Calculating fib({n}) in process pool...")
    process_result = await run_in_process_pool(cpu_bound_fib, n)
    print(f"fib({n}) = {process_result}")

    print("Comparing scheduling strategies...")
    scheduling = await demonstrate_scheduling_strategies()
    print(f"gather(): {scheduling['gather']}")
    print(f"TaskGroup: {scheduling['taskgroup']}")
    print(f"Staggered race winner: {scheduling['staggered_winner']}")


if __name__ == "__main__":
    # Use a safer start method to avoid the fork() warning in multi-threaded
    # environments
    multiprocessing.set_start_method("spawn")
    asyncio.run(main())
