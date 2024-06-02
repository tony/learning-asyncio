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
    await asyncio.sleep(0.001)  # Simulate IO-bound task
    return f"Hello, {name}!"


async def main() -> None:
    """
    Asynchronously prints multiple personalized greetings concurrently.

    Examples
    --------
    >>> asyncio.run(main())
    Hello, Alice!
    Hello, Bob!
    Hello, Charlie!
    """
    names = ["Alice", "Bob", "Charlie"]
    greetings = await asyncio.gather(*[greet(name) for name in names])
    for greeting in greetings:
        print(greeting)


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
