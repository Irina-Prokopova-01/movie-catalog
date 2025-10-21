import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIE_STORAGE_FILEPATH = BASE_DIR / "movie_list.json"

# C:\Users\User\PycharmProjects\movie-catalog\catalog\core\config.py
LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS: frozenset[str] = frozenset(
    {
        "Ykn4HsTExNoSwPAmwEt-3Q",
        "rrSpMES6ozOvoxQKTTGc8g",
    }
)

USERS_DB: dict[str, str] = {
    "sam": "passw1",
    "bob": "pass2",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2

REDIS_TOKENS_SET_NAME = "tokens"
