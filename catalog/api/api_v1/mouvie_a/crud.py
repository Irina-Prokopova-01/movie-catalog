from pydantic import BaseModel

from schemas.movie import BaseMovie, CreateMovie


class Storage(BaseModel):
    slug_movies: dict[str, BaseMovie] = {}

    def get(self) -> list[BaseMovie]:
        return list(self.slug_movies.values())

    def get_by_slug(self, movie_slug) -> BaseMovie | None:
        return self.slug_movies.get(movie_slug)

    def create(self, movie_create_new: CreateMovie) -> BaseMovie:
        new_movie = BaseMovie(**movie_create_new.model_dump())
        self.slug_movies[new_movie.slug] = new_movie
        return new_movie


storage = Storage()

storage.create(
    CreateMovie(
        slug="movie_3",
        title="Movie 3",
        description="Movie description3",
        year=2025,
        rating=4.8,
    )
)
storage.create(
    CreateMovie(
        slug="movie_2",
        title="Movie 2",
        description="Movie description2",
        year=2024,
        rating=4.7,
    )
)
