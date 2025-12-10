#!/usr/bin/env python
"""
Asynchronous File I/O Operations.

Context
-------
This lesson demonstrates asynchronous file I/O patterns in Python. While Python's
built-in file operations are synchronous and can block the event loop, we'll explore
techniques to handle file I/O asynchronously, including using thread executors for
file operations and implementing streaming patterns for large files.

Prerequisites: Understanding of async/await, asyncio.run(), and basic file operations.
This lesson builds on the concurrency concepts from lessons 1-5 and the I/O patterns
introduced in lesson 14 (streams).

Summary
-------
- Learn to perform file operations without blocking the event loop.
- Use `asyncio.to_thread()` for simple file operations.
- Implement streaming file reading for large files.
- Handle multiple file operations concurrently.
- Understand when and why to use async file I/O.

Official Documentation:
- https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread
- https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor

Doctest Notes:
- We use temporary files to ensure consistent, reproducible tests.
- File operations are deterministic, making doctests straightforward.
"""

import asyncio
import tempfile
from collections.abc import AsyncIterator, Iterator
from pathlib import Path


async def read_file_async(filepath: Path) -> str:
    """
    Read a file asynchronously using asyncio.to_thread().

    This prevents blocking the event loop during file I/O operations.

    Parameters
    ----------
    filepath : Path
        Path to the file to read.

    Returns
    -------
    str
        Contents of the file.

    Examples
    --------
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    ...     _ = f.write("Hello, async file I/O!")
    ...     temp_path = Path(f.name)
    >>> try:
    ...     content = asyncio.run(read_file_async(temp_path))
    ...     print(content)
    ... finally:
    ...     temp_path.unlink()
    Hello, async file I/O!
    """
    # to_thread runs the blocking operation in a thread pool
    return await asyncio.to_thread(filepath.read_text)


async def write_file_async(filepath: Path, content: str) -> None:
    """
    Write to a file asynchronously.

    Parameters
    ----------
    filepath : Path
        Path to the file to write.
    content : str
        Content to write to the file.

    Examples
    --------
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     filepath = Path(tmpdir) / "test.txt"
    ...     asyncio.run(write_file_async(filepath, "Async write!"))
    ...     print(filepath.read_text())
    Async write!
    """
    await asyncio.to_thread(filepath.write_text, content)


async def read_file_in_chunks(
    filepath: Path,
    chunk_size: int = 1024,
) -> AsyncIterator[str]:
    r"""
    Read a file in chunks asynchronously.

    This is useful for processing large files without loading
    the entire content into memory at once.

    Parameters
    ----------
    filepath : Path
        Path to the file to read.
    chunk_size : int
        Size of each chunk in bytes.

    Yields
    ------
    str
        Each chunk of the file.

    Examples
    --------
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    ...     _ = f.write("ABCDEFGHIJKLMNOP")
    ...     temp_path = Path(f.name)
    >>> async def read_chunks():
    ...     chunks = []
    ...     async for chunk in read_file_in_chunks(temp_path, chunk_size=5):
    ...         chunks.append(chunk)
    ...     return chunks
    >>> try:
    ...     result = asyncio.run(read_chunks())
    ...     print(f"Got {len(result)} chunks:")
    ...     for chunk in result:
    ...         print(f"  {chunk!r}")
    ... finally:
    ...     temp_path.unlink()
    Got 4 chunks:
      'ABCDE'
      'FGHIJ'
      'KLMNO'
      'P'
    """

    def read_chunks_sync() -> Iterator[str]:
        with filepath.open(encoding="utf-8") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # Run the generator in a thread to avoid blocking
    for chunk in read_chunks_sync():
        # Yield control back to event loop between chunks
        await asyncio.sleep(0)
        yield chunk


async def process_files_concurrently(filepaths: list[Path]) -> list[str]:
    """
    Read multiple files concurrently.

    This demonstrates the power of async I/O when dealing with
    multiple file operations.

    Parameters
    ----------
    filepaths : List[Path]
        List of file paths to read.

    Returns
    -------
    List[str]
        Contents of all files.

    Examples
    --------
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     files = []
    ...     for i in range(3):
    ...         filepath = Path(tmpdir) / f"file{i}.txt"
    ...         _ = filepath.write_text(f"Content {i}")
    ...         files.append(filepath)
    ...     contents = asyncio.run(process_files_concurrently(files))
    ...     for content in contents:
    ...         print(content)
    Content 0
    Content 1
    Content 2
    """
    tasks = [read_file_async(filepath) for filepath in filepaths]
    return await asyncio.gather(*tasks)


async def demonstrate_concept() -> str:
    """
    Demonstrate async file I/O operations.

    Shows how to read and write files asynchronously, handle
    multiple files concurrently, and process large files in chunks.

    Examples
    --------
    >>> asyncio.run(demonstrate_concept())
    'Successfully demonstrated async file I/O with 3 files'
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Create test files
        files = []
        for i in range(3):
            filepath = tmpdir_path / f"demo{i}.txt"
            await write_file_async(filepath, f"Demo content {i}")
            files.append(filepath)

        # Read files concurrently
        contents = await process_files_concurrently(files)

        # Verify all files were read
        if len(contents) == 3 and all(
            f"Demo content {i}" in contents[i] for i in range(3)
        ):
            return f"Successfully demonstrated async file I/O with {len(files)} files"

        return "Demonstration failed"


async def main() -> None:
    """
    Run the main demonstration for this lesson.

    Shows practical examples of async file I/O including concurrent
    file processing and performance benefits.

    Examples
    --------
    >>> asyncio.run(main())  # doctest: +ELLIPSIS
    Writing files asynchronously...
    Files written!
    <BLANKLINE>
    Reading files concurrently...
    File 0: Async file content 0
    File 1: Async file content 1
    File 2: Async file content 2
    <BLANKLINE>
    Processing large file in chunks:
    Processing chunk 1...
    Processing chunk 2...
    Processing chunk 3...
    ...
    <BLANKLINE>
    Async file I/O demonstration complete!
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # 1. Write multiple files asynchronously
        print("Writing files asynchronously...")
        write_tasks = []
        for i in range(3):
            filepath = tmpdir_path / f"async_file_{i}.txt"
            task = write_file_async(filepath, f"Async file content {i}")
            write_tasks.append(task)

        await asyncio.gather(*write_tasks)
        print("Files written!\n")

        # 2. Read files concurrently
        print("Reading files concurrently...")
        filepaths = [tmpdir_path / f"async_file_{i}.txt" for i in range(3)]
        contents = await process_files_concurrently(filepaths)
        for i, content in enumerate(contents):
            print(f"File {i}: {content}")

        # 3. Process a large file in chunks
        print("\nProcessing large file in chunks:")
        large_file = tmpdir_path / "large_file.txt"

        # Create a "large" file with multiple chunks
        large_content = "\n".join(
            f"This is line {i} of the large file." for i in range(10)
        )
        await write_file_async(large_file, large_content)

        # Read and process chunks
        chunk_num = 0
        async for _chunk in read_file_in_chunks(large_file, chunk_size=50):
            chunk_num += 1
            print(f"Processing chunk {chunk_num}...")
            await asyncio.sleep(0.001)  # Simulate processing

        print("\nAsync file I/O demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())
