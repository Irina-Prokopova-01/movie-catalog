from pydantic import BaseModel


class BaseMovie(BaseModel):
    title: str
    description: str = ""
    year: int


class CreateMovie(BaseMovie):
    slug: str


class UpdateMovie(BaseMovie):
    title: str
    description: str
    year: int


class UpdatePartialMovie(BaseMovie):
    title: str | None = None
    description: str | None = None
    year: int | None = None


class MovieRead(BaseMovie):
    """Модель для чтения данных о фильмах"""

    slug: str


class Movie(BaseMovie):
    slug: str
    notes: str
