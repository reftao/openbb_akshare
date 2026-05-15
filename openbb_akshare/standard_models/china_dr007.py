"""China DR007 Standard Model."""

from datetime import date as dateType
from typing import Literal, Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from pydantic import Field


class ChinaDR007QueryParams(QueryParams):
    """China DR007 Query."""

    start_date: Optional[dateType] = Field(
        default=None,
        description="Start date of the data, in YYYY-MM-DD format.",
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description="End date of the data, in YYYY-MM-DD format.",
    )
    maturity: Literal["O/N", "1W", "2W", "1M", "3M", "6M", "9M", "1Y"] = Field(
        default="1W",
        description="Shibor maturity.",
    )


class ChinaDR007Data(Data):
    """China DR007 Data."""

    date: dateType = Field(description="Observation date.")
    rate: float = Field(description="Interest rate, in percent.")
    maturity: str = Field(description="Shibor maturity.")
    change: Optional[float] = Field(
        default=None,
        description="Change from the previous observation.",
    )
