import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Успешно получилось!",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {"admin": "admin", "alex": "password"}


def get_auth_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """Проверяет пароль и выдает имя пользователя если пароль верный."""
    unauthed_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя или пароль!"
    )

    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_ex

    if credentials.username not in usernames_to_passwords:
        raise unauthed_ex

    # secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"), correct_password.encode("utf-8")
    ):
        raise unauthed_ex

    return credentials.username


@router.get("/basic-auth-username")
def basic_auth_username(auth_username: str = Depends(get_auth_username)):
    return {
        "message": f"Здарова, {auth_username}",
        "username": auth_username,
    }
