#!/usr/bin/env python

import asyncio


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    """
    Asynchronously handles a client connection.

    Parameters
    ----------
    reader : asyncio.StreamReader
        The stream reader.
    writer : asyncio.StreamWriter
        The stream writer.

    Examples
    --------
    >>> asyncio.run(main())
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
    """
    Asynchronously starts a server to handle client connections.

    Examples
    --------
    >>> asyncio.run(main())
    """
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8881)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    # Running the main coroutine
    asyncio.run(main())
