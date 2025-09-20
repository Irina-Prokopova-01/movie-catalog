from fastapi import APIRouter

from api.api_v1.mouvie_a.crud import LIST_MOVIES
from schemas.movie import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies_list"],
)


@router.get("/list_movies/", response_model=list[Movie])
def list_all_movies():
    return LIST_MOVIES
