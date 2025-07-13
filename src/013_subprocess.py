#!/usr/bin/env python
"""
Running and Managing Subprocesses.

Context
-------
This lesson shows how to run external commands as subprocesses within your async
application. By using `asyncio.create_subprocess_shell()` or
`asyncio.create_subprocess_exec()`, you can start external processes, capture
their output, and integrate them into your event loop without blocking. This is
essential for scenarios where your async code needs to interact with legacy
tools, shell commands, or other external programs.

Summary
-------
- Demonstrate starting a subprocess asynchronously.
- Show how to capture and handle stdout/stderr from the subprocess.
- Integrate subprocess handling into the async event loop, ensuring other tasks
  aren't blocked.

Official Documentation:
- https://docs.python.org/3/library/asyncio-subprocess.html

Doctest Notes:
- We use a simple `echo` command as an example, which should output
  "Hello, World!" reliably.
- The doctest for `run_command` checks only the returned value, so we should not
  print inside `run_command`.
- In `main`, we demonstrate printing the output after calling `run_command`.
"""

import asyncio


async def run_command(command: str) -> str:
    """
    Asynchronously runs a command in a subprocess and returns its stdout output.

    Parameters
    ----------
    command : str
        The shell command to run.

    Returns
    -------
    str
        The output of the command.

    Examples
    --------
    >>> output = asyncio.run(run_command("echo Hello, World!"))
    >>> output.strip()
    'Hello, World!'
    """
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, _stderr = await proc.communicate()

    # Return only the output, do not print here to avoid failing the doctest.
    return stdout.decode() if stdout else ""


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Runs a sample command (`echo Hello, World!`) using an async subprocess,
    captures its output, and prints it. This demonstrates how to integrate
    external commands into an async workflow without blocking the event loop.

    Examples
    --------
    >>> asyncio.run(main())
    [stdout]
    Hello, World!
    Output: Hello, World!
    """
    command = "echo Hello, World!"
    output = await run_command(command)

    # Now we print the output here for demonstration:
    print("[stdout]")
    print(output)
    print(f"Output: {output.strip()}")


if __name__ == "__main__":
    asyncio.run(main())
