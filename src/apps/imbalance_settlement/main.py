from src.apps.imbalance_settlement.configs.settlement_system_prices.configuration import (
    config,
)
from src.apps.imbalance_settlement.core.settlement_system_prices.app import (
    ImbalanceApplication,
)
from src.apps.imbalance_settlement.utils.log import logger


def main() -> None:
    """
    Start the application.
    """
    logger.info(f"Application started | Environment: {config.ENVIRONMENT}")

    try:
        app = ImbalanceApplication()
        app.run()
    except Exception:
        logger.exception("Imbalance settlement application terminated.")
        raise


if __name__ == "__main__":

    import timeit

    runs = 1
    execution_time = timeit.timeit(lambda: main(), number=runs)
    average_time = execution_time / runs

    print(f"Execution time : {execution_time * 1000:.4f} ms")
    print(f"Average execution time : {average_time * 1000:.4f} ms")
