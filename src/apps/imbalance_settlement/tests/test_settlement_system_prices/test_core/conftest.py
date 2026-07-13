import pandas as pd
import pytest


@pytest.fixture
def valid_time_series_data():
    return pd.DataFrame(
        {
            "settlementDate": [
                pd.Timestamp("2025-01-01").date(),
                pd.Timestamp("2025-01-01").date(),
            ],
            "settlementPeriod": [
                1,
                2,
            ],
        }
    )


@pytest.fixture
def valid_imbalance_metrics_data():
    return pd.DataFrame(
        {
            "netImbalanceVolume": [
                10,
                20,
            ],
            "systemBuyPrice": [
                50.0,
                60.0,
            ],
            "systemSellPrice": [
                50.0,
                60.0,
            ],
        }
    )


@pytest.fixture
def invalid_buy_sell_prices_data():
    return pd.DataFrame(
        {
            "netImbalanceVolume": [
                10,
                20,
            ],
            "systemBuyPrice": [
                50.0,
                70.0,
            ],
            "systemSellPrice": [
                50.0,
                60.0,
            ],
        }
    )


@pytest.fixture
def valid_niv_price_df_data():
    return pd.DataFrame(
        {
            "UTCDateTime": pd.date_range("2026-07-12", periods=48, freq="30min"),
            "netImbalanceVolume": [100, -200] * 24,
            "systemSellPrice": [50.0, 120.0] * 24,
        }
    )
