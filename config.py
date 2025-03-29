from pydantic_settings import SettingsConfigDict, BaseSettings

DEBUG = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env-dev' if DEBUG else 'deploy/.env',
        env_file_encoding='utf-8'
    )

    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()

DATABASE_URL = (f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
                f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}?async_fallback=True')

VERSION = 1
