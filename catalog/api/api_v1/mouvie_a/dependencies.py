from fastapi import HTTPException, status, APIRouter

from api.api_v1.mouvie_a.crud import LIST_MOVIES
from schemas.movie import BaseMovie

router = APIRouter(
    prefix="/movie",
    tags=["Movies_detail"],
)


@router.get("/{movie_id}", response_model=BaseMovie)
def read_movie(slug: str):
    for movie in LIST_MOVIES:
        if movie.slug == slug:
            return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found.",
    )
