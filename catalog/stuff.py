from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
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
