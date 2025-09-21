from pydantic import BaseModel


class BaseMovie(BaseModel):
    id: int
    title: str
    description: str
    year: int
    rating: float


class Movie(BaseMovie):
    pass
