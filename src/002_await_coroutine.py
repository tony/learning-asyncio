#!/usr/bin/env python

import asyncio


async def greet(name: str) -> str:
    """
    Asynchronously returns a personalized greeting string.

    Parameters
    ----------
    name : str
        The name to greet.

    Returns
    -------
    str
        A personalized greeting string.

    Examples
    --------
    >>> asyncio.run(greet("Alice"))
    'Hello, Alice!'
    """
    return f"Hello, {name}!"


async def main() -> None:
    """
    Asynchronously prints a personalized greeting.

    Examples
    --------
    >>> asyncio.run(main())
    Hello, Alice!
    """
    greeting = await greet("Alice")
    print(greeting)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
