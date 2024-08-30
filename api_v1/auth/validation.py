from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from api_v1.auth.helpers import (ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
                                 TOKEN_TYPE_FIELD)
from api_v1.auth.utils import decode_jwt, validate_password
from users.schemas import UserSchema
from .crud import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    """Получает payload для передачи далее."""

    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Неверный токен: {e}'
        )

    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    """Проверяет тип токена на соответствие."""

    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Неверный тип токена. Сейчас он - {current_token_type!r}! Ожидаем - {token_type}.",
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    """Получает данные о пользователе по заголовку sub."""

    username: str = payload.get("sub")
    if user := users_db.get(username):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Пользователь не найден!'
    )


def get_user_from_token_of_type(token_type: str):
    def get_user_from_token(payload: dict = Depends(get_current_token_payload)
                            ) -> UserSchema:

        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_user_from_token


get_current_user = get_user_from_token_of_type(ACCESS_TOKEN_TYPE)

# def get_current_user(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserSchema:
#     """Получает данные о пользователе из payload
#     по access токену."""

#     validate_token_type(payload, ACCESS_TOKEN_TYPE)
#     return get_user_by_token_sub(payload)


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)

# def get_current_user_for_refresh(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserSchema:
#     """Получает данные о пользователе из payload
#     по refresh токену."""

#     validate_token_type(payload, REFRESH_TOKEN_TYPE)
#     return get_user_by_token_sub(payload)


def get_current_active_user(user: UserSchema = Depends(get_current_user)):
    """Получение активного пользователя."""
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Пользователь не активен!'
    )


def validate_user_login(
    username: str = Form(),
    password: str = Form(),
):
    """Проверка логина и пароля пользователя."""

    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Неверное имя или пароль!'
    )
    if not (user := users_db.get(username)):
        raise unauthed_exp

    if validate_password(
        password=password,
        hashed_password=user.password
    ):
        return user

    raise unauthed_exp
