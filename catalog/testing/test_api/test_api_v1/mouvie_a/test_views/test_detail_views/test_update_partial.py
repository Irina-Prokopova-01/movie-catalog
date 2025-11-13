from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.mouvie_a.crud import storage
from main import app
from schemas.movie import Movie
from testing.conftest import create_movie


class TestUpdatePartial:
    @pytest.fixture
    def movie(self, request: SubRequest) -> Generator[Movie]:
        slug, description = request.param
        movie = create_movie(
            slug=slug,
            description=description,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                ("foo", "some description"),
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                ("bar", ""),
                "some-description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                ("max-to-min", "a" * 200),
                "",
                id="max-description-to-min-description",
            ),
            pytest.param(
                ("min-to-max", ""),
                "a" * 200,
                id="min-description-to-max-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self,
        auth_client: TestClient,
        new_description: str,
        movie: Movie,
    ):
        url = app.url_path_for(
            "update_partial_movie",
            slug=movie.slug,
        )
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db.description == new_description
