from typing import Annotated
from annotated_types import Len
import random
from fastapi import APIRouter, status, Form

from api.api_v1.mouvie_a.crud import LIST_MOVIES
from schemas.movie import BaseMovie, CreateMovie, MovieResponse

router = APIRouter(
    prefix="/movies",
    tags=["Movies_list"],
)

movies: list[BaseMovie] = []


@router.get("/list_movies/", response_model=list[BaseMovie])
def list_all_movies():
    return movies


@router.post(
    "/create_movie/",
    response_model=BaseMovie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: CreateMovie) -> BaseMovie:
    # Генерируем случайный id
    movie_id = random.randint(3, 1000)
    new_movie = BaseMovie(id=movie_id, **movie_create.model_dump())
    movies.append(new_movie)
    return BaseMovie(**new_movie.model_dump())
