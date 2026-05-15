"""China PMI Standard Model."""

from datetime import date as dateType
from typing import Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from pydantic import Field


class ChinaPMIQueryParams(QueryParams):
    """China PMI Query."""

    start_date: Optional[dateType] = Field(
        default=None,
        description="Start date of the data, in YYYY-MM-DD format.",
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description="End date of the data, in YYYY-MM-DD format.",
    )


class ChinaPMIData(Data):
    """China PMI Data."""

    date: dateType = Field(description="Observation month.")
    manufacturing_pmi: Optional[float] = Field(
        default=None,
        description="Manufacturing PMI index.",
    )
    manufacturing_yoy: Optional[float] = Field(
        default=None,
        description="Manufacturing PMI year-over-year change.",
    )
    non_manufacturing_pmi: Optional[float] = Field(
        default=None,
        description="Non-manufacturing PMI index.",
    )
    non_manufacturing_yoy: Optional[float] = Field(
        default=None,
        description="Non-manufacturing PMI year-over-year change.",
    )
