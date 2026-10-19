from __future__ import annotations

from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    """Base class that every table class inherits from."""


class Book(Base):
    """One row in the books table."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    year: Mapped[int]


engine = create_engine("sqlite:///library.db")

def add_books() -> None:
    """Insert three books, but only if the table is still empty."""
    with Session(engine) as session:
        if session.scalars(select(Book)).first() is not None:
            return
        session.add_all(
            [
                Book(title="Fluent Python", author="Ramalho", year=2015),
                Book(title="Clean Code", author="Martin", year=2008),
                Book(title="The Pragmatic Programmer", author="Hunt", year=1999),
            ]
        )
        session.commit()


def list_books() -> list[Book]:
    """Return every book as a Book object."""
    with Session(engine) as session:
        return list(session.scalars(select(Book)).all())


def books_after(year: int) -> list[Book]:
    """Return books published after the given year."""
    with Session(engine) as session:
        return list(session.scalars(select(Book).where(Book.year > year)).all())


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_books()

    print("All books:")
    for book in list_books():
        print(" ", book.id, book.title, book.author, book.year)

    print("Books after 2000:")
    for book in books_after(2000):
        print(" ", book.id, book.title, book.year)