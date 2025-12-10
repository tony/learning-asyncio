#!/usr/bin/env python
"""
Async Call Graph Introspection.

Context
-------
Python 3.14 exposes an async call-graph inspector via
``asyncio.capture_call_graph`` and ``asyncio.print_call_graph``. The runtime now
understands how futures await each other, letting us snapshot structured stacks
for debugging or health checks.

Summary
-------
- Build a small call hierarchy that includes nested coroutines inside a
  ``TaskGroup``.
- Use ``capture_call_graph`` to snapshot the current task and derive a concise
  textual summary.
- Demonstrate ``print_call_graph`` for human-friendly logging.

Official Documentation
----------------------
- https://docs.python.org/3/library/asyncio-graph.html
- https://docs.python.org/3/whatsnew/3.14.html#asyncio

Doctest Notes
-------------
- We trim the call stack to bare function names to keep doctest output stable.
- The doctest asserts that both the call stack and awaited-by sections contain
  the expected coroutine names.
- ``asyncio.capture_call_graph`` raises ``RuntimeError`` if invoked outside a
  running loop or without a target future, so every example keeps the call
  inside an active ``TaskGroup``.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from typing import Any, NamedTuple


class GraphSummary(NamedTuple):
    """Structured summary of an async call graph."""

    frames: list[str]
    awaited_by_frames: list[str]


def _summarise_future(fut: asyncio.Future[Any]) -> GraphSummary:
    """Capture and summarise the graph for *fut*."""
    graph = asyncio.capture_call_graph(fut, limit=None)
    assert graph is not None
    frames = [entry.frame.f_code.co_name for entry in graph.call_stack]
    awaited_by_frames = []
    for parent in graph.awaited_by:
        stack_frames = [entry.frame.f_code.co_name for entry in parent.call_stack]
        awaited_by_frames.append(
            stack_frames[-1] if stack_frames else parent.future.__class__.__name__,
        )
    return GraphSummary(frames=frames, awaited_by_frames=awaited_by_frames)


async def demonstrate_concept() -> Sequence[GraphSummary]:
    """Return call-graph summaries while nested coroutines are active.

    Examples
    --------
    >>> summaries = asyncio.run(demonstrate_concept())
    >>> all('inner' in summary.frames for summary in summaries)
    True
    >>> any('demonstrate_concept' in frame for frame in summaries[0].awaited_by_frames)
    True
    """
    pause = asyncio.Event()

    async def inner() -> str:
        await pause.wait()
        return "inner-complete"

    async def outer() -> str:
        return await inner()

    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(outer(), name="outer-task")
        await asyncio.sleep(0.001)
        summary = _summarise_future(task)
        pause.set()
        await task

    return [summary]


async def main() -> None:
    """Run the demonstration and print the call graph."""
    for summary in await demonstrate_concept():
        print("Frames:", " -> ".join(summary.frames))
        print("Awaited by:", summary.awaited_by_frames or ["<none>"])
        asyncio.print_call_graph(depth=0)


if __name__ == "__main__":
    asyncio.run(main())
