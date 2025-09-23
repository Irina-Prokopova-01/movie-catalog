from fastapi import HTTPException, status, APIRouter

from api.api_v1.mouvie_a.crud import storage
from schemas.movie import BaseMovie

router = APIRouter(
    prefix="/movie",
    tags=["Movies_detail"],
)


@router.get("/{movie_slug}", response_model=BaseMovie)
def read_movie(slug: str) -> BaseMovie:
    movie: BaseMovie | None = storage.get_by_slug(slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found.",
    )
