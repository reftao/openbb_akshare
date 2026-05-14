"""AKShare Economy Consumer Price Index Model."""

# pylint: disable=unused-argument

from datetime import date as dateType
from typing import Any, Dict, List, Literal, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.consumer_price_index import (
    ConsumerPriceIndexData,
    ConsumerPriceIndexQueryParams,
)
from openbb_core.provider.utils.errors import EmptyDataError
from pydantic import Field, field_validator


class AKShareConsumerPriceIndexQueryParams(ConsumerPriceIndexQueryParams):
    """AKShare Consumer Price Index Query.

    Source: https://data.eastmoney.com/cjsj/cpi.html
    """

    __json_schema_extra__ = {
        "country": {"choices": ["china"]},
        "transform": {"choices": ["index", "yoy", "period"]},
        "frequency": {"choices": ["monthly"]},
    }

    country: Literal["china"] = Field(
        default="china",
        description="Country for the CPI data. Only China is supported.",
    )
    transform: Literal["index", "yoy", "period"] = Field(
        default="yoy",
        description="Transformation of the CPI data.",
    )
    frequency: Literal["monthly"] = Field(
        default="monthly",
        description="Frequency of the CPI data. Only monthly is supported.",
    )

    @field_validator("country", mode="before", check_fields=False)
    @classmethod
    def validate_country(cls, value: str) -> str:
        """Validate country."""
        if str(value).lower() != "china":
            raise ValueError("AKShare CPI only supports country='china'.")
        return "china"

    @field_validator("transform", mode="before", check_fields=False)
    @classmethod
    def validate_transform(cls, value: str) -> str:
        """Validate transform."""
        transform = str(value).lower()
        if transform == "mom":
            transform = "period"
        if transform not in {"index", "yoy", "period"}:
            raise ValueError("AKShare CPI transform must be one of: index, yoy, period.")
        return transform


class AKShareConsumerPriceIndexData(ConsumerPriceIndexData):
    """AKShare Consumer Price Index Data."""


class AKShareConsumerPriceIndexFetcher(
    Fetcher[
        AKShareConsumerPriceIndexQueryParams,
        List[AKShareConsumerPriceIndexData],
    ]
):
    """Transform the query, extract and transform the data from the AKShare endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareConsumerPriceIndexQueryParams:
        """Transform the query params."""
        return AKShareConsumerPriceIndexQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareConsumerPriceIndexQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        data = ak.macro_china_cpi()
        return data.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareConsumerPriceIndexQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareConsumerPriceIndexData]:
        """Return the transformed data."""
        value_column = {
            "index": "全国-当月",
            "yoy": "全国-同比增长",
            "period": "全国-环比增长",
        }[query.transform]

        results: List[AKShareConsumerPriceIndexData] = []
        for row in data:
            date = _parse_month(row.get("月份"))
            if date is None:
                continue

            if query.start_date and date < query.start_date:
                continue
            if query.end_date and date > query.end_date:
                continue

            value = _to_float(row.get(value_column))
            if value is None:
                continue

            results.append(
                AKShareConsumerPriceIndexData.model_validate(
                    {
                        "date": date,
                        "country": "china",
                        "value": value,
                    }
                )
            )

        if not results:
            raise EmptyDataError("No CPI data was returned.")

        results.sort(key=lambda item: item.date)
        return results


def _parse_month(value: Any) -> Optional[dateType]:
    """Parse AKShare month values to a month-start date."""
    if value is None:
        return None
    if isinstance(value, dateType):
        return dateType(value.year, value.month, 1)

    text = str(value).strip()
    if not text:
        return None

    import re
    from datetime import datetime

    match = re.search(r"(?P<year>\d{4})\D*(?P<month>\d{1,2})", text)
    if match:
        return dateType(int(match.group("year")), int(match.group("month")), 1)

    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            parsed = datetime.strptime(text, fmt).date()
            return dateType(parsed.year, parsed.month, 1)
        except ValueError:
            continue

    return None


def _to_float(value: Any) -> Optional[float]:
    """Convert values to float while preserving missing values."""
    if value is None:
        return None

    import pandas as pd

    if pd.isna(value):
        return None
    return float(value)
