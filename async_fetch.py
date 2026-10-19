from __future__ import annotations

import asyncio
import time

import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"


async def get_user_name(client: httpx.AsyncClient, user_id: int) -> str:
    """Fetch one user by id and return their name."""
    response = await client.get(f"{BASE_URL}/users/{user_id}")
    response.raise_for_status()
    return response.json()["name"]


async def fetch_concurrently(ids: list[int]) -> list[str]:
    """Fetch several users at the same time with asyncio.gather."""
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*[get_user_name(client, i) for i in ids])


def fetch_one_by_one(ids: list[int]) -> list[str]:
    """Fetch the same users one after another with a normal loop."""
    names: list[str] = []
    with httpx.Client() as client:
        for user_id in ids:
            response = client.get(f"{BASE_URL}/users/{user_id}")
            response.raise_for_status()
            names.append(response.json()["name"])
    return names


async def main() -> None:
    """Time both approaches for users 1 to 5."""
    ids = [1, 2, 3, 4, 5]

    start = time.perf_counter()
    names = await fetch_concurrently(ids)
    print("concurrent:", names, round(time.perf_counter() - start, 3), "seconds")

    start = time.perf_counter()
    names = fetch_one_by_one(ids)
    print("one by one:", names, round(time.perf_counter() - start, 3), "seconds")


if __name__ == "__main__":
    asyncio.run(main())