#!/usr/bin/env python
"""
Customizing the Event Loop.

[Context and summary as before]

Doctest Notes:
- We use ellipses in the doctest to allow flexibility in class names and memory
  addresses.
- We match on substrings like 'DefaultEventLoopPolicy' and 'EventLoop' rather
  than full paths.

"""

import asyncio


class CustomEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    """A custom event loop policy for demonstration purposes."""

    def new_event_loop(self) -> asyncio.AbstractEventLoop:
        """Create a new event loop instance."""
        return super().new_event_loop()


async def demonstrate_custom_loop() -> str:
    """Demonstrate running on a custom event loop."""
    await asyncio.sleep(0.001)
    return "Ran on a custom loop"


def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates:
    1. Getting the current default event loop policy.
    2. Installing a custom event loop policy.
    3. Creating a new event loop from that policy and running a coroutine on it.
    4. Restoring the original policy afterward.

    Examples
    --------
    >>> main()  # doctest: +ELLIPSIS
    Original policy: <...DefaultEventLoopPolicy object at ...>
    Custom policy installed: <...CustomEventLoopPolicy object at ...>
    Running with custom loop: <...EventLoop ...>
    Result: Ran on a custom loop
    Policy restored: <...DefaultEventLoopPolicy object at ...>
    """
    original_policy = asyncio.get_event_loop_policy()
    print(f"Original policy: {original_policy}")

    custom_policy = CustomEventLoopPolicy()
    asyncio.set_event_loop_policy(custom_policy)
    print(f"Custom policy installed: {asyncio.get_event_loop_policy()}")

    loop = asyncio.new_event_loop()
    print(f"Running with custom loop: {loop}")

    try:
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(demonstrate_custom_loop())
        print(f"Result: {result}")
    finally:
        loop.close()
        asyncio.set_event_loop_policy(original_policy)
        print(f"Policy restored: {asyncio.get_event_loop_policy()}")


if __name__ == "__main__":
    main()
