from pydantic import BaseModel


class BaseMovie(BaseModel):
    slug: str
    title: str
    description: str
    year: int
    rating: float


class CreateMovie(BaseMovie):
    slug: str
    title: str
    description: str
    year: int
    rating: float


# Модель для ответа (без поля id)
class MovieResponse(BaseModel):
    slug: str
    title: str
    description: str
    year: int
    rating: float
