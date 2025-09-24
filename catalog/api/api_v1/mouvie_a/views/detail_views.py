from typing import Annotated

from fastapi import APIRouter, status, Depends

from api.api_v1.mouvie_a.crud import storage
from api.api_v1.mouvie_a.dependencies import read_movie
from schemas.movie import BaseMovie

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


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie_by_slug(
    movie: Annotated[BaseMovie, Depends(read_movie)],
) -> None:
    storage.delete_by_slug(slug=movie.slug)
