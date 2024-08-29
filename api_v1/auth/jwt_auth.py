from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from api_v1.auth.helpers import create_access_token, create_refresh_token
from users.schemas import UserSchema


from .validation import (get_current_active_user, get_current_user_for_refresh,
                         validate_user_login)

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


@router.post("/login", response_model=TokenInfo)
def get_jwt_token(user: UserSchema = Depends(validate_user_login)):
    """Получение JWT токена пользователем."""

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


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
