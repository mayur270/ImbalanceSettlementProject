from datetime import date, datetime

import pytest

from src.apps.imbalance_settlement.utils.api import APIClient


@pytest.fixture
def mock_api_client():
    return APIClient(
        base_url="https://api.example.com",
        headers={"Accepted": "application/json", "Content-Type": "application/json"},
        retries=3,
        retry_delay=2,
    )


@pytest.fixture
def mock_valid_data():
    return {
        "settlementDate": date(2025, 1, 1),
        "settlementPeriod": 1,
        "startTime": datetime(2025, 1, 1, 0, 0),
        "createdDateTime": datetime(2025, 1, 1, 0, 0),
        "systemSellPrice": 100.5,
        "systemBuyPrice": 99.5,
        "bsadDefaulted": False,
        "priceDerivationCode": "ABC",
        "reserveScarcityPrice": None,
        "netImbalanceVolume": 200.0,
        "sellPriceAdjustment": None,
        "buyPriceAdjustment": None,
        "replacementPrice": None,
        "replacementPriceReferenceVolume": None,
        "totalAcceptedOfferVolume": None,
        "totalAcceptedBidVolume": None,
        "totalAdjustmentSellVolume": None,
        "totalAdjustmentBuyVolume": None,
        "totalSystemTaggedAcceptedOfferVolume": None,
        "totalSystemTaggedAcceptedBidVolume": None,
        "totalSystemTaggedAdjustmentSellVolume": None,
        "totalSystemTaggedAdjustmentBuyVolume": None,
    }


@pytest.fixture
def missing_settlement_period_data(mock_valid_data):
    return {
        "data": [
            {
                **mock_valid_data,
                "settlementPeriod": 1,
            },
            {
                **mock_valid_data,
                "settlementPeriod": 3,
            },
            {
                **mock_valid_data,
                "settlementPeriod": 5,
            },
        ]
    }


@pytest.fixture
def duplicate_settlement_period_data(settlement_period_data, mock_valid_data):
    settlement_period_data["data"].append(
        {
            **mock_valid_data,
            "settlementPeriod": 10,
        }
    )
    return settlement_period_data


@pytest.fixture
def settlement_period_data(mock_valid_data):
    return {
        "data": [
            {
                **mock_valid_data,
                "settlementPeriod": period,
            }
            for period in range(1, 49)
        ]
    }
