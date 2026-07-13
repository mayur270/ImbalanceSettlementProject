import numpy as np
import pandas as pd


class TimeSeries:

    @staticmethod
    def create_time_series_df(df: pd.DataFrame) -> pd.DataFrame:
        """Adding HH time to dataframe.
        :param df: Validated dataframe
        :return: Timeseries dataframe
        """
        df["UTCDateTime"] = (
            pd.to_datetime(df["settlementDate"], utc=True)
            + pd.to_timedelta((df["settlementPeriod"] - 1) * 30, unit="m")
        ).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return df

    @staticmethod
    def calculate_imbalance_metrics(df: pd.DataFrame) -> dict:
        """Calculates daily imbalance cost and unit rate.

        Formulas:
            1. total_imbalance_cost =
                Σ ((systemBuyPrice(SBP) or systemSellPrice(SSP)) x net_imbalance_volume)

            note: Single price regime from 2015-11-06, therefore SBP=SSP
                Prior to this date, no data is available from api.

            2. imbalance_unit_rate =
                total_imbalance_cost (net) / (absolute Σ(imbalance_volume))
        """

        net_imbalance_volume, system_buy_price, system_sell_price = (
            df[["netImbalanceVolume", "systemBuyPrice", "systemSellPrice"]].to_numpy().T
        )

        # Checking if sell_price matches buy_price in case there are errors
        if not np.array_equal(system_buy_price, system_sell_price):
            mismatch = np.flatnonzero(system_buy_price != system_sell_price)
            raise ValueError(
                f"Mismatch at indices: {mismatch}. "
                f"buy_price values: {system_buy_price[mismatch]}"
                f"sell_price values: {system_sell_price[mismatch]}"
            )

        # Calculating total imbalance cost
        total_daily_imbalance_cost = np.dot(system_buy_price, net_imbalance_volume)

        # Calculating net imbalance volume
        total_net_imbalance_volume = np.sum(net_imbalance_volume)

        # Calculating imbalance unit rate
        imbalance_unit_rate = total_daily_imbalance_cost / np.abs(
            total_net_imbalance_volume
        )

        metrics = {
            "total_daily_imbalance_cost": round(float(total_daily_imbalance_cost), 2),
            "imbalance_unit_rate": round(float(imbalance_unit_rate), 2),
        }

        return metrics


imbalance_time_series = TimeSeries()
