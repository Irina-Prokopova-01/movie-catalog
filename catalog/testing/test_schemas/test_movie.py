from unittest import TestCase

from schemas.movie import CreateMovie, Movie


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_created_schemas(self):
        movie_in = CreateMovie(
            slug="some-slug",
            description="Some description",
            title="Some title",
            year=1999,
        )
        movie_out = Movie(
            **movie_in.model_dump(),
        )
        self.assertEqual(
            movie_out.slug,
            movie_in.slug,
        )
        self.assertEqual(
            movie_out.description,
            movie_in.description,
        )
        self.assertEqual(
            movie_out.title,
            movie_in.title,
        )
        self.assertEqual(
            movie_out.year,
            movie_in.year,
        )
