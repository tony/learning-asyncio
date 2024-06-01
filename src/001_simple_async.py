#!/usr/bin/env python

import asyncio


async def hello_world() -> str:
    """
    Asynchronously returns a greeting string.

    Returns
    -------
    str
        A greeting string "Hello, world!"

    Examples
    --------
    >>> asyncio.run(hello_world())
    'Hello, world!'
    """
    return "Hello, world!"


if __name__ == "__main__":
    # Running the coroutine
    result = asyncio.run(hello_world())
    print(result)
