from datetime import date
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from pydantic import ValidationError

from src.apps.imbalance_settlement.tests.test_settlement_system_prices.test_utils.conftest import (
    missing_settlement_period_data,
)
from src.apps.imbalance_settlement.utils.schema import ImbalanceSettlementDataSchema
from src.apps.imbalance_settlement.utils.validate import validator


def make_validation_error():
    return ValidationError.from_exception_data(
        title="ImbalanceSettlementDataSchema",
        line_errors=[
            {
                "type": "missing",
                "loc": ("settlementDate",),
                "input": {},
            }
        ],
    )


class TestValidateDataTypeSuccess:

    @patch("src.apps.imbalance_settlement.utils.validate.TypeAdapter")
    def test_validate_datatype_return_schema_success(
        self, mock_type_adapter, mock_valid_data
    ):
        mock_validator = MagicMock()
        mock_type_adapter.return_value = mock_validator

        expected_result = ImbalanceSettlementDataSchema(**mock_valid_data)

        mock_validator.validate_python.return_value = expected_result

        result = validator.validate_datatype(
            ImbalanceSettlementDataSchema,
            mock_valid_data,
        )

        # Checking with assert
        assert result == expected_result
        assert isinstance(result, ImbalanceSettlementDataSchema)

        mock_type_adapter.assert_called_once_with(ImbalanceSettlementDataSchema)

        mock_validator.validate_python.assert_called_once_with(mock_valid_data)


class TestValidateDataTypeHandlingError:

    @patch("src.apps.imbalance_settlement.utils.validate.TypeAdapter")
    def test_validate_datatype_raises_validation_error(
        self, mock_type_adapter, mock_valid_data
    ):
        """unitest test for exception handling logic
        e.g. if TypeAdapter unexpectedly gives error"""
        mock_validator = MagicMock()
        mock_type_adapter.return_value = mock_validator

        mock_validator.validate_python.side_effect = make_validation_error()

        with pytest.raises(ValueError, match="Validation failed"):
            validator.validate_datatype(ImbalanceSettlementDataSchema, mock_valid_data)

        # Checking with assert
        mock_type_adapter.assert_called_once_with(ImbalanceSettlementDataSchema)

        mock_validator.validate_python.assert_called_once_with(mock_valid_data)

    @pytest.mark.parametrize(
        "schema_field,incorrect_data",
        [
            # Date Field
            ("settlementDate", "not-a-date"),
            ("settlementDate", 123),
            ("settlementDate", None),
            ("settlementDate", True),
            # DateTime Field
            ("createdDateTime", ""),
            ("createdDateTime", None),
            ("createdDateTime", 123),
            ("startTime", "datetime"),
            ("startTime", True),
            # Int Field
            ("settlementPeriod", "one"),
            ("settlementPeriod", None),
            ("settlementPeriod", ""),
            ("settlementPeriod", 1.234),
            ("settlementPeriod", False),
            ("settlementPeriod", 51),  # Checking upper limit
            ("settlementPeriod", 0),  # Checking lower limit
            # Float Field
            ("systemBuyPrice", None),
            ("systemBuyPrice", "1.234"),
            ("systemBuyPrice", True),
            # String Field
            ("priceDerivationCode", 123),
            ("priceDerivationCode", True),
        ],
    )
    def test_validate_datatype_invalid_field_type(
        self,
        mock_valid_data,
        schema_field,
        incorrect_data,
    ):
        data = mock_valid_data.copy()
        data[schema_field] = incorrect_data

        with pytest.raises(ValueError) as exc:
            validator.validate_datatype(
                ImbalanceSettlementDataSchema,
                data,
            )

        assert "Validation failed" in str(exc.value)
        assert schema_field in str(exc.value)


class TestValidatePayloadHandlingError:

    def test_validate_payload_when_data_is_empty_value_error(self):
        payload = {"data": [], "metadata": ["DATASETS"]}

        with pytest.raises(ValueError, match="Payload 'data' is empty."):
            validator.validate_payload(
                payload=payload,
                yesterdays_date=date(year=2026, month=1, day=1),
            )

    @patch("src.apps.imbalance_settlement.utils.validate.logger")
    @patch(
        "src.apps.imbalance_settlement.utils.validate.get_settlement_period",
        return_value=5,
    )
    def test_validate_payload_missing_settlement_period_are_logged(
        self,
        mock_get_periods,
        mock_logger,
        missing_settlement_period_data,
        mock_valid_data,
    ):

        validator.validate_payload(
            payload=missing_settlement_period_data,
            yesterdays_date=date(year=2026, month=1, day=1),
        )

        mock_logger.error.assert_called_once_with("Missing settlement periods: [2, 4]")

        assert mock_get_periods.return_value == 5

    @patch("src.apps.imbalance_settlement.utils.validate.logger")
    @patch(
        "src.apps.imbalance_settlement.utils.validate.get_settlement_period",
        return_value=48,
    )
    def test_validate_payload_by_removing_duplicates(
        self,
        mock_get_periods,
        mock_logger,
        duplicate_settlement_period_data,
        mock_valid_data,
    ):
        validator.validate_payload(
            payload=duplicate_settlement_period_data,
            yesterdays_date=date(year=2025, month=1, day=1),
        )

        mock_logger.error.assert_called_once_with(
            "Duplicate settlement period(s) removed: {10}"
        )


class TestValidatePayloadSuccess:

    @patch(
        "src.apps.imbalance_settlement.utils.validate.get_settlement_period",
        return_value=48,
    )
    def test_validate_payload_returns_df_success(
        self, mock_get_periods, settlement_period_data, mock_valid_data
    ):
        result = validator.validate_payload(
            payload=settlement_period_data,
            yesterdays_date=date(year=2025, month=1, day=1),
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 48
