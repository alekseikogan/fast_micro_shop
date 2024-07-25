from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    '''Для подгрузки переменных окружения.'''
    db_url: str = 'sqlite+aiosqlite:/// ./shop_db.sqlite3'
    db_echo: bool = True


settings = Setting()
