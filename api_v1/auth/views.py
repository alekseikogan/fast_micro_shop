import secrets
import time
import uuid
from typing import Annotated, Any

from fastapi import (APIRouter, Cookie, Depends, Header, HTTPException,
                     Response, status)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def basic_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """Аутентификация пользователя."""
    return {
        "message": "Успешно получилось!",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {
    "admin": "admin",
    "alex": "password"
}


def get_auth_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    """Проверяет пароль и выдает имя пользователя если пароль верный."""

    unauthed_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверное имя или пароль!"
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
    """Если пользователь существует - выдает его имя."""

    return {
        "message": f"Здарова, {auth_username}",
        "username": auth_username,
    }


static_auth_token_to_username = {
    "qwerty123456": "admin",
    "ytrewq654321": "alex"
}


def get_username_by_static_token(
        static_token: str = Header(alias='x-secret-token')
) -> str:
    """Проверяет токен и выдает имя пользователя если токен верный."""

    if static_token not in static_auth_token_to_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверный токен')

    return static_auth_token_to_username[static_token]


@router.get("/some-http-header-auth")
def basic_auth_some_http_header(
    username: str = Depends(get_username_by_static_token)
):
    """Если токен существует - выдает имя пользователя."""

    return {
        "message": f"Здарова, {username}",
        "username": username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'web_app_session_id'


@router.post("/login-cookie")
def basic_auth_login_cookie(
    response: Response,
    username: str = Depends(basic_auth_username)
):
    """Аутентификация через Cookie."""

    def generate_session_id() -> str:
        return uuid.uuid4().hex

    session_id = generate_session_id()

    # записываем на сервер данные о клиенте (полные)
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time.time())
    }

    # записываем в браузер ключ сессии
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)

    return {
        "message": "Успешно залогинились!"
    }


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
                     ) -> dict:
    """Получение данных о сессии через session_id."""

    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Ключ сессии не найден'
        )

    return COOKIES[session_id]


@router.get('/check_cookie')
def check_cookie(
    user_session_data: dict = Depends(get_session_data)
):
    """Получает данные о пользователе по сессии."""

    return {
        **user_session_data
    }


@router.get("/logout_cookie")
def logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data)
):
    """Разлогинивается по куки."""

    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {"message": f"ВЫ РАЗЛОГИНИЛИСЬ, {username}"}
