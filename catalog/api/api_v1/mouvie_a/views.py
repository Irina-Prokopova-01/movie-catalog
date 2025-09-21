from typing import Annotated
from annotated_types import Len
import random
from fastapi import APIRouter, status, Form

from api.api_v1.mouvie_a.crud import LIST_MOVIES
from schemas.movie import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies_list"],
)


@router.get("/list_movies/", response_model=list[Movie])
def list_all_movies():
    return LIST_MOVIES


movies: list[Movie] = []


@router.post(
    "/create_movie/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    id: Annotated[int, Form()],
    title: Annotated[str, Len(max_length=20, min_length=3), Form()],
    description: Annotated[str, Len(max_length=100, min_length=20), Form()],
    year: Annotated[int, Form()],
    rating: Annotated[float, Form()],
) -> Movie:
    movie_id = random.randint(3, 1000)
    new_movie = Movie(
        id=movie_id,
        title=title,
        description=description,
        year=year,
        rating=rating,
    )
    movies.append(new_movie)
    return new_movie
