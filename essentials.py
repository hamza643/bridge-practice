from __future__ import annotations

import functools
import time
from typing import Any, Callable


def word_count(text: str) -> dict[str, int]:
    """Count how many times each word appears in the text."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def only_adults(people: list[dict]) -> list[dict]:
    """Return people whose age is 18 or more."""
    return [person for person in people if person["age"] >= 18]


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """ prints how long the wrapped function took to run."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result

    return wrapper


@timer
def slow_sum(n: int) -> int:
    """Add the numbers from 1 to n."""
    return sum(range(1, n + 1))


if __name__ == "__main__":
    print(word_count("the cat and the hat"))

    people = [{"name": "Ali", "age": 17}, {"name": "Sara", "age": 22}]
    print(only_adults(people))

    print(slow_sum(1_000_000))
    