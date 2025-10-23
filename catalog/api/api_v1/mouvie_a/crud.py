import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import MOVIE_STORAGE_FILEPATH
from schemas.movie import (
    CreateMovie,
    UpdateMovie,
    UpdatePartialMovie,
    Movie,
    MovieRead,
)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)

log = logging.getLogger(__name__)


class Storage(BaseModel):
    slug_movies: dict[str, Movie] = {}

    def save_state(self) -> None:
        for _ in range(30_000):
            MOVIE_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        MOVIE_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info(f"Saved movie to storage file.")

    @classmethod
    def from_state(cls) -> "Storage":
        if not MOVIE_STORAGE_FILEPATH.exists():
            log.info(f"Movie to storage file does not exist.")
            return Storage()
        return cls.model_validate_json(MOVIE_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = Storage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file")
            return

        self.slug_movies.update(
            data.slug_movies,
        )
        log.warning("Recovered data from storage file")

    def save_movie(self, new_movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=new_movie.slug,
            value=new_movie.model_dump_json(),
        )

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(movie)
            for movie in redis.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, movie_slug: str) -> Movie | None:
        if data := redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie_slug,
        ):
            return Movie.model_validate_json(data)

    def create(self, movie_create_new: CreateMovie) -> Movie:
        new_movie = Movie(**movie_create_new.model_dump())
        self.save_movie(new_movie)
        # self.slug_movies[new_movie.slug] = new_movie
        log.info("Created new movie.")
        return new_movie

    def delete_by_slug(self, slug) -> None:
        self.slug_movies.pop(slug, None)
        # self.save_state()
        log.info("Delete_by_slug movie.")

    def delete(self, movie_delete: Movie) -> None:
        self.delete_by_slug(slug=movie_delete.slug)

    def update(self, movie_base: Movie, movie_update: UpdateMovie) -> Movie:
        for k, v in movie_update:
            setattr(movie_base, k, v)
        self.save_movie(movie_base)
        # self.save_state()
        log.info("Update movie.")
        return movie_base

    def update_partial(
        self, movie_base: Movie, movie_update_in: UpdatePartialMovie
    ) -> Movie:
        for k, v in movie_update_in.model_dump(exclude_unset=True).items():
            setattr(movie_base, k, v)
        # self.save_state()
        self.save_movie(movie_base)
        log.info("Update_partial movie.")
        return movie_base


storage = Storage()
