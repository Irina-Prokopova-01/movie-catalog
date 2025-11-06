import random
import string
from typing import ClassVar
from unittest import TestCase


from os import getenv

from api.api_v1.mouvie_a.crud import storage
from schemas.movie import (
    CreateMovie,
    UpdateMovie,
    Movie,
    UpdatePartialMovie,
)

if getenv("TESTING") != "1":
    raise OSError(
        "Environment is not ready for testing",
    )


def create_movie() -> Movie:
    movie_create_new = CreateMovie(
        slug="".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8,
            )
        ),
        title="Movie Title",
        description="Movie Description",
        year=1999,
    )
    return storage.create(movie_create_new)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

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
        cls.movies = [create_movie() for _ in range(cls.MOVIE_COUNT)]

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
