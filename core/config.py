from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "shop_db.sqlite3"


class Setting(BaseSettings):
    '''Для подгрузки переменных окружения.'''
    api_v1_prefix: str = '/api/v1'
    db_url: str = f'sqlite+aiosqlite:///{DB_PATH}'
    db_echo: bool = False


settings = Setting()
