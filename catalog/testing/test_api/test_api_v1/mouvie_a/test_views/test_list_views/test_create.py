import random
import string
from http.client import responses
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from fastapi import status

from main import app
from schemas.movie import CreateMovie, Movie
from testing.conftest import build_create_movie_random_slug


pytestmark = pytest.mark.apitest


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    movie_create = CreateMovie(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=10,
            ),
        ),
        description="A short url",
        year=1999,
        title="title",
    )
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED, response.text
    received_value = CreateMovie(**response_data)
    assert received_value == movie_create, response_data


def test_create_movie_already_exists(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    movie_create = CreateMovie(**movie.model_dump())
    data = movie_create.model_dump(mode="json")
    url = app.url_path_for("create_movie")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie URL with slug={movie_create.slug!r} already exists"
    assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too-short"),
            pytest.param(("qwerty-foo-param", "string_too_long"), id="max-slug"),
        ]
    )
    def movie_create_values(self, request: SubRequest) -> tuple[dict[str, Any], str]:
        movie = build_create_movie_random_slug()
        data = movie.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        print(slug, err_type)
        return data, err_type

    def test_invalid_slug(
        self,
        movie_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_movie")
        create_data, expected_err_type = movie_create_values
        response = auth_client.post(url=url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_err_type, response.text
