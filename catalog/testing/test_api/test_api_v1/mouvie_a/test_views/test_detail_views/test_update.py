from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from storage.movie_a.crud import storage
from main import app
from schemas.movie import Movie, UpdateMovie
from testing.conftest import create_movie_random_slug


@pytest.mark.apitest
class TestUpdate:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        description, title, year = request.param
        movie = create_movie_random_slug(
            title=title,
            description=description,
            year=year,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description, new_title, new_year",
        [
            pytest.param(
                ("some description", "movie20", 2000),
                "some description",
                "movie21",
                2000,
                id="change movie",
            ),
            pytest.param(
                ("some description", "movie20", 2000),
                "new description",
                "movie20",
                2000,
                id="change description",
            ),
            pytest.param(
                ("some description", "movie20", 2000),
                "some description",
                "movie20",
                2021,
                id="change year",
            ),
            pytest.param(
                ("some description", "movie20", 2000),
                "new description",
                "movie22",
                2022,
                id="change all",
            ),
            pytest.param(
                ("some description", "movie20", 2000),
                "q",
                "q",
                0,
                id="",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movie,
        auth_client: TestClient,
        new_description: str,
        new_title: str,
        new_year: int,
    ) -> None:
        url = app.url_path_for(
            "update_movie",
            slug=movie.slug,
        )
        update = UpdateMovie(
            description=new_description,
            title=new_title,
            year=new_year,
        )
        response = auth_client.put(url, json=update.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        new_data = UpdateMovie(**movie_db.model_dump())
        assert new_data == update
