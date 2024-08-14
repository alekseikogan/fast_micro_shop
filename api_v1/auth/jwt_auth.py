from .utils import hash_password, validate_password, encode_jwt
from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel

from users.schemas import UserSchema


class TokenInfo(BaseModel):

    access_token: str
    token_type: str


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

    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,
    }

    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer')
