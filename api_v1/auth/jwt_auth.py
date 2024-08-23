from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel

from api_v1.auth.helpers import create_access_token, create_refresh_token
from users.schemas import UserSchema

from .utils import decode_jwt, hash_password, validate_password

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


class TokenInfo(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


alex = UserSchema(
    username='alex',
    password=hash_password('Noah 575'),
    email='alex@yandex.ru'
    )

anna = UserSchema(
    username="anna",
    password=hash_password("Noah 575")
)

users_db: dict[str, UserSchema] = {
    alex.username: alex,
    anna.username: anna
}

router = APIRouter(
    prefix='/jwt',
    tags=['JWT']
)


def validate_user_login(
    username: str = Form(),
    password: str = Form(),
):
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


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    """Получает payload для передачи далее."""

    # token = credentials.credentials

    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Неверный токен: {e}'
        )

    return payload


def get_current_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    """Получает данные о пользователе по payload."""

    username: str = payload.get('sub')
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Пользователь не найден!'
    )


def get_current_active_user(user: UserSchema = Depends(get_current_user)):
    """Получение активного пользователя."""
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Пользователь неактивен!'
    )


@router.get('/users/me')
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_user)
):
    """Получение информации о пользователе по его токену."""

    return {
        "username": user.username,
        "email": user.email,
    }
