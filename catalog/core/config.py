import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_format: str = LOG_FORMAT
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = ""
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisCollectionNameConfig(BaseModel):
    tokens_set: str = "tokens"
    movie_hash_name: str = "movies-hash"


class RedisDataBaseConfig(BaseSettings):
    default: int = 0
    tokens: int = 1
    users: int = 2
    movies: int = 3


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    collection_names: RedisCollectionNameConfig = RedisCollectionNameConfig()
    db: RedisDataBaseConfig = RedisDataBaseConfig()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)
    redis: RedisConfig = RedisConfig()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
# print(settings.logging)
# print(settings.logging.log_level)
