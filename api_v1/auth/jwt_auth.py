from auth import utils
from auth.utils import hash_password
from fastapi import APIRouter, Depends
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


def validate_user_login():
    pass


@router.post("/login", response_model=TokenInfo)
def get_jwt_token(user: UserSchema = Depends(validate_user_login)):
    """Получение JWT токена пользователем."""

    token = utils.encode_jwt()
    return TokenInfo(
        access_token=token,
        token_type='Bearer')
