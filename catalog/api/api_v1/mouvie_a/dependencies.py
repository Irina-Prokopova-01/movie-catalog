import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    Request,
    status,
)
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)
from schemas.movie import Movie

from api.api_v1.auth.services import redis_tokens, redis_users
from api.api_v1.mouvie_a.crud import storage

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


def read_movie(
    slug: str,
) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found.",
    )


def validate_api_token(api_token: HTTPAuthorizationCredentials) -> None:
    if redis_tokens.token_exists(
        api_token.credentials,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
) -> None:
    log.info("Api token %s", api_token)
    if request.method not in UNSAFE_METHODS:
        return
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )
    validate_api_token(api_token=api_token)


def validate_basic_auth(credentials: HTTPBasicCredentials | None) -> None:
    if credentials and redis_users.validate_user_password(
        credentials.username,
        credentials.password,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required.Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return
    validate_basic_auth(credentials=credentials)


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return None

    if api_token:
        return validate_api_token(api_token=api_token)

    if credentials:
        return validate_basic_auth(credentials=credentials)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth required",
    )
