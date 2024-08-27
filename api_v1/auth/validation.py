from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from api_v1.auth.helpers import (ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
                                 TOKEN_TYPE_FIELD)
from api_v1.auth.utils import decode_jwt
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
    """Проверяет тип токена."""

    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Неверный тип токена - {token_type!r}! ожидаем {ACCESS_TOKEN_TYPE}.",
    )


def get_user_by_token_sub(
        payload: dict = Depends(get_current_token_payload)):
    """Получает данные о пользователе по payload."""

    validate_token_type(payload, ACCESS_TOKEN_TYPE)

    return get_user_by_token_sub(payload)


def get_current_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    """Получает данные о пользователе по payload."""

    validate_token_type(payload, ACCESS_TOKEN_TYPE)

    return get_user_by_token_sub(payload)


def get_current_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    """Получает данные о пользователе по payload."""

    validate_token_type(payload, REFRESH_TOKEN_TYPE)

    username: str = payload.get('sub')
    if user := users_db.get(username):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Пользователь не найден!'
    )
