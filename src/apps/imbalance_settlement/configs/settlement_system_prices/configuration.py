import logging
import os


class BaseConfig:
    BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Logging Config
    LOG_FILE_NAME = "settlement_system_prices.log"
    LOGGING_LEVEL = logging.DEBUG


class DevConfig(BaseConfig):
    ENVIRONMENT = "dev"


CONFIG = {
    "dev": DevConfig,
}

environment = os.getenv("ENVIRONMENT", "dev")
config = CONFIG[environment]
