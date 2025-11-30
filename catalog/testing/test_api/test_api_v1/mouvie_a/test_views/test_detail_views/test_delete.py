
import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.mouvie_a.crud import storage
from main import app
from schemas.movie import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        "some-slug",
        "slug",
        pytest.param("abs", id="minimal-slug"),
        pytest.param("qwerty-foo", id="max-slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    # print(type(request))
    return create_movie(request.param)


@pytest.mark.apitest
def test_delete_by_slug(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)

    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not storage.exists(movie.slug)
