import datetime
from users.schemas import UserSchema
from .utils import encode_jwt
from core.config import settings


TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: datetime.timedelta | None = None,
) -> str:
    """Создает токен с основанием payload."""

    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_access_token(user: UserSchema) -> str:
    """Создание ACCESS токена для пользователя в виде строчки."""
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload
    )


def create_refresh_token(user: UserSchema) -> str:
    """Создание REFRESH токена для пользователя."""
    jwt_payload = {
        "sub": user.username,
    }

    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=datetime.timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
