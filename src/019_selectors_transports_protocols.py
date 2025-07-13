#!/usr/bin/env python
"""
Selectors, Transports, and Protocols.

Context
-------
At the core of asyncio's asynchronous I/O lie transports and protocols, which are
low-level abstractions over system calls, sockets, and selectors. A "selector" is used by
asyncio to monitor multiple file descriptors for I/O readiness events. Transports provide
a high-level interface for sending and receiving data without directly dealing with the
underlying OS calls. Protocols define the behavior of what to do with incoming and
outgoing data.

Key Concepts:
- A Selector (from the `selectors` module) is used internally by the event loop to watch
  file descriptors (sockets, pipes, etc.) for read/write readiness. The event loop then
  triggers protocol callbacks when data is ready.
- A Transport is an abstraction provided by asyncio that handles the actual I/O (like
  writing to a socket) and buffering. It frees you from manually handling `os.read()`,
  `os.write()`, or non-blocking flags on sockets.
- A Protocol is a callback-based abstraction that receives events: connection made, data
  received, connection lost. It's where you implement your application logic for handling
  I/O.

By understanding these, you gain insight into how asyncio can handle multiple network
connections concurrently without blocking.

Examples of Selectors and Transports
------------------------------------
While asyncio hides selectors behind its event loop, here's what happens under the hood:
- The event loop (often a SelectorEventLoop on Unix) uses a `selectors.Selector` instance
  (e.g., `selectors.EpollSelector` on Linux) to register sockets for read/write events.
- When a socket is ready, the selector notifies the event loop, which then calls the
  protocol's `data_received()` or `connection_made()` methods depending on the event.

You typically don't interact with the selector directly. Instead, you work with high-level
APIs like `create_connection()` or `create_server()` that return a Transport and use a
Protocol.

Transports Example:
- When you call `transport.write(data)`, the Transport schedules the write operation.
- The event loop uses the selector to know when the socket can accept writes without
  blocking.
- Once ready, the Transport writes the data to the socket.

Official Documentation:
- https://docs.python.org/3/library/asyncio-protocol.html
- https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.create_connection
- https://docs.python.org/3/library/selectors.html

Doctest Notes:
- We'll start a small echo server protocol and then connect to it with a client.
- Output order may vary slightly, so we'll use ellipses in doctests.
- The example focuses on conceptual clarity rather than robust error handling.

"""

import asyncio
from typing import cast


class EchoServerProtocol(asyncio.Protocol):
    """Protocol implementation for an echo server."""

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """Handle new client connection."""
        # Cast transport to WriteTransport so .write() is recognized
        self.transport = cast("asyncio.WriteTransport", transport)
        peername = self.transport.get_extra_info("peername")
        print(f"Connection made from {peername}")

    def data_received(self, data: bytes) -> None:
        """Handle data received from the client."""
        message = data.decode()
        print(f"Server received: {message!r}")
        # Echo the data back
        self.transport.write(data)

    def connection_lost(self, exc: Exception | None) -> None:
        """Handle connection close."""
        print("Server connection closed")


class EchoClientProtocol(asyncio.Protocol):
    """Protocol implementation for an echo client."""

    def __init__(self, message: str, on_con_lost: asyncio.Future[bool]) -> None:
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport: asyncio.Transport | None = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """Handle connection establishment."""
        # Store transport for closing later, cast to Transport to satisfy mypy
        self.transport = cast("asyncio.Transport", transport)
        wtransport = cast("asyncio.WriteTransport", self.transport)
        print("Client connection made, sending message...")
        wtransport.write(self.message.encode())

    def data_received(self, data: bytes) -> None:
        """Handle data received from the server."""
        print(f"Client received: {data.decode()!r}")
        # Signal that we got the response
        self.on_con_lost.set_result(True)
        if self.transport is not None:
            self.transport.close()

    def connection_lost(self, exc: Exception | None) -> None:
        """Handle connection close."""
        print("Client connection closed")


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates creating a server and a client using custom protocols.
    We show that:
    - The event loop uses a selector internally to watch for I/O readiness.
    - Transports handle buffering and I/O operations.
    - Protocols define the handling of data and connection events.

    The server echoes back any data received from the client. The client sends
    "Hello, Protocol!" and expects to receive the same message echoed back.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Server listening on ...
    Connection made from ...
    Client connection made, sending message...
    Server received: 'Hello, Protocol!'
    Client received: 'Hello, Protocol!'
    Client connection closed
    Server connection closed
    """
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        EchoServerProtocol,
        "127.0.0.1",
        0,  # 0 means pick an abitrary free port
    )

    server_address = server.sockets[0].getsockname()
    print(f"Server listening on {server_address}")

    on_con_lost: asyncio.Future[bool] = loop.create_future()
    message = "Hello, Protocol!"

    # Create a client connection using a protocol
    await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        "127.0.0.1",
        server_address[1],
    )

    await on_con_lost

    server.close()
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
