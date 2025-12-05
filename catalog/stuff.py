from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.connection.db,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    redis.set("name", "Andrey")
    redis.set("foo", "Star")
    redis.set("number", "43")
    print(
        [
            redis.get("name"),
            redis.get("foo"),
            redis.get("spam"),
        ],
    )
    redis.delete("name")
    print(redis.get("name"))


if __name__ == "__main__":
    main()
