from datetime import date, datetime
from pathlib import Path
from typing import Optional

from src.apps.imbalance_settlement.core.settlement_system_prices.time_series import (
    imbalance_time_series,
)
from src.apps.imbalance_settlement.core.settlement_system_prices.visualisation import (
    niv_vs_price_bar_line_plot,
    niv_vs_price_scatter_plot,
)
from src.apps.imbalance_settlement.utils.api import APIClient, api_client
from src.apps.imbalance_settlement.utils.util import get_yesterday
from src.apps.imbalance_settlement.utils.validate import validator


class ImbalanceApplication:
    """Runs the core imbalance processing workflow."""

    def run(self) -> None:
        """Workflow pipeline."""
        yesterday = get_yesterday()

        # Fetch API data
        payload = self.fetch_settlement_system_prices(yesterdays_date=yesterday)

        # Validate series
        df = validator.validate_payload(payload=payload, yesterdays_date=yesterday)

        # Add HH timeseries data
        time_series_df = imbalance_time_series.create_time_series_df(df=df)

        # Generate Metrics
        metrics = imbalance_time_series.calculate_imbalance_metrics(df=df)

        # Display results/ Visualise Data
        charts = [
            (
                "niv_vs_price_bar_line_plot",
                niv_vs_price_bar_line_plot(time_series_df, yesterday),
            ),
            ("niv_vs_price_scatter_plot", niv_vs_price_scatter_plot(time_series_df)),
        ]
        self.display_results(charts, metrics)

    def fetch_settlement_system_prices(
        self, yesterdays_date: Optional[date], fetch_format: str = "json"
    ) -> APIClient:
        """Fetch API data."""
        return api_client.get(
            endpoint=f"/balancing/settlement/system-prices/{yesterdays_date}",
            params={"format": fetch_format},
        )

    def display_results(self, charts: list, metrics: dict) -> None:
        """Display pipeline in csv file."""
        print(f"""
        Imbalance Cost Summary
        ----------------------
        Total Daily Imbalance Cost : £{metrics["total_daily_imbalance_cost"]:,.2f}
        Imbalance Unit Rate        : £{metrics['imbalance_unit_rate']:,.2f}/MWh
        """)
        # Save each image in a folder
        output_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "charts"
            / "settlement_system_prices"
        )
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for name, fig in charts:
            file_path = output_dir / f"{name}_{timestamp}.png"

            fig.savefig(file_path, dpi=300, bbox_inches="tight")

        print(f"Charts saved in: {output_dir.resolve()}")
