import jwt
import bcrypt
from core.config import settings


def encode_jwt(payload, privat_key, algorithm):
    """Создает JWT-токен."""

    encoded = jwt.encode(
        payload: dict,
        privat_key: str = settings.auth_jwt.privatekey_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    )
    return encoded


def decode_jwt(
        token: str,
        public_key: str = settings.auth_jwt.publickey_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    """Расшифровывает JWT-токен."""

    decoded = jwt.decode(
        token,
        public_key
        algorithm=[algorithm],
    )
    return decoded


def hash_password(
    password: str
) -> bytes:
    """Хэширует пароль."""

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Проверка пароля черех хэш."""

    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )
