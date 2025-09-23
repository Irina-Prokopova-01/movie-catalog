from typing import Annotated

from fastapi import APIRouter, status, Depends

from api.api_v1.mouvie_a.crud import storage
from api.api_v1.mouvie_a.dependencies import read_movie
from schemas.movie import BaseMovie, CreateMovie

router = APIRouter(
    prefix="/movies",
    tags=["Movies_list"],
)


@router.get("/list_movies/", response_model=list[BaseMovie])
def list_all_movies() -> list[BaseMovie]:
    return storage.get()


@router.post(
    "/create_movie/",
    response_model=BaseMovie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create_new: CreateMovie) -> BaseMovie:
    return storage.create(movie_create_new)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_movie_by_slug(
    movie: Annotated[BaseMovie, Depends(read_movie)],
) -> None:
    storage.delete_by_slug(slug=movie.slug)
