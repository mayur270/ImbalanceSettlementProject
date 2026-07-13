from datetime import date, datetime, timedelta

from src.apps.imbalance_settlement.utils.exceptions import DateError


def get_yesterday() -> date:
    """Returns yesterday's date"""
    try:
        return date.today() - timedelta(days=1)
    except Exception as e:
        raise DateError("Incorrect date. Does not match yesterday's date.") from e


def bst_transition_dates(year: int):
    """
    Returns the British Summer Time start and end dates for a given year.

    BST start is last Sunday in March.
    BST end is last Sunday in October.
    """

    # Calculate last Sunday in March
    march_end = datetime(year, 4, 1) - timedelta(days=1)
    bst_start = march_end - timedelta(days=(march_end.weekday() + 1) % 7)

    # Calculate last Sunday in October
    october_end = datetime(year, 11, 1) - timedelta(days=1)
    bst_end = october_end - timedelta(days=(october_end.weekday() + 1) % 7)

    return bst_start.date(), bst_end.date()


def get_settlement_period(yesterdays_date: date) -> int:
    """Gets settlement period depending on BST for yesterday's date"""
    year = yesterdays_date.year
    british_summer_time_start, british_summer_time_end = bst_transition_dates(year)

    if yesterdays_date == british_summer_time_start:
        max_periods = 46
    elif yesterdays_date == british_summer_time_end:
        max_periods = 50
    else:
        max_periods = 48
    return max_periods
