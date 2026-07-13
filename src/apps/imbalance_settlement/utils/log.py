import logging
from pathlib import Path

from src.apps.imbalance_settlement.configs.settlement_system_prices.configuration import (
    config,
)


def get_logger(log_path: Path | None = None) -> logging.getLogger:
    """For message or error logging purposes."""

    _logger = logging.getLogger(__name__)
    _logger.setLevel(config.LOGGING_LEVEL)

    if not _logger.handlers:
        if log_path is None:
            log_dir = Path(__file__).resolve().parent.parent / "logs"
            log_dir.mkdir(exist_ok=True)
            log_path = log_dir / config.LOG_FILE_NAME

        handler = logging.FileHandler(filename=log_path)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)

        _logger.addHandler(handler)

    return _logger


logger = get_logger()
