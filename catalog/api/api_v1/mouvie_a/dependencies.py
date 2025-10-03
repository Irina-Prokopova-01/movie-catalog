import logging
from idlelib.query import Query
from typing import Annotated

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
    Request,
    Header,
)
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from api.api_v1.mouvie_a.crud import storage
from core.config import API_TOKENS, USERS_DB
from schemas.movie import Movie

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="**API token** fot developer. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="**Basic username** + password auth",
    auto_error=False,
)


def read_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found.",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    log.info("Incoming %r request", request.method)
    # код выполняемый до
    log.info("first time inside dependency save_storage_state")
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add BackgroundTasks to save_storage")
        background_tasks.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("Api token %s", api_token)
    if request.method not in UNSAFE_METHODS:
        return
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )
    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )


def user_basic_auth_required(
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    log.info("User basic auth credentials %s", credentials)
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required.Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
