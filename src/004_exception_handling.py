#!/usr/bin/env python

import asyncio


async def may_fail(succeed: bool) -> str:
    """
    Asynchronously returns a success message or raises an exception based on input.

    Parameters
    ----------
    succeed : bool
        Determines if the coroutine should succeed or fail.

    Returns
    -------
    str
        A success message.

    Raises
    ------
    ValueError
        If succeed is False.

    Examples
    --------
    >>> asyncio.run(may_fail(True))
    'Success!'
    >>> asyncio.run(may_fail(False))
    Traceback (most recent call last):
    ...
    ValueError: Failure!
    """
    if succeed:
        return "Success!"
    msg = "Failure!"
    raise ValueError(msg)


async def main() -> None:
    """
    Asynchronously handles exceptions in coroutines.

    Examples
    --------
    >>> asyncio.run(main())
    Success!
    Caught an exception: Failure!
    """
    try:
        result = await may_fail(True)
        print(result)
        result = await may_fail(False)
        print(result)
    except ValueError as e:
        print(f"Caught an exception: {e}")


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
