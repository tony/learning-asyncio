#!/usr/bin/env python
"""
Instrumenting Event Loops with ``asyncio.Runner``.

[Context]
- Shows how to replace deprecated event-loop policies with ``asyncio.Runner``
  and its ``loop_factory`` hook.
- Prerequisites: Familiarity with ``asyncio.run()``, custom Tasks, and
  debugging helpers from earlier lessons.
- References:
  - ``asyncio.Runner`` documentation:
    https://docs.python.org/3/library/asyncio-runner.html
  - ``loop.set_task_factory`` for instrumentation.

[Summary]
- Build a tailor-made event loop by supplying a factory to ``Runner``.
- Enable debug mode and capture every Task created by the loop.
- Demonstrate how to use this hook for lightweight instrumentation without
  relying on deprecated event-loop policies.

Doctest Notes:
- Outputs include task names; doctests use ellipses when needed to avoid
  coupling tests to memory addresses.
- All sleeps remain at 0.001 seconds for snappy execution.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Coroutine
from typing import Any

EventLog = list[str]


def instrumented_loop_factory(log: EventLog) -> Callable[[], asyncio.AbstractEventLoop]:
    """Return a ``Runner``-compatible loop factory that records loop activity."""

    def loop_factory() -> asyncio.AbstractEventLoop:
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        log.append(f"loop-created:debug={loop.get_debug()}")

        def logging_task_factory(
            loop: asyncio.AbstractEventLoop,
            coro: Coroutine[Any, Any, Any],
            **kwargs: Any,
        ) -> asyncio.Task[Any]:
            task_name = kwargs.get("name") or getattr(
                coro, "__qualname__", type(coro).__name__
            )
            log.append(f"task-created:{task_name}")
            return asyncio.Task(coro, loop=loop, **kwargs)

        loop.set_task_factory(logging_task_factory)
        return loop

    return loop_factory


async def demonstrate_concept() -> str:
    """Simulate async work that will run inside the customized event loop.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'instrumented result'
    """
    await asyncio.sleep(0.001)
    return "instrumented result"


def run_with_instrumented_runner() -> EventLog:
    """Execute ``demonstrate_concept`` via ``asyncio.Runner`` and collect logs.

    Examples
    --------
    >>> run_with_instrumented_runner()  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ['loop-created:debug=True',
     'task-created:demonstrate_concept',
     ..., 'result:instrumented result']
    """
    log: EventLog = []
    loop_factory = instrumented_loop_factory(log)

    with asyncio.Runner(loop_factory=loop_factory) as runner:
        result = runner.run(demonstrate_concept())
    log.append(f"result:{result}")
    return log


def main() -> None:
    """Display each recorded event from the instrumented loop run.

    Examples
    --------
    >>> main()  # doctest: +ELLIPSIS
    Loop event: loop-created:debug=True
    Loop event: task-created:demonstrate_concept
    ...
    Loop event: result:instrumented result
    """
    for entry in run_with_instrumented_runner():
        print(f"Loop event: {entry}")


if __name__ == "__main__":
    main()
