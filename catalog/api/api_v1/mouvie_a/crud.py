from pydantic import BaseModel

from schemas.movie import BaseMovie, CreateMovie, UpdateMovie


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

    def delete_by_slug(self, slug) -> None:
        self.slug_movies.pop(slug, None)

    def delete(self, movie_delete: BaseMovie) -> None:
        self.delete_by_slug(slug=movie_delete.slug)

    def update(self, movie_base: BaseMovie, movie_update: UpdateMovie) -> BaseMovie:
        for k, v in movie_update:
            setattr(movie_base, k, v)
        return movie_base


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
