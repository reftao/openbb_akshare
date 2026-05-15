"""AKShare China DR007 Model."""

# pylint: disable=unused-argument

import time
from typing import Any, Dict, List, Optional

from openbb_akshare.standard_models.china_dr007 import (
    ChinaDR007Data,
    ChinaDR007QueryParams,
)
from openbb_akshare.utils.ak_macro import in_date_range, parse_date, to_float
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.utils.errors import EmptyDataError


MATURITY_MAP = {
    "O/N": "隔夜",
    "1W": "1周",
    "2W": "2周",
    "1M": "1月",
    "3M": "3月",
    "6M": "6月",
    "9M": "9月",
    "1Y": "1年",
}


class AKShareChinaDR007QueryParams(ChinaDR007QueryParams):
    """AKShare China DR007 Query."""


class AKShareChinaDR007Data(ChinaDR007Data):
    """AKShare China DR007 Data."""


class AKShareChinaDR007Fetcher(
    Fetcher[
        AKShareChinaDR007QueryParams,
        List[AKShareChinaDR007Data],
    ]
):
    """Transform the query, extract and transform DR007 data from AKShare."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareChinaDR007QueryParams:
        """Transform the query params."""
        return AKShareChinaDR007QueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareChinaDR007QueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        return _fetch_shibor(
            indicator=MATURITY_MAP[query.maturity],
            start_date=query.start_date,
            end_date=query.end_date,
        )

    @staticmethod
    def transform_data(
        query: AKShareChinaDR007QueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareChinaDR007Data]:
        """Return the transformed data."""
        results: List[AKShareChinaDR007Data] = []

        for row in data:
            date = parse_date(row.get("报告日"))
            rate = to_float(row.get("利率"))
            if date is None or rate is None:
                continue
            if not in_date_range(date, query.start_date, query.end_date):
                continue
            results.append(
                AKShareChinaDR007Data.model_validate(
                    {
                        "date": date,
                        "rate": rate,
                        "maturity": query.maturity,
                        "change": to_float(row.get("涨跌")),
                    }
                )
            )

        if not results:
            raise EmptyDataError("No DR007 data was returned.")

        results.sort(key=lambda item: item.date)
        return results


def _fetch_shibor(
    indicator: str,
    start_date: Any = None,
    end_date: Any = None,
) -> List[Dict]:
    """Fetch Shibor data directly from Eastmoney with bounded pagination."""
    import pandas as pd

    indicator_map = {
        "隔夜": "001",
        "1周": "101",
        "2周": "102",
        "3周": "103",
        "1月": "201",
        "2月": "202",
        "3月": "203",
        "4月": "204",
        "5月": "205",
        "6月": "206",
        "7月": "207",
        "8月": "208",
        "9月": "209",
        "10月": "210",
        "11月": "211",
        "1年": "301",
    }
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    page_size = 500
    params = {
        "reportName": "RPT_IMP_INTRESTRATEN",
        "columns": "REPORT_DATE,REPORT_PERIOD,IR_RATE,CHANGE_RATE,INDICATOR_ID,"
        "LATEST_RECORD,MARKET,MARKET_CODE,CURRENCY,CURRENCY_CODE",
        "quoteColumns": "",
        "filter": f'(MARKET_CODE="001")(CURRENCY_CODE="CNY")'
        f'(INDICATOR_ID="{indicator_map[indicator]}")',
        "pageNumber": "1",
        "pageSize": str(page_size),
        "sortTypes": "-1",
        "sortColumns": "REPORT_DATE",
        "source": "WEB",
        "client": "WEB",
        "p": "1",
        "pageNo": "1",
        "pageNum": "1",
    }

    rows: List[Dict] = []
    total_pages = 1
    page = 1
    while page <= total_pages:
        params.update(
            {
                "pageNumber": str(page),
                "p": str(page),
                "pageNo": str(page),
                "pageNum": str(page),
            }
        )
        data_json = _get_json_with_retry(url, params)
        result = data_json.get("result") or {}
        total_pages = int(result.get("pages") or 1)
        page_rows = result.get("data") or []
        if not page_rows:
            break

        frame = pd.DataFrame(page_rows)
        frame = frame.rename(
            columns={
                "REPORT_DATE": "报告日",
                "IR_RATE": "利率",
                "CHANGE_RATE": "涨跌",
            }
        )
        frame = frame[["报告日", "利率", "涨跌"]]
        frame["报告日"] = pd.to_datetime(frame["报告日"], errors="coerce").dt.date
        frame["利率"] = pd.to_numeric(frame["利率"], errors="coerce")
        frame["涨跌"] = pd.to_numeric(frame["涨跌"], errors="coerce")
        rows.extend(frame.to_dict(orient="records"))

        oldest_date = parse_date(frame["报告日"].iloc[-1])
        boundary_date = start_date or end_date
        if boundary_date is None:
            break
        if oldest_date and oldest_date < boundary_date:
            break

        page += 1
        time.sleep(0.1)

    return rows


def _get_json_with_retry(url: str, params: Dict[str, str]) -> Dict:
    """Get JSON with a small retry loop for intermittent chunked responses."""
    import requests
    from requests.exceptions import ChunkedEncodingError, RequestException

    last_error: Exception | None = None
    for _ in range(3):
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except (ChunkedEncodingError, RequestException) as error:
            last_error = error
            time.sleep(0.5)

    if last_error:
        raise last_error
    raise RuntimeError("Failed to fetch Shibor data.")
