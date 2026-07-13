import matplotlib
import pandas as pd

# Headless backend (No display for tests)
matplotlib.use("Agg")

from datetime import date

import matplotlib.pyplot as plt

from src.apps.imbalance_settlement.core.settlement_system_prices.visualisation import (
    niv_vs_price_bar_line_plot,
    niv_vs_price_scatter_plot,
)


class TestCharts:

    def test_niv_price_bar_line_plot(self, valid_niv_price_df_data: pd.DataFrame):

        yesterday = date(year=2026, month=1, day=1)
        result = niv_vs_price_bar_line_plot(
            valid_niv_price_df_data, yesterdays_date=yesterday
        )

        assert isinstance(result, plt.Figure)
        plt.close(result)

    def test_niv_price_scatter_plot(self, valid_niv_price_df_data: pd.DataFrame):

        result = niv_vs_price_scatter_plot(valid_niv_price_df_data)

        assert isinstance(result, plt.Figure)
        plt.close(result)
