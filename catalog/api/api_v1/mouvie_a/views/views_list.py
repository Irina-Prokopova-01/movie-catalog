from fastapi import APIRouter, status, BackgroundTasks, Depends, HTTPException

from api.api_v1.mouvie_a.crud import storage
from api.api_v1.mouvie_a.dependencies import (
    # api_token_required_for_unsafe_methods,
    user_basic_auth_required_for_unsafe_methods,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.movie import BaseMovie, CreateMovie, MovieRead

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
def list_all_movies() -> list[BaseMovie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(user_basic_auth_required)],
)
def create_movie(
    movie_create_new: CreateMovie,
    # background_tasks: BackgroundTasks,
    # _=Depends(api_token_required,),
) -> BaseMovie:
    if not storage.get_by_slug(movie_create_new):
        return storage.create(movie_create_new)
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Short URL with slug={movie_create_new.slug!r} already exists",
    )
    # background_tasks.add_task(storage.save_state)
