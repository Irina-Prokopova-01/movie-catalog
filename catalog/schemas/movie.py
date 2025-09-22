from pydantic import BaseModel


class BaseMovie(BaseModel):
    id: int
    title: str
    description: str
    year: int
    rating: float


class CreateMovie(BaseModel):
    title: str
    description: str
    year: int
    rating: float


# Модель для ответа (без поля id)
class MovieResponse(BaseModel):
    title: str
    description: str
    year: int
    rating: float
