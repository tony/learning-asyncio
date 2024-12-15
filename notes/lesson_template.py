#!/usr/bin/env python
"""
[Lesson Title].

[Context]
- Explain what this lesson is teaching: e.g., This lesson demonstrates how to use asyncio.Lock to ensure safe concurrent access.
- State the prerequisites: e.g., Familiarity with basic asyncio concepts is required (async/await, event loop).
- Provide links or references: e.g., Official docs: https://docs.python.org/3/library/asyncio.html

[Summary]
- In a few lines, summarize what the code does and what learners will take away from it.

Doctests:
- Provide doctest examples below that can be run with `pytest --doctest-modules` or `python -m doctest -v thisfile.py`.
- Use ellipses in doctests if necessary (e.g. `# doctest: +ELLIPSIS`) to allow flexibility in output if concurrency makes order unpredictable.
- Keep sleeps minimal and deterministic if possible, or rely on ellipses in doctest output where concurrent output order isn't guaranteed.
"""

import asyncio

# INSTRUCTIONS/NOTES:
# 1. Use only standard library asyncio and built-ins.
# 2. Provide a simple async function or class that demonstrates the lesson concept.
# 3. Include doctests that run `asyncio.run(main())` or similar to show expected behavior.
# 4. Ensure the code can be directly executed: `python thisfile.py`.
# 5. Keep examples minimal but illustrative, focusing on the concept taught in this lesson.
# 6. Comment on tricky parts of the code to help learners understand the "why" behind decisions.


async def demonstrate_concept() -> str:
    """
    [Function Purpose]
    Explain what this function does and why it is important for this lesson.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'Expected Result'
    """
    # For demonstration, we simulate a short sleep.
    await asyncio.sleep(0.001)
    return "Expected Result"


async def main() -> None:
    """
    Main entrypoint for this lesson.

    - Orchestrates the demonstration.
    - Prints or returns results to be verified by doctests.
    - Optionally, show multiple usage scenarios here.

    Examples
    --------
    >>> asyncio.run(main())
    Expected Result
    """
    result = await demonstrate_concept()
    print(result)


if __name__ == "__main__":
    # Running the main coroutine to allow standalone execution.
    asyncio.run(main())
