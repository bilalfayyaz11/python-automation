import asyncio
import aiohttp
import aiofiles
import os


async def fetch_url(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            content = await response.text()

            return {
                "url": url,
                "status_code": response.status,
                "content_length": len(content),
            }


async def process_file(filename: str, operation: str) -> dict:
    if operation == "read":
        async with aiofiles.open(filename, mode="r") as file:
            content = await file.read()

        return {
            "filename": filename,
            "operation": operation,
            "bytes_read": len(content),
            "content_preview": content[:80],
        }

    if operation == "write":
        async with aiofiles.open(filename, mode="w") as file:
            await file.write("Generated asynchronously by the execution engine.\n")

        return {
            "filename": filename,
            "operation": operation,
            "bytes_written": os.path.getsize(filename),
        }

    raise ValueError("Unsupported file operation")


async def compute_intensive_task(n: int) -> int:
    await asyncio.sleep(n)
    return n * n
