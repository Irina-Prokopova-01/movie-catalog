from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.api_v1.auth.services import redis_tokens
from api.api_v1.mouvie_a.crud import storage
from api.api_v1.mouvie_a.views.views_list import create_movie
from main import app
from schemas.movie import Movie


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def auth_token() -> Generator[str]:
    token = redis_tokens.generate_and_save_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture()
def auth_client(
    auth_token: str,
) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app, headers=headers) as client:
        yield client
