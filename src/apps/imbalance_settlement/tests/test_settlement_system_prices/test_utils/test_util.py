from datetime import date
from unittest.mock import patch

import pytest

from src.apps.imbalance_settlement.utils.exceptions import DateError
from src.apps.imbalance_settlement.utils.util import (
    bst_transition_dates,
    get_settlement_period,
    get_yesterday,
)

MODULE = "src.apps.imbalance_settlement.utils.util"


def test_get_yesterday_success():
    with patch(f"{MODULE}.date") as mock_date:
        mock_date.today.return_value = date(year=2026, month=7, day=11)

        result = get_yesterday()

    assert result == date(year=2026, month=7, day=10)


def test_get_yesterday_date_error_exception():
    with patch(f"{MODULE}.date") as mock_date:
        msg = "Incorrect date. Does not match yesterday's date."
        mock_date.today.side_effect = Exception(msg)

        with pytest.raises(DateError) as exc_info:
            get_yesterday()

        assert exc_info.type is DateError
        assert str(exc_info.value) == msg


def test_bst_transition_dates_success():
    year = 2026
    result = bst_transition_dates(year)
    expected_result = (
        date(year=2026, month=3, day=29),
        date(year=2026, month=10, day=25),
    )

    assert result == expected_result


class TestBSTSuccess:

    def test_get_settlement_period_bst_start_success(self):

        result = get_settlement_period(date(year=2026, month=3, day=29))

        assert result == 46

    def test_get_settlement_period_bst_end_success(self):

        result = get_settlement_period(date(year=2026, month=10, day=25))

        assert result == 50

    def test_get_settlement_period_normal_day_success(self):

        result = get_settlement_period(date(year=2026, month=1, day=1))

        assert result == 48
