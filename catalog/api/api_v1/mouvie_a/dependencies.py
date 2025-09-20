from fastapi import HTTPException, status, APIRouter

from api.api_v1.mouvie_a.crud import LIST_MOVIES
from schemas.movie import Movie

router = APIRouter(
    prefix="/movie",
    tags=["Movies_detail"],
)


@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int):
    for movie in LIST_MOVIES:
        if movie.movie_id == movie_id:
            return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {movie_id!r} not found.",
    )
