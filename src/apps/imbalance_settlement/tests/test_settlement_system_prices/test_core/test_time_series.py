import pytest

from src.apps.imbalance_settlement.core.settlement_system_prices.time_series import (
    TimeSeries,
)

time_series = TimeSeries()


def test_create_time_series_df_success(valid_time_series_data):
    result = time_series.create_time_series_df(valid_time_series_data)

    assert "UTCDateTime" in result.columns
    assert result["UTCDateTime"].to_list() == [
        "2025-01-01T00:00:00Z",
        "2025-01-01T00:30:00Z",
    ]


def test_calculate_imbalance_metrics_success(valid_imbalance_metrics_data):

    result = time_series.calculate_imbalance_metrics(valid_imbalance_metrics_data)

    assert result == {
        "total_daily_imbalance_cost": 1700.0,
        "imbalance_unit_rate": 56.67,
    }


def test_calculate_imbalance_metrics_value_error(invalid_buy_sell_prices_data):

    with pytest.raises(ValueError) as exc_info:
        time_series.calculate_imbalance_metrics(invalid_buy_sell_prices_data)

    assert str(exc_info.value) == (
        "Mismatch at indices: [1]. buy_price values: [70.]sell_price values: [60.]"
    )
