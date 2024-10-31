"""Finance Capital Structure Standard Model."""

from datetime import date as dateType
from typing import Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)
from pydantic import Field


class FinanceCapitalStructureQueryParams(QueryParams):
    """Finance Capital Structure Query."""

    symbol: str = Field(description=QUERY_DESCRIPTIONS.get("symbol", ""))


class FinanceCapitalStructureData(Data):
    """Finance Capital Structure Data."""

    symbol: str = Field(
        description=DATA_DESCRIPTIONS.get("symbol", "The symbol of the company.")
    )
    timestamp: Optional[dateType] = Field(
        description=DATA_DESCRIPTIONS.get(
            "timestamp", "Reporting period publication time."
        )
    )
    period_ending: Optional[dateType] = Field(
        description="The end date of the reporting period."
    )