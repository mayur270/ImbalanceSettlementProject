from datetime import date
from typing import TypeVar

import numpy as np
import pandas as pd
from pydantic import TypeAdapter, ValidationError

from src.apps.imbalance_settlement.utils.log import logger
from src.apps.imbalance_settlement.utils.schema import ImbalanceSettlementDataSchema
from src.apps.imbalance_settlement.utils.util import get_settlement_period

T = TypeVar("T")


class Validator:
    """Generic validator class."""

    @staticmethod
    def validate_datatype(schema: type[T], data: dict) -> T:
        """Generic pydantic dataclass validation function.
        :param schema: schema for data validation
        :param data: This is the payload data
        """
        try:
            schema_validator = TypeAdapter(schema)
            validate_request = schema_validator.validate_python(data)
            return validate_request
        except ValidationError as e:
            errors = [
                f"Field: {'.'.join(map(str, error.get('loc')))}\n"
                f"Error: {error.get('msg')}\n"
                f"Type: {error.get('type')}"
                for error in e.errors()
            ]
            raise ValueError("Validation failed:\n\n" + "\n\n".join(errors)) from e

    @staticmethod
    def validate_payload(payload: dict, yesterdays_date: date) -> pd.DataFrame:
        """Validates payload data.
        :param payload: 'data' from API payload dict e.g. {'metadata': [], 'data': []}
        :param yesterdays_date: yesterday's date
        :return: Pandas DataFrame
        """

        # Check if required 'data' is not empty
        request_data_payload = payload.get("data")
        if not request_data_payload:
            raise ValueError("Payload 'data' is empty.")

        settlement_periods = get_settlement_period(yesterdays_date=yesterdays_date)

        seen = np.zeros(settlement_periods, dtype=bool)

        duplicate_periods = set()

        for record in request_data_payload:
            # Below validates the schema datatype. Generally all is validated but
            # let's assume metadata data will never be used.
            Validator.validate_datatype(ImbalanceSettlementDataSchema, record)

            # Subtracting by 1 as Python starts from 0.
            period = record["settlementPeriod"] - 1

            # Checking for duplicates
            if seen[period]:
                duplicate_periods.add(record["settlementPeriod"])
            seen[period] = True

        # Check for missing periods
        missing_periods = np.where(~seen)[0] + 1
        if missing_periods.size:
            logger.error(f"Missing settlement periods: {missing_periods.tolist()}")
            # raise ValueError(f"Missing settlement periods: {missing_periods.tolist()}")

        df = pd.DataFrame(request_data_payload)
        if duplicate_periods:
            df.drop_duplicates(subset=["settlementPeriod"], keep="first", inplace=True)
            logger.error(f"Duplicate settlement period(s) removed: {duplicate_periods}")

        return df


validator = Validator()
