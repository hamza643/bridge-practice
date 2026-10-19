from __future__ import annotations

import asyncio
import time


def fetch_sync(n: int) -> int:
    """Pretend network call that blocks for one second."""
    time.sleep(1)
    return n


async def fetch_async(n: int) -> int:
    """Pretend network call that waits one second without blocking."""
    await asyncio.sleep(1)
    return n


async def main() -> None:
    """Compare three waits done one after another vs overlapped."""
    start = time.perf_counter()
    results = [fetch_sync(1), fetch_sync(2), fetch_sync(3)]
    print("sync :", results, round(time.perf_counter() - start, 2), "seconds")

    start = time.perf_counter()
    results = await asyncio.gather(fetch_async(1), fetch_async(2), fetch_async(3))
    print("async:", results, round(time.perf_counter() - start, 2), "seconds")


if __name__ == "__main__":
    asyncio.run(main())