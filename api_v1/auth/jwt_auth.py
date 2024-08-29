from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from api_v1.auth.helpers import (REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD, create_access_token,
                                 create_refresh_token)
from api_v1.auth.validation import get_current_user
from users.schemas import UserSchema

from .crud import users_db
from .utils import validate_password
from .validation import UserGetterFromToken, get_current_user_for_refresh, get_user_from_token_of_type

http_bearer = HTTPBearer(auto_error=False)


class TokenInfo(BaseModel):

    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)]
)


def validate_user_login(
    username: str = Form(),
    password: str = Form(),
):
    """Проверка логина и пароля пользователя"""

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


@router.post("/login", response_model=TokenInfo)
def get_jwt_token(user: UserSchema = Depends(validate_user_login)):
    """Получение JWT токена пользователем."""

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


def get_current_active_user(user: UserSchema = Depends(get_current_user)):
    """Получение активного пользователя."""
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Пользователь не активен!'
    )


@router.get('/users/me')
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_user)
) -> dict:
    """Получение информации о пользователе по его токену."""

    return {
        "username": user.username,
        "email": user.email,
    }


@router.post(
        '/refresh',
        response_model=TokenInfo,
        response_model_exclude_none=True
    )
def refresh_jwt_token(
    user: UserSchema = Depends(get_current_user_for_refresh)
    # ниже приведены различные вариации получения пользователя
    # user: UserSchema = Depends(get_user_from_token_of_type(REFRESH_TOKEN_TYPE))
    # user: UserSchema = Depends(UserGetterFromToken(REFRESH_TOKEN_TYPE))
) -> TokenInfo:
    """Обновление JWT токена."""

    access_token = create_access_token(user)

    return TokenInfo(access_token=access_token)
