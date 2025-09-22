from schemas.movie import BaseMovie

LIST_MOVIES = [
    BaseMovie(
        slug="movie_1",
        title="Movie 1",
        description="Movie description1",
        year=2020,
        rating=4.5,
    ),
    BaseMovie(
        slug="movie_2",
        title="Movie 2",
        description="Movie description2",
        year=2025,
        rating=4.7,
    ),
    BaseMovie(
        slug="movie_3",
        title="Movie 3",
        description="Movie description3",
        year=2025,
        rating=4.8,
    ),
]
