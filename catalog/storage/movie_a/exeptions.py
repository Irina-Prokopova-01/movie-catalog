class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised on movie creation if such slug already exists
    """
