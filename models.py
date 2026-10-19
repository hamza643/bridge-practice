from __future__ import annotations

from pydantic import BaseModel, ValidationError, field_validator


class Student(BaseModel):
    """A student record, validated automatically by pydantic."""

    name: str
    age: int
    email: str
    grades: dict[str, int] = {}

    @field_validator("age")
    @classmethod
    def check_age(cls, value: int) -> int:
        """Reject an age outside 5 to 25."""
        if not 5 <= value <= 25:
            raise ValueError("age must be between 5 and 25")
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        """Reject an email without an @."""
        if "@" not in value:
            raise ValueError("email must contain @")
        return value


if __name__ == "__main__":
    data = {"name": "Ali", "age": "17", "email": "ali@example.com", "grades": {"math": 88}}
    student = Student.model_validate(data)
    print(student.age, type(student.age))
    print(student.model_dump())

    try:
        Student.model_validate({"name": "Bad", "age": 99, "email": "bad-email"})
    except ValidationError as error:
        print(error)