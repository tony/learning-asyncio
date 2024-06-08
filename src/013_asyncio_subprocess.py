#!/usr/bin/env python
"""This example demonstrates how to use asyncio to run subprocesses.

It covers creating subprocesses and reading their output asynchronously.
"""

import asyncio


async def run_command(command: str) -> str:
    """Asynchronously runs a command in a subprocess.

    Parameters
    ----------
    command : str
        The command to run.

    Returns
    -------
    str
        The output of the command.

    Examples
    --------
    >>> asyncio.run(main())
    [stdout]
    Hello, World!
    <BLANKLINE>
    Output: Hello, World!
    """
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()

    if stdout:
        print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")

    return stdout.decode()


async def main() -> None:
    """Asynchronously runs a sample command in a subprocess and prints the output.

    Examples
    --------
    >>> asyncio.run(main())
    [stdout]
    Hello, World!
    <BLANKLINE>
    Output: Hello, World!
    """
    command = f'echo {"Hello, World!"}'
    output = await run_command(command)
    print(f"Output: {output.strip()}")


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
