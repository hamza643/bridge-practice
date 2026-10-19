from __future__ import annotations

import asyncio
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError, field_validator
from sqlalchemy import String, create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

BASE_URL = "https://jsonplaceholder.typicode.com"
engine = create_engine("sqlite:///capstone.db")


class Base(DeclarativeBase):
    """Base class for the table classes."""


class UserRow(Base):
    """One row in the users table."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))


class User(BaseModel):
    """A validated user with only the fields we care about."""

    name: str
    email: str
    city: str

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        """Reject an email without an @."""
        if "@" not in value:
            raise ValueError("email must contain @")
        return value


async def fetch_user(client: httpx.AsyncClient, user_id: int) -> dict[str, Any]:
    """Fetch one raw user from the API."""
    response = await client.get(f"{BASE_URL}/users/{user_id}")
    response.raise_for_status()
    return response.json()


def to_user(raw: dict[str, Any]) -> User:
    """Pick the fields we need from the raw JSON and validate them."""
    return User.model_validate(
        {
            "name": raw.get("name"),
            "email": raw.get("email"),
            "city": raw.get("address", {}).get("city"),
        }
    )


def store_users(users: list[User]) -> None:
    """Replace the contents of the users table with the given users."""
    with Session(engine) as session:
        session.execute(delete(UserRow))
        session.add_all([UserRow(**user.model_dump()) for user in users])
        session.commit()


def read_users() -> list[UserRow]:
    """Read all users back from the database."""
    with Session(engine) as session:
        return list(session.scalars(select(UserRow)).all())


async def main() -> None:
    """Run the pipeline: fetch, validate, store, read back."""
    Base.metadata.create_all(engine)

    async with httpx.AsyncClient() as client:
        raw_users = await asyncio.gather(*[fetch_user(client, i) for i in range(1, 6)])
    print(f"1. Fetched {len(raw_users)} users")

    valid_users: list[User] = []
    for raw in raw_users:
        try:
            valid_users.append(to_user(raw))
        except ValidationError as error:
            print(f"   Skipping bad user: {error}")
    print(f"2. Validated {len(valid_users)} users")

    store_users(valid_users)
    print("3. Stored in the database")

    print("4. Read back from the database:")
    for row in read_users():
        print(" ", row.id, row.name, row.email, row.city)


if __name__ == "__main__":
    asyncio.run(main())