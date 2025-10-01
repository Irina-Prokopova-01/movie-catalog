from typing import Annotated

from fastapi import APIRouter, status, Depends

from api.api_v1.mouvie_a.crud import storage
from api.api_v1.mouvie_a.dependencies import read_movie
from schemas.movie import BaseMovie, UpdateMovie, UpdatePartialMovie, MovieRead

router = APIRouter(
    prefix="/movies",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    }
                },
            },
        },
    },
)

MOVIE_DEP = Annotated[BaseMovie, Depends(read_movie)]


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie_by_slug(
    movie: MOVIE_DEP,
    # background_tasks: BackgroundTasks,
) -> None:
    # background_tasks.add_task(storage.save_state)
    storage.delete_by_slug(slug=movie.slug)


@router.put(
    "/{slug}",
    response_model=MovieRead,
)
def update_movie(
    movie: MOVIE_DEP,
    movie_update: UpdateMovie,
    # background_tasks: BackgroundTasks,
):
    # background_tasks.add_task(storage.save_state)
    return storage.update(
        movie_base=movie,
        movie_update=movie_update,
    )


@router.patch(
    "/{slug}",
    response_model=MovieRead,
)
def update_partial_movie(
    movie: MOVIE_DEP,
    movie_update_in: UpdatePartialMovie,
    # background_tasks: BackgroundTasks,
):
    # background_tasks.add_task(storage.save_state)
    return storage.update_partial(
        movie_base=movie,
        movie_update_in=movie_update_in,
    )
