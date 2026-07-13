from datetime import date

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure


def niv_vs_price_bar_line_plot(df: pd.DataFrame, yesterdays_date: date) -> Figure:
    """Chart that depicts relationship between netImbalanceVolume and systemPrice.
    :param df: timeseries pandas dataframe
    :return: matplotlib chart
    """

    x = pd.to_datetime(df["UTCDateTime"], utc=True).dt.tz_convert("Europe/London")
    volume = df["netImbalanceVolume"]
    price = df["systemSellPrice"]  # SSP == SBP

    fig, ax1 = plt.subplots(figsize=(12, 5))

    # Net Imbalance Volume
    ax1.bar(
        x,
        volume,
        color=np.where(volume >= 0, "green", "red"),
        alpha=0.5,
        width=0.02,
        label="Imbalance Volume",
    )

    ax1.set_xlabel("Time of day (UK Local)")
    ax1.set_ylabel("Net Imbalance Volume (MWh)")
    ax1.grid(alpha=0.3)

    # Time ticks
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    fig.autofmt_xdate(rotation=45)

    # System Price
    ax2 = ax1.twinx()

    ax2.plot(
        x,
        price,
        color="black",
        marker="o",
        label="System Price",
    )

    ax2.set_ylabel("System Price (£/MWh)")

    formatted_date = yesterdays_date.strftime("%d %B %Y")
    plt.title(
        f"Half-hourly Net Imbalance Volume (NIV) " f"and System Price {formatted_date}"
    )

    # Legend
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    fig.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=2,
        frameon=False,
    )

    fig.tight_layout(rect=[0, 0.08, 1, 1])

    return fig


def niv_vs_price_scatter_plot(df: pd.DataFrame) -> Figure:
    """Plots a scatter plot:
            net_imbalance_volume vs system_sell_price or system_buy_price.
    :param df: timeseries pandas dataframe
    :return: matplotlib chart
    """

    volume = df["netImbalanceVolume"]
    price = df["systemSellPrice"]  # SSP = SBP

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(volume, price, alpha=0.5, s=20, c=np.where(volume >= 0, "green", "red"))
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_xlabel("Net Imbalance Volume (MWh)")
    ax.set_ylabel("System Price (£/MWh)")
    ax.set_title("NIV vs System Price")
    ax.grid(alpha=0.3)

    corr = volume.corr(price)
    ax.annotate(
        f"corr = {corr:.2f}", xy=(0.05, 0.95), xycoords="axes fraction", va="top"
    )
    fig.tight_layout()
    return fig
