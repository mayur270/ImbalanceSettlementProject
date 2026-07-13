from src.apps.imbalance_settlement.utils.exceptions import (
    BadRequestError,
    NotFoundError,
)

ERRORS = {
    400: BadRequestError,
    404: NotFoundError,
}

RETRY_STATUS_CODE = {429, 500, 502, 503, 504}
