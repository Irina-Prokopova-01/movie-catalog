import random
import string
from collections.abc import Generator
from os import getenv
import pytest

from api.api_v1.mouvie_a.crud import storage
from api.api_v1.mouvie_a.views.views_list import create_movie
from schemas.movie import Movie, CreateMovie

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for pytest testing",
    )


def build_create_movie(slug: str) -> CreateMovie:
    return CreateMovie(
        slug=slug,
        title="Movie Title",
        description="Movie Description",
        year=1999,
    )


def build_create_movie_random_slug() -> CreateMovie:
    return build_create_movie(
        slug="".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8,
            ),
        ),
    )


def create_movie(slug: str) -> Movie:
    movie = build_create_movie(slug)
    return storage.create(movie)


def create_movie_random_slug() -> Movie:
    movie = build_create_movie_random_slug()
    return storage.create(movie)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie()
    print("Created Movie", movie.slug)
    yield movie
    storage.delete(movie)
    print("Deleted short url %s", movie.slug)
