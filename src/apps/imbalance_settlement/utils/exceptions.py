class APIError(Exception):
    """Base exception for API-related errors."""

    pass


class BadRequestError(APIError):
    """Raised when the API returns HTTP 400."""

    pass


class NotFoundError(APIError):
    """Raised when the API returns HTTP 404."""

    pass


class DateError(Exception):
    """Raised when Date is incorrect."""

    pass
