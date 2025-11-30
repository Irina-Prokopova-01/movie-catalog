from unittest import TestCase

from pydantic import ValidationError

from schemas.movie import CreateMovie, Movie, UpdateMovie, UpdatePartialMovie


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_created_schemas(self)-> None:
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

    def test_movie_can_be_update_from_schemas(self)-> None:
        movie_in = UpdateMovie(
            description="Some description",
            title="Some title",
            year=1999,
        )
        movie_out = Movie(
            slug="some-slug",
            **movie_in.model_dump(),
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

    def test_movie_create_accepts_different_urls(self) -> None:
        movie_in = UpdatePartialMovie(
            title="",
            description="Some description",
            year=1999,
        )
        movie_out = Movie(
            slug="some-slug",
            **movie_in.model_dump(),
        )
        self.assertEqual(
            movie_out.title,
            movie_in.title,
        )
        self.assertEqual(
            movie_out.description,
            movie_in.description,
        )
        self.assertEqual(
            movie_out.year,
            movie_in.year,
        )

    def test_movie_create_accepts_different_title(self) -> None:
        title_movies = [
            "movie1",
            "movie2",
            # "Movie about history (Russia, Siberia)",
            "WWW.movie.ru",
            "movie/",
            "rtmps://video.example.com",
        ]
        for title in title_movies:
            with self.subTest(title=title, msg=f"test-title {title}"):
                movie_in = CreateMovie(
                    slug="some-slug",
                    description="Some description",
                    title=title,
                    year=1999,
                )
                self.assertEqual(
                    title,
                    movie_in.model_dump(mode="json")["title"],
                )

    def test_movie_slug_to_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            CreateMovie(
                slug="s",
                description="Some description",
                title="Some title",
                year=1999,
            )
        # print(exc_info.exception)
        # print(exc_info.exception.json())
        # print(exc_info.exception.errors())
        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(expected_type, error_details["type"])

    def test_movie_slug_to_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 2 characters",
        ):
            CreateMovie(
                slug="s",
                description="Some description",
                title="Some title",
                year=1999,
            )
