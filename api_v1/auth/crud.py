from api_v1.auth.utils import hash_password
from users.schemas import UserSchema


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
