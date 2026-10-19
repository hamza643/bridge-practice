from __future__ import annotations

from typing import Any

import httpx

BASE_URL = "https://jsonplaceholder.typicode.com"


def get_json(path: str) -> Any | None:
    """GET a path from the API and return the parsed JSON, or None on failure."""
    try:
        response = httpx.get(f"{BASE_URL}{path}", timeout=10)
    except httpx.HTTPError as error:
        print(f"Request failed: {error}")
        return None

    if response.status_code != 200:
        print(f"Error {response.status_code} for {path}")
        return None

    return response.json()


def main() -> None:
    """Fetch a user and all posts, and print some details."""
    user = get_json("/users/1")
    if user:
        print(user["name"], user["email"], user["address"]["city"])

    posts = get_json("/posts")
    if posts:
        print(f"Total posts: {len(posts)}")
        titles = [post["title"] for post in posts if post["userId"] == 1]
        for title in titles:
            print(" -", title)


if __name__ == "__main__":
    main()