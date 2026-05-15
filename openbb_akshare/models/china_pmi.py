"""AKShare China PMI Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Optional

from openbb_akshare.standard_models.china_pmi import ChinaPMIData, ChinaPMIQueryParams
from openbb_akshare.utils.ak_macro import in_date_range, parse_month, to_float
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.utils.errors import EmptyDataError


class AKShareChinaPMIQueryParams(ChinaPMIQueryParams):
    """AKShare China PMI Query."""


class AKShareChinaPMIData(ChinaPMIData):
    """AKShare China PMI Data."""


class AKShareChinaPMIFetcher(
    Fetcher[
        AKShareChinaPMIQueryParams,
        List[AKShareChinaPMIData],
    ]
):
    """Transform the query, extract and transform PMI data from AKShare."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareChinaPMIQueryParams:
        """Transform the query params."""
        return AKShareChinaPMIQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareChinaPMIQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        data = ak.macro_china_pmi()
        return data.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareChinaPMIQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareChinaPMIData]:
        """Return the transformed data."""
        results: List[AKShareChinaPMIData] = []

        for row in data:
            date = parse_month(row.get("月份"))
            if date is None or not in_date_range(date, query.start_date, query.end_date):
                continue
            results.append(
                AKShareChinaPMIData.model_validate(
                    {
                        "date": date,
                        "manufacturing_pmi": to_float(row.get("制造业-指数")),
                        "manufacturing_yoy": to_float(row.get("制造业-同比增长")),
                        "non_manufacturing_pmi": to_float(row.get("非制造业-指数")),
                        "non_manufacturing_yoy": to_float(row.get("非制造业-同比增长")),
                    }
                )
            )

        if not results:
            raise EmptyDataError("No PMI data was returned.")

        results.sort(key=lambda item: item.date)
        return results
