import datetime
import jwt
import bcrypt
from core.config import settings


def encode_jwt(
        payload: dict,
        privat_key: str = settings.auth_jwt.privatekey_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes):
    """Создает JWT-токен c ограниченным сроком действия."""

    now = datetime.datetime.now(datetime.UTC)
    to_encode = payload.copy()
    expire = now + datetime.timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)

    encoded = jwt.encode(
        to_encode,
        privat_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.publickey_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm
):
    """Расшифровывает JWT-токен."""
    
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
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
