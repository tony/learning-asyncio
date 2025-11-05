# Asyncio Doctest Playbook

Guide for stitching together async examples that pass doctest while showcasing `asyncio`. Each section references the CPython source where the pattern appears so you can cross-check the canonical usage.

## Core Pattern: Coroutine + `asyncio.run`

**Scenario**: Show a top-level coroutine that prints or returns values. (See `Doc/library/asyncio-task.rst:27`.)

```pycon
>>> import asyncio
>>> async def main():
...     print("hello")
...     await asyncio.sleep(0.01)
...     print("world")
>>> asyncio.run(main())
hello
world

```

**Why it works**: `asyncio.run()` owns the event loop, keeps the doctest synchronous, and produces deterministic output.

**Variations**:
- Return a value from `main()` and assert equality.
- Accept parameters and show different awaitable calls.
- Chain multiple awaits to demonstrate sequencing guarantees.

## Pattern: Simulating REPL-Only `await`

**Scenario**: Document the behavior of `python -m asyncio`, which allows top-level `await`. (See `Doc/whatsnew/3.8.rst:636` and `Doc/library/asyncio.rst:72`.)

You cannot run top-level `await` directly inside doctest, so provide an equivalent coroutine helper and mention the REPL behavior alongside it.

```pycon
>>> import asyncio
>>> async def repl_simulator():
...     return await asyncio.sleep(0, result="hello")
>>> asyncio.run(repl_simulator())
'hello'

```

Text to accompany the runnable snippet (not part of the doctest):
- In the asyncio REPL you would type `await asyncio.sleep(10, result='hello')` and see `hello`.
- Make it clear the REPL avoids repeated event-loop creation, unlike calling `asyncio.run()` for every await.

## Pattern: Async Context Managers

**Scenario**: Demonstrate `async with` blocks that wrap cancellable work. (See `Lib/asyncio/timeouts.py:142` and `:165`, plus `Doc/library/unittest.mock-examples.rst:308`.)

```pycon
>>> import asyncio
>>> async def short_task():
...     await asyncio.sleep(0)
...     return "ok"
>>> async def with_timeout():
...     async with asyncio.timeout(1):
...         return await short_task()
>>> asyncio.run(with_timeout())
'ok'

```

```pycon
>>> import asyncio
>>> async def short_task():
...     await asyncio.sleep(0)
...     return "ok"
>>> async def with_absolute_timeout():
...     loop = asyncio.get_running_loop()
...     async with asyncio.timeout_at(loop.time() + 1):
...         return await short_task()
>>> asyncio.run(with_absolute_timeout())
'ok'

```

**Notes**:
- Describe cancellation behavior in prose if the example does not raise.
- To show failure modes, call a coroutine that never completes and expect `asyncio.TimeoutError`.
- When mocking, demonstrate `assert_awaited_once()` on `__aenter__` and `__aexit__`.

## Pattern: Async Iterators & Comprehensions

**Scenario**: Verify `async for` iteration or comprehensions. (See `Doc/library/unittest.mock-examples.rst:276`.)

```pycon
>>> from unittest.mock import MagicMock
>>> import asyncio
>>> mock = MagicMock()
>>> mock.__aiter__.return_value = [1, 2, 3]
>>> async def consume():
...     return [item async for item in mock]
>>> asyncio.run(consume())
[1, 2, 3]

```

**Tips**:
- Keep the sequence finite; doctest waits for completion before comparison.
- Mock out I/O-heavy operations to prevent flakiness.

## Pattern: Mocking Awaitables with `AsyncMock`

**Scenario**: Assert awaited behavior or call ordering. (See `Doc/library/unittest.mock.rst:972-1138`.)

```pycon
>>> from unittest.mock import AsyncMock
>>> import asyncio
>>> mock = AsyncMock()
>>> async def call_twice():
...     await mock("foo")
...     await mock("bar")
>>> asyncio.run(call_twice())
>>> mock.assert_has_awaits([(("foo",), {}), (("bar",), {})])

```

**Variants**:
- Use `assert_any_await()` for order-insensitive checks.
- Inspect `await_args_list` to introspect historical calls.
- Reset the mock to demonstrate state cleanup between awaits.

## Pattern: Manual Loop Plumbing

**Scenario**: Teach legacy patterns or custom loop factories. (See `Doc/whatsnew/3.8.rst:626`.)

```pycon
>>> import asyncio
>>> async def legacy_main():
...     await asyncio.sleep(0)
...     return "legacy"
>>> loop = asyncio.new_event_loop()
>>> asyncio.set_event_loop(loop)
>>> try:
...     loop.run_until_complete(legacy_main())
... finally:
...     asyncio.set_event_loop(None)
...     loop.close()
'legacy'

```

**When to use**:
- Demonstrating `loop_factory` hooks.
- Explaining cleanup responsibilities predating `asyncio.run()`.

## Pattern: Tasks and Debugger Transcripts

**Scenario**: Capture async `pdb` sessions that interact with tasks. (See `Lib/test/test_pdb.py:2134-2295`.)

Running those doctests requires CPython’s `PdbTestInput` harness, which is not practical in standalone markdown. Present a runnable extraction plus a companion transcript.

```pycon
>>> import asyncio
>>> async def coroutine_that_prints():
...     await asyncio.sleep(0)
...     return "done"
>>> async def spawn_task():
...     task = asyncio.create_task(coroutine_that_prints())
...     await task
...     return task.result()
>>> asyncio.run(spawn_task())
'done'

```

Transcript excerpt (plain text, not executed):

```
... (Pdb) task = asyncio.create_task(test())
... (Pdb) x = await task
hello
world
```

**Notes**:
- Reference the harness helpers (`PdbTestInput`, custom `loop_factory`) when adapting CPython’s doctests.
- Use `# doctest: +ELLIPSIS` to mask task names or memory addresses.

## Pattern: Context Variables with Async Workflows

**Scenario**: Combine `contextvars` with awaited calls without leaking state. (See `Lib/test/test_pdb.py:2215`.)

```pycon
>>> import asyncio, contextvars
>>> var = contextvars.ContextVar("var", default=0)
>>> async def get_and_set(val):
...     previous = var.get()
...     var.set(val)
...     return previous, var.get()
>>> async def main():
...     var.set(42)
...     return await get_and_set(99)
>>> asyncio.run(main())
(42, 99)

```

**Key takeaway**: Document that context state flows through awaited calls and task switches.

## Pattern: Async Generators & Yield Points

**Scenario**: Inspect stepping behavior across `await` and `yield`. (See `Lib/test/test_pdb.py:2255` and `:2288`.)

```pycon
>>> import asyncio
>>> async def agen():
...     yield 1
...     await asyncio.sleep(0)
...     yield 2
>>> async def gather():
...     result = []
...     async for value in agen():
...         result.append(value)
...     return result
>>> asyncio.run(gather())
[1, 2]

```

**Guidelines**:
- Pair the runnable snippet with textual debugger transcripts when explaining stepping semantics.
- Highlight where `asyncio` suppresses `StopIteration` noise.

## Doctest Directives for Async Output

- `+ELLIPSIS`: Mask loop IDs, task names, or memory addresses.
- `+NORMALIZE_WHITESPACE`: Relax alignment in multi-line transcripts.
- `+SKIP`: Guard platform-specific behavior (socket availability, signal handling, etc.).
- `+FAIL_FAST`: Abort long transcripts on first mismatch.

## Permutation Cheatsheet

| Goal                         | Loop Strategy                        | Tooling            | Reference                               |
|------------------------------|--------------------------------------|--------------------|-----------------------------------------|
| Run a coroutine sequentially | `asyncio.run(main())`                | None               | `Doc/library/asyncio-task.rst:27`       |
| Simulate REPL await          | helper coroutine + `asyncio.run`     | None               | `Doc/library/asyncio.rst:72`            |
| Manual loop lifecycle        | explicit create/run/close            | None               | `Doc/whatsnew/3.8.rst:626`              |
| Timeout guard                | `asyncio.timeout` / `timeout_at`     | None               | `Lib/asyncio/timeouts.py:142`           |
| Task orchestration           | `asyncio.create_task`                | Debug transcripts  | `Lib/test/test_pdb.py:2161`             |
| Async iterator demo          | `async for` comprehension            | `MagicMock`        | `Doc/library/unittest.mock-examples.rst:276` |
| Await verification           | `AsyncMock.assert_*` helpers         | `AsyncMock`        | `Doc/library/unittest.mock.rst:972`     |
| Context propagation          | `contextvars.ContextVar`             | None               | `Lib/test/test_pdb.py:2215`             |

## Building New Async Doctests

1. Choose the event loop owner: prefer `asyncio.run`, fall back to manual loops when teaching legacy APIs.
2. Keep awaitables bounded: doctest expects termination; simulate I/O with mocks or short sleeps.
3. Stabilize output: replace non-deterministic values with placeholders plus `+ELLIPSIS`.
4. Signal environment needs: note when a snippet assumes an async-friendly REPL or debugger harness.
5. Document state transitions: after each await, display or assert the change you want the reader to notice.

## LLM Prompt Seeds

- "Generate a doctest that demonstrates `asyncio.timeout` canceling slow work."
- "Create a doctest showing how `AsyncMock.assert_has_awaits` tracks multiple awaited calls."
- "Write a doctest transcript that drives `pdb` through an async task using `set_trace_async`."
- "Produce a doctest that illustrates `contextvars` cooperating with awaited coroutines."
- "Draft a doctest that iterates over an async generator and asserts collected results."

## Common Pitfalls Checklist

- Forgetting to wrap coroutines with `asyncio.run` in plain doctests.
- Expecting top-level `await` outside the asyncio REPL.
- Allowing event loop IDs or task names to break string comparisons—mask them with `+ELLIPSIS`.
- Running infinite loops or long sleeps without timeouts, causing hangs.
- Neglecting to close manual event loops when documenting legacy patterns.

Use this playbook as a menu: pick the pattern that matches your teaching goal, copy the runnable snippet, then tailor the narrative around it so doctest and readers stay in sync.
