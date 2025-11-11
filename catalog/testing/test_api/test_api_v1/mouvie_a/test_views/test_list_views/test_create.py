import random
import string
from typing import Any

from fastapi.testclient import TestClient
from fastapi import status

from main import app
from schemas.movie import CreateMovie


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
