#!/usr/bin/env python
"""This example demonstrates the use of asyncio streams for network communication.

It covers creating a server, handling client connections, and performing read and write
operationv asynchronously.
"""

import asyncio
import contextlib


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    """Asynchronously handles a client connection.

    Parameters
    ----------
    reader : asyncio.StreamReader
        The stream reader.
    writer : asyncio.StreamWriter
        The stream writer.

    Examples
    --------
    >>> asyncio.run(main())
    Serving on ('127.0.0.1', 8889)
    Shutting down the server
    """
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info("peername")

    print(f"Received {message} from {addr}")

    writer.write(data)
    await writer.drain()

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()


async def main() -> None:
    """Asynchronously starts a server to handle client connections and shuts it down after a brief period.

    Examples
    --------
    >>> asyncio.run(main())
    Serving on ('127.0.0.1', 8889)
    Shutting down the server
    """
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8889)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async def shutdown() -> None:
        await asyncio.sleep(0.001)  # Shutdown after a brief period
        server.close()
        await server.wait_closed()
        print("Shutting down the server")

    async with server:
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.gather(server.serve_forever(), shutdown())


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
