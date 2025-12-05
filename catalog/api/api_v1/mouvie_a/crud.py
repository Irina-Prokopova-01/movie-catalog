__all__ = ("storage",)

import logging
from collections.abc import Iterable
from typing import cast

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.movie import (
    CreateMovie,
    Movie,
    UpdateMovie,
    UpdatePartialMovie,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.movies,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised on movie creation if such slug already exists
    """


class Storage(BaseModel):
    hash_name: str

    def save_movie(self, new_movie: Movie) -> None:
        redis.hset(
            name=self.hash_name,
            key=new_movie.slug,
            value=new_movie.model_dump_json(),
        )

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(movie)
            for movie in cast(
                Iterable[str],
                redis.hvals(name=self.hash_name),
            )
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(
            name=self.hash_name,
            key=slug,
        ):
            assert isinstance(data, str)
            return Movie.model_validate_json(data)
        return None

    def exists(
        self,
        slug: str,
    ) -> bool:
        return cast(
            bool,
            redis.hexists(
                name=self.hash_name,
                key=slug,
            ),
        )

    def create(self, movie_create_new: CreateMovie) -> Movie:
        new_movie = Movie(
            **movie_create_new.model_dump(),
        )
        self.save_movie(new_movie)
        log.info("Created new movie.%s", new_movie)
        return new_movie

    def create_or_raise_if_exists(self, movie_in: CreateMovie) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in)

        msg = f"Movie {movie_in.slug} already exists."
        raise MovieAlreadyExistsError(movie_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            self.hash_name,
            slug,
        )

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie_base: Movie, movie_update: UpdateMovie) -> Movie:
        for k, v in movie_update:
            setattr(movie_base, k, v)
        self.save_movie(movie_base)
        # self.save_state()
        log.info("Update movie.")
        return movie_base

    def update_partial(
        self,
        movie_base: Movie,
        movie_update_in: UpdatePartialMovie,
    ) -> Movie:
        for k, v in movie_update_in.model_dump(exclude_unset=True).items():
            setattr(movie_base, k, v)
        # self.save_state()
        self.save_movie(movie_base)
        log.info("Update_partial movie.")
        return movie_base


storage = Storage(
    hash_name=settings.redis.collection_names.movie_hash_name,
)
