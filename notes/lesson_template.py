#!/usr/bin/env python
"""
[Lesson Title].

[Context]
- State the concept: e.g., "This lesson demonstrates how to use asyncio.Lock to ensure safe concurrent access."
- Prerequisites: Familiarity with `asyncio.run()`, basic async/await syntax, and the event loop model.
- References:
  - Official docs: https://docs.python.org/3/library/asyncio.html
  - If relevant, link to previous lessons or external docs on advanced usage.

[Summary]
- Summarize in a few lines what this lesson covers and what learners will take away.
- For example: "By the end of this lesson, you'll understand how to lock shared resources in async code,
  preventing race conditions and ensuring data integrity under concurrency."

Doctests:
- Include doctests demonstrating usage.
- Use ellipses (e.g., `# doctest: +ELLIPSIS`) if concurrency or timing introduces non-determinism.
- Keep sleeps minimal and, if needed, rely on ellipses to handle output variance.
- Ensure that running `pytest --doctest-modules` or `python -m doctest -v thisfile.py` succeeds.
- Each example should be self-contained and instructive, focusing on the core concept.

Type Hints & Mypy:
- Consider adding type hints to functions to improve clarity and help with static analysis.
- For instance, specify return types (e.g., `async def demonstrate_concept() -> str:`).
- If tasks or external constructs are used, consider using `Awaitable` or `Callable` where appropriate.

Execution:
- Running `python thisfile.py` should execute `main()` and demonstrate the concept.
- Keep the example minimal and self-contained.
"""

import asyncio

# INSTRUCTIONS/NOTES:
# 1. Use only standard library asyncio and built-ins (no external dependencies).
# 2. Show a simple asynchronous function or class that demonstrates the lesson's concept clearly.
# 3. Include doctests that show expected output.
# 4. Focus on clarity and educational value: explain tricky parts in comments.
# 5. Ensure that output is stable enough for doctests, or use ellipses if order can vary.
# 6. Consider adding a small delay (like 0.001 seconds) to simulate async behavior without causing long test runs.


async def demonstrate_concept() -> str:
    """
    [Function Purpose]
    Explain what this function does and why it is important for this lesson.

    For example:
    This function simulates a short async operation (like an I/O wait)
    and returns a predetermined result. It illustrates how an async function
    can await a coroutine and produce a value.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'Expected Result'
    """
    # Simulate a brief async operation
    await asyncio.sleep(0.001)
    return "Expected Result"


async def main() -> None:
    """
    Main entrypoint for this lesson.

    This orchestrates the demonstration by calling the core function and printing the result.
    In more complex lessons, main might handle multiple tasks, show concurrency patterns,
    or illustrate error handling.

    Examples
    --------
    >>> asyncio.run(main())
    Expected Result
    """
    result = await demonstrate_concept()
    print(result)


if __name__ == "__main__":
    # Running the main coroutine so the file is executable directly.
    asyncio.run(main())
