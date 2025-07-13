#!/usr/bin/env python
"""
Advanced Scheduling and Executors.

Context
-------
This lesson shows how to integrate `asyncio` with executors to offload
CPU-bound tasks from the event loop. While asyncio excels at managing I/O-bound
concurrency, CPU-bound tasks can block the event loop and degrade
responsiveness. By running them in a thread or process pool, the event loop can
continue handling I/O while the CPU-bound work executes elsewhere.

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
- Understand when to offload tasks to avoid blocking the event loop.

Official Documentation:
- https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
- https://docs.python.org/3/library/concurrent.futures.html

Doctest Notes:
- We'll show a CPU-bound function (like calculating Fibonacci numbers) running
  in executors.
- Output order may vary slightly, so we use ellipses to allow flexibility.
- The example demonstrates offloading tasks to a thread pool and a process pool.

"""

import asyncio
import concurrent.futures
import multiprocessing
from collections.abc import Callable


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
    to show that the event loop is not blocked by these computations.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Calculating fib(20) in thread pool...
    fib(20) = ...
    Calculating fib(20) in process pool...
    fib(20) = ...
    """
    n = 20  # a value large enough to simulate some CPU load, but not too large.
    print(f"Calculating fib({n}) in thread pool...")
    thread_result = await run_in_thread_pool(cpu_bound_fib, n)
    print(f"fib({n}) = {thread_result}")

    print(f"Calculating fib({n}) in process pool...")
    process_result = await run_in_process_pool(cpu_bound_fib, n)
    print(f"fib({n}) = {process_result}")


if __name__ == "__main__":
    # Use a safer start method to avoid the fork() warning in multi-threaded
    # environments
    multiprocessing.set_start_method("spawn")
    asyncio.run(main())
