import random
import string
from unittest import TestCase


from os import getenv

from api.api_v1.mouvie_a.crud import storage
from schemas.movie import CreateMovie, UpdateMovie, Movie, UpdatePartialMovie

if getenv("TESTING") != "1":
    raise OSError(
        "Environment is not ready for testing",
    )


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def create_movie(self) -> Movie:
        movie_create_new = CreateMovie(
            slug="".join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            title="Movie Title",
            description="Movie Description",
            year=1999,
        )
        return storage.create(movie_create_new)

    def test_update_movie(self):
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
