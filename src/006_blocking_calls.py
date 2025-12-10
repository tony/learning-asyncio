#!/usr/bin/env python
"""
The Cooperative Contract: How Blocking Calls Break Asyncio.

Context
-------
Python's asyncio runs on a single thread and relies on cooperative multitasking.
Concurrency only works when every coroutine voluntarily yields control via ``await``.
A single blocking call—whether ``time.sleep()``, a synchronous HTTP request, or a
blocking file read—holds the thread hostage and freezes all other coroutines.

This lesson demonstrates:

1. Why asyncio's concurrency is an "illusion" maintained by cooperation
2. How blocking calls shatter that illusion and serialize execution
3. How to detect when blocking is occurring
4. The ``asyncio.to_thread()`` escape hatch for legacy sync code

Prerequisites:
- Familiarity with ``asyncio.run()``, basic async/await syntax
- Understanding that asyncio uses a single-threaded event loop
- Lessons 001-005 (foundations of async programming)

References
----------
- Official docs: https://docs.python.org/3/library/asyncio-dev.html#running-blocking-code
- PEP 3156 (asyncio): https://peps.python.org/pep-3156/

Summary
-------
By the end of this lesson, you'll understand:

- How asyncio's cooperative nature requires every task to yield
- Why one blocking call freezes the entire event loop
- How to use ``asyncio.to_thread()`` to offload blocking work
- How to detect blocking with a "canary" task pattern

Doctest Notes:
- Core demonstrations use deterministic tick-counting (no timing dependencies)
- Visual demonstrations use ``+ELLIPSIS`` for sections with timing output
- All doctests pass without ``+SKIP``

Type Hints:
- All functions are fully typed
- Uses modern Python 3.9+ syntax with ``Callable`` and ``Awaitable``
"""

from __future__ import annotations

import asyncio
import contextlib
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

# =============================================================================
# PART 1: Core Demonstration (Deterministic Tick-Counting)
# =============================================================================


@dataclass
class WorkerState:
    """Shared state between a worker and the heartbeat monitor.

    Attributes
    ----------
    worker_running
        True while the worker is "in the middle" of its job.
    stop
        When True, the heartbeat task exits its loop.
    """

    worker_running: bool = False
    stop: bool = False


@dataclass
class HeartbeatStats:
    """Statistics collected by the heartbeat monitor.

    Attributes
    ----------
    ticks_total
        Total times the heartbeat had a chance to run.
    ticks_while_worker_running
        Ticks that occurred while worker_running was True.

    The key insight:
    - Cooperative worker: ticks_while_worker_running > 0 (heartbeat ran during work)
    - Blocking worker: ticks_while_worker_running == 0 (heartbeat starved)
    """

    ticks_total: int = 0
    ticks_while_worker_running: int = 0


async def heartbeat(state: WorkerState, stats: HeartbeatStats) -> None:
    """Record how often the event loop schedules this task.

    This heartbeat runs in a tight loop, incrementing counters each time the
    event loop gives it CPU time. It's designed to detect whether the event
    loop is running (cooperative code) or frozen (blocking code).

    Parameters
    ----------
    state
        Shared state with the worker.
    stats
        Mutable statistics object for recording ticks.

    Examples
    --------
    The heartbeat ticks when given a chance:

    >>> async def demo():
    ...     state = WorkerState()
    ...     stats = HeartbeatStats()
    ...     task = asyncio.create_task(heartbeat(state, stats))
    ...     await asyncio.sleep(0)  # Let heartbeat tick once
    ...     await asyncio.sleep(0)  # And again
    ...     state.stop = True
    ...     await task
    ...     return stats.ticks_total >= 1
    >>> asyncio.run(demo())
    True
    """
    while not state.stop:
        if state.worker_running:
            stats.ticks_while_worker_running += 1
        stats.ticks_total += 1
        await asyncio.sleep(0)  # Yield to event loop


async def cooperative_worker(state: WorkerState) -> None:
    """Cooperate with the event loop by yielding control.

    This worker marks itself as running, yields control with
    ``await asyncio.sleep(0)``, then marks itself as done. The yield
    gives the heartbeat a chance to tick while we're "running".

    Parameters
    ----------
    state
        Shared state with the heartbeat.

    Examples
    --------
    The heartbeat gets exactly 1 tick while this worker is running:

    >>> async def demo():
    ...     state = WorkerState()
    ...     stats = HeartbeatStats()
    ...     hb = asyncio.create_task(heartbeat(state, stats))
    ...     await cooperative_worker(state)
    ...     state.stop = True
    ...     await hb
    ...     return stats.ticks_while_worker_running
    >>> asyncio.run(demo())
    1
    """
    state.worker_running = True
    await asyncio.sleep(0)  # THE COOPERATIVE YIELD
    state.worker_running = False


async def blocking_worker(state: WorkerState) -> None:
    """Block the event loop with a synchronous call.

    Despite being an ``async def``, this worker calls ``time.sleep()``—a
    blocking syscall. The event loop cannot run other tasks during this
    call, so the heartbeat is completely starved.

    Parameters
    ----------
    state
        Shared state with the heartbeat.

    Examples
    --------
    The heartbeat gets 0 ticks while this worker is running:

    >>> async def demo():
    ...     state = WorkerState()
    ...     stats = HeartbeatStats()
    ...     hb = asyncio.create_task(heartbeat(state, stats))
    ...     await blocking_worker(state)
    ...     state.stop = True
    ...     await hb
    ...     return stats.ticks_while_worker_running
    >>> asyncio.run(demo())
    0
    """
    state.worker_running = True
    time.sleep(0.0)  # BLOCKING! Event loop cannot switch tasks here.
    state.worker_running = False


async def offloaded_worker(state: WorkerState) -> None:
    """Offload blocking work to a thread via asyncio.to_thread.

    This demonstrates the fix for blocking code: use ``asyncio.to_thread()``
    to run the blocking function in a separate thread. The ``await`` yields
    control to the event loop while the thread works.

    Parameters
    ----------
    state
        Shared state with the heartbeat.

    Examples
    --------
    The heartbeat gets at least 1 tick while this worker is running:

    >>> async def demo():
    ...     state = WorkerState()
    ...     stats = HeartbeatStats()
    ...     hb = asyncio.create_task(heartbeat(state, stats))
    ...     await offloaded_worker(state)
    ...     state.stop = True
    ...     await hb
    ...     return stats.ticks_while_worker_running >= 1
    >>> asyncio.run(demo())
    True
    """

    def _blocking_work() -> None:
        # Use small but non-zero delay to ensure heartbeat gets scheduled
        time.sleep(0.001)

    state.worker_running = True
    await asyncio.to_thread(_blocking_work)  # Yields to event loop!
    state.worker_running = False


WorkerFn = Callable[[WorkerState], Awaitable[None]]


async def run_scenario(worker: WorkerFn) -> HeartbeatStats:
    """Run a worker alongside a heartbeat monitor and return statistics.

    This helper wires together the shared state, heartbeat, and worker,
    providing a clean interface for testing different worker behaviors.

    Parameters
    ----------
    worker
        An async function that accepts WorkerState.

    Returns
    -------
    HeartbeatStats
        Statistics about heartbeat ticks during the worker's execution.

    Examples
    --------
    >>> asyncio.run(run_scenario(cooperative_worker)).ticks_while_worker_running
    1
    >>> asyncio.run(run_scenario(blocking_worker)).ticks_while_worker_running
    0
    >>> asyncio.run(run_scenario(offloaded_worker)).ticks_while_worker_running >= 1
    True
    """
    state = WorkerState()
    stats = HeartbeatStats()
    hb_task = asyncio.create_task(heartbeat(state, stats))

    await worker(state)

    state.stop = True
    await hb_task
    return stats


# =============================================================================
# PART 2: Visual Demonstration (Interleaving vs Serialization)
# =============================================================================


async def traced_cooperative(name: str, delay: float = 0.001) -> str:
    """Log start and completion while cooperating with the event loop.

    All tasks using the same delay will resume in creation order,
    making the output deterministic.

    Examples
    --------
    >>> asyncio.run(traced_cooperative("test", 0.001))
    [test] start
    [test] done
    'test'
    """
    print(f"[{name}] start")
    await asyncio.sleep(delay)
    print(f"[{name}] done")
    return name


def traced_blocking(name: str, delay: float = 0.001) -> str:
    """Log start and completion while blocking synchronously.

    Because this is synchronous, it completes entirely before returning.

    Examples
    --------
    >>> traced_blocking("test", 0.001)
    [test] start
    [test] done
    'test'
    """
    print(f"[{name}] start")
    time.sleep(delay)
    print(f"[{name}] done")
    return name


async def demonstrate_interleaving() -> list[str]:
    """Show how cooperative tasks interleave vs how blocking tasks serialize.

    This function runs two sets of tasks:
    1. Cooperative: All start before any complete (interleaving)
    2. Blocking: Each completes before the next starts (serialization)

    The output is deterministic because:
    - Cooperative tasks are created in order and all use the same delay
    - Blocking tasks run sequentially by nature

    Returns
    -------
    list[str]
        Names of all completed tasks.

    Examples
    --------
    >>> asyncio.run(demonstrate_interleaving())
    === Cooperative (interleaving) ===
    [coop-0] start
    [coop-1] start
    [coop-2] start
    [coop-0] done
    [coop-1] done
    [coop-2] done
    === Blocking (serialized) ===
    [block-0] start
    [block-0] done
    [block-1] start
    [block-1] done
    [block-2] start
    [block-2] done
    ['coop-0', 'coop-1', 'coop-2', 'block-0', 'block-1', 'block-2']
    """
    print("=== Cooperative (interleaving) ===")
    coop_results = await asyncio.gather(
        *[traced_cooperative(f"coop-{i}") for i in range(3)]
    )

    print("=== Blocking (serialized) ===")
    block_results = [traced_blocking(f"block-{i}") for i in range(3)]

    return list(coop_results) + block_results


# =============================================================================
# PART 3: The Infection Problem
# =============================================================================


async def demonstrate_infection() -> None:
    """Show how blocking code buried in a call chain infects async wrappers.

    Even though we use ``async def`` and ``asyncio.gather()``, the blocking
    call deep in the chain prevents true concurrency. Each task must complete
    its blocking work before the next can start.

    Examples
    --------
    >>> asyncio.run(demonstrate_infection())  # doctest: +ELLIPSIS
    === The Infection Problem ===
    Task 0: starting
    Task 0: done
    Task 1: starting
    Task 1: done
    Task 2: starting
    Task 2: done
    Total time: ... (serialized, not concurrent!)
    """

    def deeply_nested_blocking() -> None:
        """Block the thread innocently."""
        time.sleep(0.01)

    def intermediate_function() -> None:
        """Call another function that secretly blocks."""
        deeply_nested_blocking()

    async def async_wrapper(task_id: int) -> None:
        """Wrap blocking code in an async function (the infection)."""
        print(f"Task {task_id}: starting")
        intermediate_function()  # THE INFECTION
        print(f"Task {task_id}: done")

    print("=== The Infection Problem ===")
    start = time.perf_counter()
    await asyncio.gather(*[async_wrapper(i) for i in range(3)])
    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.2f}s (serialized, not concurrent!)")


async def demonstrate_proper_async() -> None:
    """Contrast: properly async code all the way down.

    When every layer uses ``await``, true concurrency is achieved.

    Examples
    --------
    >>> asyncio.run(demonstrate_proper_async())  # doctest: +ELLIPSIS
    === Proper Async Chain ===
    Task 0: starting
    Task 1: starting
    Task 2: starting
    Task 0: done
    Task 1: done
    Task 2: done
    Total time: ... (concurrent!)
    """

    async def deeply_nested_async() -> None:
        """Yield control properly via await."""
        await asyncio.sleep(0.01)

    async def intermediate_async() -> None:
        """Pass through the async chain."""
        await deeply_nested_async()

    async def async_task(task_id: int) -> None:
        """Execute fully async from top to bottom."""
        print(f"Task {task_id}: starting")
        await intermediate_async()
        print(f"Task {task_id}: done")

    print("=== Proper Async Chain ===")
    start = time.perf_counter()
    await asyncio.gather(*[async_task(i) for i in range(3)])
    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.2f}s (concurrent!)")


# =============================================================================
# PART 4: Detection and Mitigation
# =============================================================================


class BlockingDetector:
    """Detect if code blocks the event loop using a canary task.

    Uses a "canary" task pattern: creates a task that sets a flag when it runs.
    If your code yields (awaits), the canary gets scheduled and runs.
    If your code blocks, the canary never runs.

    Attributes
    ----------
    canary_ran
        True if the event loop had a chance to run other tasks.

    Examples
    --------
    Cooperative code allows the canary to run:

    >>> async def test_coop():
    ...     async with BlockingDetector() as d:
    ...         await asyncio.sleep(0)  # Yields - canary runs
    ...     return d.canary_ran
    >>> asyncio.run(test_coop())
    True

    Blocking code starves the canary:

    >>> async def test_block():
    ...     async with BlockingDetector() as d:
    ...         time.sleep(0)  # Blocks - canary never runs
    ...     return d.canary_ran
    >>> asyncio.run(test_block())
    False
    """

    def __init__(self) -> None:
        """Initialize the detector."""
        self.canary_ran: bool = False
        self._task: asyncio.Task[None] | None = None

    async def _canary(self) -> None:
        """Set the flag when scheduled by the event loop."""
        self.canary_ran = True

    async def __aenter__(self) -> BlockingDetector:
        """Create the canary task (but don't yield yet)."""
        self._task = asyncio.create_task(self._canary())
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Clean up the canary task."""
        if self._task:
            if not self._task.done():
                self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task


def make_async[T](func: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    """Wrap a blocking function to run in an executor.

    Runs the function in the default thread pool executor, allowing
    the event loop to remain responsive.

    Parameters
    ----------
    func
        A synchronous function to wrap.

    Returns
    -------
    Callable[..., Awaitable[T]]
        An async version that runs in an executor.

    Examples
    --------
    >>> @make_async
    ... def blocking_add(a: int, b: int) -> int:
    ...     return a + b
    >>> asyncio.run(blocking_add(2, 3))
    5
    """

    async def wrapper(*args: object, **kwargs: object) -> T:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    return wrapper


# =============================================================================
# PART 5: Main Demonstration
# =============================================================================


async def demonstrate_concept() -> str:
    """Demonstrate the core concept with deterministic assertions.

    Runs all three worker types and returns a summary string showing
    the tick counts, proving that cooperative and offloaded workers
    allow heartbeat ticks while blocking workers don't.

    Returns
    -------
    str
        A summary of the results.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'cooperative=1, blocking=0, offloaded>=1: all passed'
    """
    coop_stats = await run_scenario(cooperative_worker)
    block_stats = await run_scenario(blocking_worker)
    off_stats = await run_scenario(offloaded_worker)

    coop_ok = coop_stats.ticks_while_worker_running == 1
    block_ok = block_stats.ticks_while_worker_running == 0
    off_ok = off_stats.ticks_while_worker_running >= 1

    if coop_ok and block_ok and off_ok:
        return "cooperative=1, blocking=0, offloaded>=1: all passed"
    return f"FAILED: coop={coop_stats}, block={block_stats}, off={off_stats}"


async def main() -> None:
    """Run the full demonstration of blocking vs cooperative async.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    ================================================================
    THE COOPERATIVE CONTRACT: How Blocking Calls Break Asyncio
    ================================================================
    <BLANKLINE>
    PART 1: Core Concept (Deterministic)
    ------------------------------------
    cooperative=1, blocking=0, offloaded>=1: all passed
    <BLANKLINE>
    PART 2: Visual Demonstration
    ----------------------------
    === Cooperative (interleaving) ===
    [coop-0] start
    [coop-1] start
    [coop-2] start
    [coop-0] done
    [coop-1] done
    [coop-2] done
    === Blocking (serialized) ===
    [block-0] start
    [block-0] done
    [block-1] start
    [block-1] done
    [block-2] start
    [block-2] done
    <BLANKLINE>
    PART 3: The Infection Problem
    -----------------------------
    === The Infection Problem ===
    Task 0: starting
    Task 0: done
    Task 1: starting
    Task 1: done
    Task 2: starting
    Task 2: done
    Total time: ...s (serialized, not concurrent!)
    <BLANKLINE>
    === Proper Async Chain ===
    Task 0: starting
    Task 1: starting
    Task 2: starting
    Task 0: done
    Task 1: done
    Task 2: done
    Total time: ...s (concurrent!)
    <BLANKLINE>
    KEY TAKEAWAYS
    =============
    1. Asyncio concurrency is COOPERATIVE - every task must yield via 'await'
    2. A single blocking call (time.sleep, requests.get) freezes ALL tasks
    3. Use asyncio.to_thread() to offload blocking work to a thread pool
    4. "Async everywhere" isn't a style choice - it's a survival requirement
    """
    print("=" * 64)
    print("THE COOPERATIVE CONTRACT: How Blocking Calls Break Asyncio")
    print("=" * 64)

    print("\nPART 1: Core Concept (Deterministic)")
    print("-" * 36)
    result = await demonstrate_concept()
    print(result)

    print("\nPART 2: Visual Demonstration")
    print("-" * 28)
    await demonstrate_interleaving()

    print("\nPART 3: The Infection Problem")
    print("-" * 29)
    await demonstrate_infection()
    print()
    await demonstrate_proper_async()

    print("\nKEY TAKEAWAYS")
    print("=" * 13)
    print("1. Asyncio concurrency is COOPERATIVE - every task must yield via 'await'")
    print("2. A single blocking call (time.sleep, requests.get) freezes ALL tasks")
    print("3. Use asyncio.to_thread() to offload blocking work to a thread pool")
    print("4. \"Async everywhere\" isn't a style choice - it's a survival requirement")


if __name__ == "__main__":
    asyncio.run(main())
