from pydantic import BaseModel


class BaseMovie(BaseModel):
    slug: str
    title: str
    description: str
    year: int
    rating: float


class CreateMovie(BaseMovie):
    title: str
    description: str
    year: int
    rating: float


class UpdateMovie(BaseMovie):
    title: str
    description: str
    year: int


class MovieResponse(BaseModel):
    slug: str
    title: str
    description: str
    year: int
    rating: float
