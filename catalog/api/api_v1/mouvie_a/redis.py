import secrets
from abc import ABC, abstractmethod

from redis import Redis
from core import config

# redis_tokens = Redis(
#     host=config.REDIS_HOST,
#     port=config.REDIS_PORT,
#     db=config.REDIS_DB_TOKENS,
#     decode_responses=True,
# )


class AbstractTokensHelper(ABC):
    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Check if token exists.
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Save token in storage.
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokensHelper(AbstractTokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        token_set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.token_set = token_set_name

    def token_exists(self, token: str) -> bool:
        return bool(self.redis.sismember(self.token_set, token))

    def add_token(self, token: str) -> None:
        self.redis.sadd(self.token_set, token)


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    token_set_name=config.REDIS_TOKENS_SET_NAME,
)
