from typing import Annotated

from fastapi import APIRouter, Depends, status

from storage.movie_a.crud import storage
from api.api_v1.mouvie_a.dependencies import read_movie
from schemas.movie import Movie, MovieRead, UpdateMovie, UpdatePartialMovie

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    },
                },
            },
        },
    },
)

MOVIE_DEP = Annotated[Movie, Depends(read_movie)]


@router.get("/", response_model=MovieRead)
def read_movie_detail(url: MOVIE_DEP) -> Movie:
    return url


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MOVIE_DEP,
) -> None:
    storage.delete(movie=movie)


@router.put(
    "/",
    response_model=MovieRead,
)
def update_movie(
    movie: MOVIE_DEP,
    movie_update: UpdateMovie,
    # background_tasks: BackgroundTasks,
) -> Movie:
    # background_tasks.add_task(storage.save_state)
    return storage.update(
        movie_base=movie,
        movie_update=movie_update,
    )


@router.patch(
    "/",
    response_model=MovieRead,
)
def update_partial_movie(
    movie: MOVIE_DEP,
    movie_update_in: UpdatePartialMovie,
    # background_tasks: BackgroundTasks,
) -> Movie:
    # background_tasks.add_task(storage.save_state)
    return storage.update_partial(
        movie_base=movie,
        movie_update_in=movie_update_in,
    )


@router.post(
    "/transfer/",
)
def transfer_movie(
    # url: ShortUrlBySlug,
) -> dict[str, str]:
    # 1 / 0
    # начинаем что-то делать...
    # raise NotImplementedError
    return {"result": "work in progress"}
