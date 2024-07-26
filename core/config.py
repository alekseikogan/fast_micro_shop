from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "shop_db.sqlite3"


class Setting(BaseSettings):
    '''Для подгрузки переменных окружения.'''
    db_url: str = f'sqlite+aiosqlite:///{DB_PATH}'
    db_echo: bool = True


settings = Setting()
