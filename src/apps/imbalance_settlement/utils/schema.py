from datetime import date, datetime
from typing import Annotated, Optional

from pydantic import BeforeValidator, Field, StrictBool, StrictFloat, StrictStr
from pydantic.dataclasses import dataclass


def reject_numeric_datetime(value):
    """This rejects int or float for datetime values"""
    if isinstance(value, (int, float)):
        raise ValueError("Unix timestamps are not allowed.")
    return value


@dataclass
class ImbalanceSettlementDataSchema:
    settlementDate: date
    settlementPeriod: Annotated[int, Field(strict=True, ge=1, le=50)]
    startTime: Annotated[datetime, BeforeValidator(reject_numeric_datetime)]
    createdDateTime: Annotated[datetime, BeforeValidator(reject_numeric_datetime)]
    systemSellPrice: StrictFloat
    systemBuyPrice: StrictFloat
    bsadDefaulted: StrictBool
    priceDerivationCode: Optional[StrictStr]
    reserveScarcityPrice: Optional[StrictFloat]
    netImbalanceVolume: StrictFloat
    sellPriceAdjustment: Optional[StrictFloat]
    buyPriceAdjustment: Optional[StrictFloat]
    replacementPrice: Optional[StrictFloat]
    replacementPriceReferenceVolume: Optional[StrictFloat]
    totalAcceptedOfferVolume: Optional[StrictFloat]
    totalAcceptedBidVolume: Optional[StrictFloat]
    totalAdjustmentSellVolume: Optional[StrictFloat]
    totalAdjustmentBuyVolume: Optional[StrictFloat]
    totalSystemTaggedAcceptedOfferVolume: Optional[StrictFloat]
    totalSystemTaggedAcceptedBidVolume: Optional[StrictFloat]
    totalSystemTaggedAdjustmentSellVolume: Optional[StrictFloat]
    totalSystemTaggedAdjustmentBuyVolume: Optional[StrictFloat]
