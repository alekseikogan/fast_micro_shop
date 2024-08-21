from users.schemas import UserSchema
from .utils import encode_jwt

TOKEN_TYPE_FIELD = 'type'


def create_jwt(token_type: str, token_data: dict) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=jwt_payload)


def create_access_token(user: UserSchema) -> str:
    """Создание токена для пользователя в виде строчки."""
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    return create_jwt(token_type="", token_data=jwt_payload)


def create_refresh_token(user: UserSchema) -> str:
    """Создание REFRESH токена для пользователя."""

    return encode_jwt(jwt_payload)
