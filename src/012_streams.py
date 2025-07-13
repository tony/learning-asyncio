#!/usr/bin/env python
"""
Network I/O with Streams.

Context
-------
This lesson demonstrates how to use `asyncio` streams for network I/O operations.
Streams provide a high-level API for working with network connections, making it easy
to create both TCP servers and clients. We'll build a simple echo server and client
to show how data flows through async streams.

Summary
-------
- Learn to create a TCP server using `asyncio.start_server()`.
- Use `StreamReader` and `StreamWriter` for reading and writing data.
- Build a client that connects to the server using `asyncio.open_connection()`.
- Understand how to handle multiple concurrent connections.

Official Documentation:
- https://docs.python.org/3/library/asyncio-stream.html

Doctest Notes:
- We use localhost (127.0.0.1) and a fixed port for predictable testing.
- The server runs briefly to handle one client connection then shuts down.
- Output is deterministic as we control both server and client.
"""

import asyncio


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, verbose: bool = True
) -> None:
    """
    Handle a single client connection.

    Parameters
    ----------
    reader : asyncio.StreamReader
        Stream for reading data from the client.
    writer : asyncio.StreamWriter
        Stream for writing data to the client.
    verbose : bool
        Whether to print connection details.
    """
    # Get client address for logging
    addr = writer.get_extra_info("peername")
    if verbose:
        print(f"Client connected from {addr}")

    # Read data from client
    data = await reader.read(100)
    message = data.decode()
    if verbose:
        print(f"Received: {message}")

    # Echo the message back
    writer.write(data)
    await writer.drain()
    if verbose:
        print(f"Echoed: {message}")

    # Close the connection
    writer.close()
    await writer.wait_closed()
    if verbose:
        print("Client disconnected")


async def run_server(host: str, port: int, verbose: bool = True) -> None:
    """
    Run the echo server.

    Parameters
    ----------
    host : str
        Host address to bind to.
    port : int
        Port number to listen on.
    verbose : bool
        Whether to print connection details.
    """

    async def handle_client_wrapper(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        await handle_client(reader, writer, verbose)

    server = await asyncio.start_server(handle_client_wrapper, host, port)

    async with server:
        # Accept one connection then stop
        await asyncio.sleep(0.1)  # Give client time to connect


async def run_client(host: str, port: int, message: str) -> str:
    """
    Connect to the server and send a message.

    Parameters
    ----------
    host : str
        Server host address.
    port : int
        Server port number.
    message : str
        Message to send.

    Returns
    -------
    str
        The echoed response from the server.
    """
    reader, writer = await asyncio.open_connection(host, port)

    # Send message
    writer.write(message.encode())
    await writer.drain()

    # Read response
    data = await reader.read(100)
    response = data.decode()

    # Close connection
    writer.close()
    await writer.wait_closed()

    return response


async def demonstrate_concept() -> str:
    """
    Demonstrate client-server communication using streams.

    This creates a simple echo server and client that exchange a message.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'Hello, streams!'
    """
    host = "127.0.0.1"
    port = 8888
    message = "Hello, streams!"

    # Start server and client concurrently (verbose=False for clean doctest)
    server_task = asyncio.create_task(run_server(host, port, verbose=False))
    await asyncio.sleep(0.01)  # Let server start

    # Run client
    response = await run_client(host, port, message)

    # Wait for server to finish
    await server_task

    return response


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Demonstrates a complete client-server interaction using asyncio streams.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Client connected from ...
    Received: Hello, streams!
    Echoed: Hello, streams!
    Client disconnected
    Echo server demo complete. Response: Hello, streams!
    """
    # Run with verbose output for main demonstration
    host = "127.0.0.1"
    port = 8889  # Different port to avoid conflicts
    message = "Hello, streams!"

    # Start server with verbose output
    server_task = asyncio.create_task(run_server(host, port, verbose=True))
    await asyncio.sleep(0.01)  # Let server start

    # Run client
    response = await run_client(host, port, message)

    # Wait for server to finish
    await server_task

    print(f"Echo server demo complete. Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
