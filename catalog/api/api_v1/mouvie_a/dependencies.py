import logging
from idlelib.query import Query
from typing import Annotated

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
    Request,
)

from api.api_v1.mouvie_a.crud import storage
from core.config import API_TOKENS
from schemas.movie import Movie

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


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
        str,
        Query,
    ] = "",
):
    if request.method not in UNSAFE_METHODS:
        return
    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
