"""AKShare Economy Money Measures Model."""

# pylint: disable=unused-argument

from datetime import date as dateType
from typing import Any, Dict, List, Literal, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.money_measures import (
    MoneyMeasuresData,
    MoneyMeasuresQueryParams,
)
from openbb_core.provider.utils.errors import EmptyDataError
from pydantic import Field


class AKShareMoneyMeasuresQueryParams(MoneyMeasuresQueryParams):
    """AKShare Money Measures Query.

    Source: https://data.eastmoney.com/cjsj/hbgyl.html
    """

    country: Literal["china"] = Field(
        default="china",
        description="Country for the money supply data. Only China is supported.",
    )


class AKShareMoneyMeasuresData(MoneyMeasuresData):
    """AKShare Money Measures Data."""


class AKShareMoneyMeasuresFetcher(
    Fetcher[
        AKShareMoneyMeasuresQueryParams,
        List[AKShareMoneyMeasuresData],
    ]
):
    """Transform the query, extract and transform the data from the AKShare endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareMoneyMeasuresQueryParams:
        """Transform the query params."""
        return AKShareMoneyMeasuresQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareMoneyMeasuresQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        data = ak.macro_china_money_supply()
        return data.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareMoneyMeasuresQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareMoneyMeasuresData]:
        """Return the transformed data."""
        results: List[AKShareMoneyMeasuresData] = []

        for row in data:
            month = _parse_month(row.get("月份"))
            if month is None:
                continue

            if query.start_date and month < query.start_date:
                continue
            if query.end_date and month > query.end_date:
                continue

            item = {
                "month": month,
                "m1": _yi_yuan_to_billions(row.get("货币(M1)-数量(亿元)")),
                "m2": _yi_yuan_to_billions(row.get("货币和准货币(M2)-数量(亿元)")),
                "currency": _yi_yuan_to_billions(row.get("流通中的现金(M0)-数量(亿元)")),
            }
            if item["m1"] is None or item["m2"] is None:
                continue
            results.append(AKShareMoneyMeasuresData.model_validate(item))

        if not results:
            raise EmptyDataError("No money measures data was returned.")

        results.sort(key=lambda item: item.month)
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


def _yi_yuan_to_billions(value: Any) -> Optional[float]:
    """Convert 100 million yuan units to billion yuan units."""
    if value is None:
        return None

    import pandas as pd

    if pd.isna(value):
        return None
    return float(value) * 0.1
