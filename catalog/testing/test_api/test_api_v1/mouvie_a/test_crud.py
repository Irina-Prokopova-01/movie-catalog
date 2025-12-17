from os import getenv
from typing import ClassVar
from unittest import TestCase

import pytest

from storage.movie_a.crud import storage
from storage.movie_a.exeptions import MovieAlreadyExistsError
from schemas.movie import (
    CreateMovie,
    Movie,
    UpdateMovie,
    UpdatePartialMovie,
)
from testing.conftest import create_movie_random_slug


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        if getenv("TESTING") != "1":
            raise OSError(
                "Environment is not ready for redis testing",
            )
        self.movie = create_movie_random_slug()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update_movie(self) -> None:
        # movie = self.create_movie()
        movie_update = UpdateMovie(
            **self.movie.model_dump(),
        )
        source_description = self.movie.description
        movie_update.description *= 2
        movie_update_storage = storage.update(
            movie_base=self.movie,
            movie_update=movie_update,
        )
        self.assertNotEqual(
            source_description,
            movie_update_storage.description,
        )
        self.assertEqual(
            movie_update,
            UpdateMovie(**movie_update_storage.model_dump()),
        )

    def test_update_partial_movie(self) -> None:
        # movie = self.create_movie()
        movie_update_partial = UpdatePartialMovie(
            **self.movie.model_dump(),
        )
        source_description = self.movie.description
        if source_description is not None:
            movie_update_partial.description = source_description * 2
        else:
            movie_update_partial.description = "default_description"
        movie_update_partial.description *= 2
        movie_update_partial_storage = storage.update_partial(
            movie_base=self.movie,
            movie_update_in=movie_update_partial,
        )
        self.assertNotEqual(
            source_description,
            movie_update_partial.description,
        )
        self.assertEqual(
            movie_update_partial.description,
            movie_update_partial_storage.description,
        )


class MovieStorageGetMoviesTestCase(TestCase):
    MOVIE_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie_random_slug() for _ in range(cls.MOVIE_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        expected_slugs = {m.slug for m in self.movies}
        slugs = {m.slug for m in movies}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_movie = storage.get_by_slug(movie.slug)
                self.assertEqual(movie, db_movie)


def test_create_or_raise_if_exists(movie: Movie) -> None:
    # existing_movie = create_movie()
    movie_create = CreateMovie(**movie.model_dump())
    # movie_create.slug += "asc"
    with pytest.raises(MovieAlreadyExistsError) as exc_info:
        storage.create_or_raise_if_exists(movie_create)

    assert exc_info.value.args[0] == movie_create.slug
    # assert exc_info.value.args[0] == movie_create.slug + "asdf"
