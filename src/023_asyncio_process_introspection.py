#!/usr/bin/env python
"""
Asyncio Process Introspection CLI.

Context
-------
Python 3.14 ships a first-party inspector for running asyncio programs. The
``python -m asyncio ps`` and ``python -m asyncio pstree`` subcommands query the
current task graph of any Python process. This lesson demonstrates how to use
the same machinery from inside your code for observability checks.

Summary
-------
- Launch a handful of named tasks that block on an ``Event`` so the inspector
  can observe them.
- Leverage ``asyncio.tools.get_all_awaited_by`` and
  ``asyncio.tools.build_task_table`` to capture a structured task table.
- Normalise volatile fields (thread IDs, memory addresses) while preserving the
  await stacks that matter for debugging.
- Show how to inspect *any* PID (just like ``python -m asyncio ps``) while still
  keeping doctests deterministic.

Official Documentation
----------------------
- https://docs.python.org/3/whatsnew/3.14.html#asyncio-introspection-capabilities
- https://docs.python.org/3/library/asyncio.html

Doctest Notes
-------------
- The inspector output contains volatile IDs; we redact them so doctests remain
  deterministic while still validating that the named tasks and stacks appear.
- The doctest asserts that every ``job-*`` task is present and that their
  coroutine stacks include the blocking ``Event.wait`` frame.
"""

from __future__ import annotations

import asyncio
import os
import re
from asyncio import tools as asyncio_tools
from collections.abc import Sequence
from typing import NamedTuple


class TaskRow(NamedTuple):
    """A normalised snapshot of a task row."""

    task_name: str
    coroutine_stack: str
    awaiter_name: str


def _snapshot_task_table(pid: int) -> list[TaskRow]:
    """Return a normalised view of the current asyncio task table."""
    awaited = asyncio_tools.get_all_awaited_by(pid)
    table = asyncio_tools.build_task_table(awaited)
    normalised: list[TaskRow] = []
    whitespace = re.compile(r"\s+")

    for (
        thread_id,
        task_id,
        task_name,
        stack,
        awaiter_chain,
        awaiter_name,
        parent_id,
    ) in table:
        del thread_id, task_id, parent_id  # Only keep human-friendly fields.
        stack_text = str(stack or "")
        awaiter_chain_text = str(awaiter_chain or "")
        awaiter_name_text = str(awaiter_name or "")
        task_name_text = str(task_name)

        clean_stack = whitespace.sub(" ", stack_text).strip() or "<idle>"
        clean_await = whitespace.sub(" ", awaiter_chain_text).strip()
        if not clean_await:
            clean_await = awaiter_name_text or "<none>"
        normalised.append(
            TaskRow(
                task_name=task_name_text,
                coroutine_stack=clean_stack,
                awaiter_name=clean_await,
            ),
        )

    return normalised


async def demonstrate_concept(pid: int | None = None) -> Sequence[TaskRow]:
    """Capture a live task table for *pid* (defaults to this process).

    Examples
    --------
    >>> rows = asyncio.run(demonstrate_concept())
    >>> sorted(row.task_name for row in rows if row.task_name.startswith("job-"))
    ['job-0', 'job-1', 'job-2']
    >>> all(
    ...     "Event.wait" in row.coroutine_stack
    ...     for row in rows
    ...     if row.task_name.startswith("job-")
    ... )
    True
    >>> explicit = asyncio.run(demonstrate_concept(pid=os.getpid()))
    >>> len(explicit) == len(rows)
    True
    """
    target_pid = pid if pid is not None else os.getpid()
    release_gate = asyncio.Event()

    async def worker(idx: int) -> str:
        await release_gate.wait()
        return f"job-{idx}-done"

    async with asyncio.TaskGroup() as tg:
        for idx in range(3):
            tg.create_task(worker(idx), name=f"job-{idx}")

        await asyncio.sleep(0.001)
        rows = await asyncio.to_thread(_snapshot_task_table, target_pid)
        release_gate.set()

    return rows


async def main() -> None:
    """Run the demonstration and print the captured task table."""
    for row in await demonstrate_concept():
        print(
            f"{row.task_name:>10} | {row.coroutine_stack} | "
            f"awaited by {row.awaiter_name}",
        )


if __name__ == "__main__":
    asyncio.run(main())
