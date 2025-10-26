#!/usr/bin/env python
"""
Cross-Thread Observability with asyncio.

Context
-------
Asyncio 3.14 improves task bookkeeping so the new inspector can see tasks that
were scheduled from different threads. This lesson submits work to the main
event loop from a background thread and renders the combined await tree.

Summary
-------
- Spawn a background thread that schedules named tasks onto the running loop.
- Keep the main loop busy with its own tasks so the inspector shows both
  sources.
- Use ``asyncio.tools.build_async_tree`` to render a normalised tree without
  volatile memory addresses.

Official Documentation
----------------------
- https://docs.python.org/3/whatsnew/3.14.html#asyncio-introspection-capabilities
- https://docs.python.org/3/library/asyncio.html

Doctest Notes
-------------
- The doctest ensures the rendered tree contains both the main-loop and
  thread-loop tasks, verifying cross-thread visibility.
"""

from __future__ import annotations

import asyncio
import os
import threading
from asyncio import tools as asyncio_tools
from collections.abc import Sequence


def _capture_tree(pid: int) -> list[str]:
    """Return the pretty-printed await tree for *pid*."""
    awaited = asyncio_tools.get_all_awaited_by(pid)
    trees = asyncio_tools.build_async_tree(awaited)
    # ``build_async_tree`` returns one list per root; we flatten to a simple list.
    return [line for tree in trees for line in tree]


async def demonstrate_concept() -> Sequence[str]:
    """Return the rendered await tree containing both threads.

    Examples
    --------
    >>> tree_lines = asyncio.run(demonstrate_concept())
    >>> any('main-job' in line for line in tree_lines)
    True
    >>> any('thread-job' in line for line in tree_lines)
    True
    """
    loop = asyncio.get_running_loop()
    release_gate = asyncio.Event()
    worker_started = threading.Event()

    async def main_worker(name: str) -> None:
        await release_gate.wait()

    def submit_thread_jobs() -> None:
        def schedule(name: str) -> None:
            loop.create_task(main_worker(name), name=name)

        for idx in range(2):
            job_name = f"thread-job-{idx}"
            loop.call_soon_threadsafe(schedule, job_name)
        worker_started.set()

    thread = threading.Thread(
        target=submit_thread_jobs,
        name="scheduler-thread",
        daemon=True,
    )
    thread.start()
    worker_started.wait()

    async with asyncio.TaskGroup() as tg:
        for idx in range(2):
            tg.create_task(main_worker(f"main-job-{idx}"), name=f"main-job-{idx}")

        await asyncio.sleep(0.001)
        tree_lines = await asyncio.to_thread(_capture_tree, os.getpid())
        release_gate.set()

    thread.join()

    return tree_lines


async def main() -> None:
    """Run the demonstration and print the tree."""
    for line in await demonstrate_concept():
        print(line)


if __name__ == "__main__":
    asyncio.run(main())
