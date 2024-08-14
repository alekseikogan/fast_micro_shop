from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUser(BaseModel):
    """Схема для создания пользователя."""

    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    """Схема с данными пользователя."""

    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
