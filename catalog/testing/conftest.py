import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.mouvie_a.crud import storage
from schemas.movie import CreateMovie, Movie


@pytest.fixture(scope="session", autouse=True)
def check_testing_env()->None:
    if getenv("TESTING") != "1":
        pytest.exit(
            "Environment is not ready for pytest testing",
        )


def build_create_movie(
    slug: str,
    description: str = "Movie Description",
    title: str = "Movie Title",
    year: int = 2000,
) -> CreateMovie:
    return CreateMovie(
        slug=slug,
        title=title,
        description=description,
        year=year,
    )


def build_create_movie_random_slug(
    description: str = "Movie Description",
    title: str = "Movie Title",
    year: int = 1999,
) -> CreateMovie:
    return build_create_movie(
        slug="".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8,
            ),
        ),
        description=description,
        title=title,
        year=year,
    )


def create_movie(
    slug: str,
    description: str = "Movie Description",
    title: str = "Movie Title",
    year: int = 1999,
) -> Movie:
    movie = build_create_movie(
        slug=slug,
        description=description,
        title=title,
        year=year,
    )
    return storage.create(movie)


def create_movie_random_slug(
    description: str = "Movie Description",
    title: str = "Movie Title",
    year: int = 1999,
) -> Movie:
    movie = build_create_movie_random_slug(
        description=description,
        title=title,
        year=year,
    )
    return storage.create(movie)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    # print("Created Movie", movie.slug)
    yield movie
    storage.delete(movie)
    # print("Deleted short url %s", movie.slug)
