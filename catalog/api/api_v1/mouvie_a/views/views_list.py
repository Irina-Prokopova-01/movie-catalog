from fastapi import APIRouter, Depends, HTTPException, status
from schemas.movie import BaseMovie, CreateMovie, Movie, MovieRead

from api.api_v1.mouvie_a.crud import MovieAlreadyExistsError, storage
from api.api_v1.mouvie_a.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies_list"],
    dependencies=[
        # Depends(api_token_required_for_unsafe_methods),
        # Depends(user_basic_auth_required_for_unsafe_methods),
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
)


@router.get("/", response_model=list[MovieRead])
def list_all_movies() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(user_basic_auth_required)],
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A movie already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='name' already exists.",
                    },
                },
            },
        },
    },
)
def create_movie(
    movie_create_new: CreateMovie,
) -> BaseMovie:
    try:
        return storage.create_or_raise_if_exists(movie_create_new)
    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie URL with slug={movie_create_new.slug!r} already exists",
        )
