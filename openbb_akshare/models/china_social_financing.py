"""AKShare China Social Financing Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Optional

from openbb_akshare.standard_models.china_social_financing import (
    ChinaSocialFinancingData,
    ChinaSocialFinancingQueryParams,
)
from openbb_akshare.utils.ak_macro import in_date_range, parse_month, yi_yuan_to_billions
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.utils.errors import EmptyDataError


class AKShareChinaSocialFinancingQueryParams(ChinaSocialFinancingQueryParams):
    """AKShare China Social Financing Query."""


class AKShareChinaSocialFinancingData(ChinaSocialFinancingData):
    """AKShare China Social Financing Data."""


class AKShareChinaSocialFinancingFetcher(
    Fetcher[
        AKShareChinaSocialFinancingQueryParams,
        List[AKShareChinaSocialFinancingData],
    ]
):
    """Transform the query, extract and transform social financing data from AKShare."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareChinaSocialFinancingQueryParams:
        """Transform the query params."""
        return AKShareChinaSocialFinancingQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareChinaSocialFinancingQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        data = _fetch_social_financing()
        return data.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareChinaSocialFinancingQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareChinaSocialFinancingData]:
        """Return the transformed data."""
        results: List[AKShareChinaSocialFinancingData] = []

        for row in data:
            date = parse_month(row.get("月份"))
            if date is None or not in_date_range(date, query.start_date, query.end_date):
                continue
            results.append(
                AKShareChinaSocialFinancingData.model_validate(
                    {
                        "date": date,
                        "total_social_financing": yi_yuan_to_billions(
                            row.get("社会融资规模增量")
                        ),
                        "rmb_loans": yi_yuan_to_billions(row.get("其中-人民币贷款")),
                        "foreign_currency_loans": yi_yuan_to_billions(
                            row.get("其中-委托贷款外币贷款")
                        ),
                        "entrusted_loans": yi_yuan_to_billions(row.get("其中-委托贷款")),
                        "trust_loans": yi_yuan_to_billions(row.get("其中-信托贷款")),
                        "undiscounted_bank_acceptances": yi_yuan_to_billions(
                            row.get("其中-未贴现银行承兑汇票")
                        ),
                        "corporate_bonds": yi_yuan_to_billions(row.get("其中-企业债券")),
                        "non_financial_enterprise_equity": yi_yuan_to_billions(
                            row.get("其中-非金融企业境内股票融资")
                        ),
                    }
                )
            )

        if not results:
            raise EmptyDataError("No social financing data was returned.")

        results.sort(key=lambda item: item.date)
        return results


def _fetch_social_financing():
    """Fetch social financing data with HTTP fallback for flaky TLS handshakes."""
    import time

    import pandas as pd
    import requests
    from requests.adapters import HTTPAdapter
    from requests.exceptions import RequestException, SSLError

    try:
        from akshare.economic.macro_china import TLSAdapter
    except ImportError:
        TLSAdapter = HTTPAdapter

    urls = [
        "http://data.mofcom.gov.cn/datamofcom/front/gnmy/shrzgmQuery",
        "https://data.mofcom.gov.cn/datamofcom/front/gnmy/shrzgmQuery",
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }

    last_error: Exception | None = None
    for url in urls:
        session = requests.Session()
        if url.startswith("https://"):
            session.mount("https://", TLSAdapter())
        for _ in range(3):
            try:
                response = session.post(url, headers=headers, timeout=20)
                response.raise_for_status()
                data_json = response.json()
                return _social_financing_frame(data_json)
            except (RequestException, SSLError, ValueError) as error:
                last_error = error
                time.sleep(0.5)

    if last_error:
        raise last_error
    raise RuntimeError("Failed to fetch social financing data.")


def _social_financing_frame(data_json):
    """Return a normalized social financing DataFrame."""
    import pandas as pd

    temp_df = pd.DataFrame(data_json)
    temp_df.columns = [
        "月份",
        "其中-未贴现银行承兑汇票",
        "其中-委托贷款",
        "其中-委托贷款外币贷款",
        "其中-人民币贷款",
        "其中-企业债券",
        "社会融资规模增量",
        "其中-非金融企业境内股票融资",
        "其中-信托贷款",
    ]
    temp_df = temp_df[
        [
            "月份",
            "社会融资规模增量",
            "其中-人民币贷款",
            "其中-委托贷款外币贷款",
            "其中-委托贷款",
            "其中-信托贷款",
            "其中-未贴现银行承兑汇票",
            "其中-企业债券",
            "其中-非金融企业境内股票融资",
        ]
    ]
    for column in temp_df.columns:
        if column != "月份":
            temp_df[column] = pd.to_numeric(temp_df[column], errors="coerce")

    temp_df.sort_values(["月份"], inplace=True)
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df
