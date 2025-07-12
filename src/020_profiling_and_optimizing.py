#!/usr/bin/env python
"""
Performance Tuning and Best Practices.

Context
-------
As your async application grows, ensuring high performance becomes essential. This lesson
outlines strategies and tools for profiling and optimizing asyncio programs, as well as
general best practices for stable, low-latency async systems.

Key Concepts and Best Practices:
1. **Reduce Event Loop Latency:**
   - Keep tasks short and non-blocking. Break long tasks into smaller coroutines.
   - For CPU-bound workloads, offload to executors or separate processes to avoid blocking the loop.
   - Limit concurrency to a reasonable level using semaphores or queues to prevent the event loop
     from being overwhelmed.

2. **Profiling and Monitoring:**
   - Use `asyncio.run(main(), debug=True)` or `PYTHONASYNCIODEBUG=1` to enable asyncio debug mode.
     This can help detect common pitfalls like blocked event loops or slow callbacks.
   - Employ profiling tools such as `yappi`, `py-spy`, or `tracemalloc` to identify bottlenecks.
   - Use logging and metrics (e.g., Prometheus, StatsD) to monitor latency, task durations, and system load.

3. **Minimizing Overhead:**
   - Avoid excessive context switches by batching I/O operations.
   - Use bulk operations when possible (e.g., gather multiple tasks at once rather than
     iterating with awaits).
   - Keep the number of scheduled tasks manageable. Over-scheduling can increase
     overhead.

4. **Testing Under Load:**
   - Use load testing and benchmarking tools (like `locust` for HTTP, custom scripts
     for internal tasks) to measure how your application scales.
   - Identify the "sweet spot" for concurrency and tune it. Sometimes fewer tasks
     result in better throughput.

5. **Other Python and System-level Optimizations:**
   - Consider using `uvloop` (a drop-in replacement for the default event loop) for
     lower latency if allowed.
   - Ensure the system's event loop integration (e.g., epoll on Linux) is working
     optimally.
   - Consider C extensions or PyPy for CPU-heavy code if compatible.

Summary
-------
- Introduce debugging and profiling tools for asyncio (debug mode, external profilers).
- Show techniques for reducing overhead and keeping the event loop responsive.
- Demonstrate best practices like limiting concurrency and offloading CPU-bound tasks.

Official Documentation:
- https://docs.python.org/3/library/asyncio-dev.html
- Profiling: https://docs.python.org/3/library/profile.html
- `uvloop`: https://github.com/MagicStack/uvloop

Doctest Notes:
- We'll show simple examples of measuring time and limiting concurrency. Actual
  performance gains must be verified by running the code under realistic conditions,
  not just doctests.

"""

import asyncio
import time
from collections.abc import Awaitable, Callable, Sequence
from typing import Any


async def measure_runtime(coro: Callable[[], Awaitable[Any]]) -> float:
    """
    Measure how long a given coroutine takes to complete.

    Examples
    --------
    >>> async def example_task():
    ...     await asyncio.sleep(0.01)
    ...     return "done"
    >>> runtime = asyncio.run(measure_runtime(example_task))
    >>> runtime < 0.1
    True
    """
    start = time.perf_counter()
    await coro()
    end = time.perf_counter()
    return end - start


async def cpu_bound_task(n: int) -> int:
    """Simulate a CPU-bound task (inefficient fibonacci).

    Demonstrates why to offload CPU tasks.
    """
    if n < 2:
        return n
    return await asyncio.to_thread(fib, n)


def fib(n: int) -> int:
    """Calculate Fibonacci number (naive implementation for demonstration)."""
    # Naive Fibonacci for demonstration only.
    return n if n < 2 else fib(n - 1) + fib(n - 2)


async def limited_concurrency_example(
    tasks: Sequence[Callable[[], Awaitable[Any]]],
    concurrency: int = 5,
) -> None:
    """
    Demonstrate limiting concurrency using a semaphore.

    This helps prevent the event loop from being overwhelmed.
    """
    sem = asyncio.Semaphore(concurrency)

    async def worker(task_coro: Callable[[], Awaitable[Any]]) -> None:
        async with sem:
            await task_coro()

    await asyncio.gather(*(worker(t) for t in tasks))


async def main() -> None:
    """Demonstrate performance techniques.

    1. Measure runtime of a task.
    2. Show CPU-bound offloading using `asyncio.to_thread()`.
    3. Limit concurrency with semaphores.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Measured time: 0...
    CPU-bound result: ...
    Done with limited concurrency
    """
    # 1. Measure runtime
    runtime = await measure_runtime(lambda: asyncio.sleep(0.05))
    print(f"Measured time: {runtime:.4f} seconds")

    # 2. Offload CPU-bound task
    n = 20
    result = await cpu_bound_task(n)
    print(f"CPU-bound result: fib({n}) = {result}")

    # 3. Limit concurrency
    # Suppose we have many tasks; limit to a concurrency of 3.
    # asyncio.sleep(...) returns a coroutine, which is an Awaitable.
    tasks = [lambda: asyncio.sleep(0.01) for _ in range(10)]
    await limited_concurrency_example(tasks, concurrency=3)
    print("Done with limited concurrency")


if __name__ == "__main__":
    # For actual debugging, you might run:
    #   PYTHONASYNCIODEBUG=1 python thisfile.py
    # Or:
    #   asyncio.run(main(), debug=True)
    asyncio.run(main())
