import logging

from pydantic import BaseModel, ValidationError

from core.config import MOVIE_STORAGE_FILEPATH
from schemas.movie import (
    CreateMovie,
    UpdateMovie,
    UpdatePartialMovie,
    Movie,
    MovieRead,
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

    def get(self) -> list[Movie]:
        return list(self.slug_movies.values())

    def get_by_slug(self, movie_slug) -> Movie | None:
        return self.slug_movies.get(movie_slug)

    def create(self, movie_create_new: CreateMovie) -> Movie:
        new_movie = Movie(**movie_create_new.model_dump())
        self.slug_movies[new_movie.slug] = new_movie
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
        # self.save_state()
        log.info("Update movie.")
        return movie_base

    def update_partial(
        self, movie_base: Movie, movie_update_in: UpdatePartialMovie
    ) -> Movie:
        for k, v in movie_update_in.model_dump(exclude_unset=True).items():
            setattr(movie_base, k, v)
        # self.save_state()
        log.info("Update_partial movie.")
        return movie_base


storage = Storage()
