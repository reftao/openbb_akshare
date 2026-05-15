"""AKShare China Northbound Flow Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Optional

from openbb_akshare.standard_models.china_northbound_flow import (
    ChinaNorthboundFlowData,
    ChinaNorthboundFlowQueryParams,
)
from openbb_akshare.utils.ak_macro import in_date_range, parse_date, to_float
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.utils.errors import EmptyDataError


CHANNEL_MAP = {
    "northbound": "北向资金",
    "sh_connect": "沪股通",
    "sz_connect": "深股通",
}


class AKShareChinaNorthboundFlowQueryParams(ChinaNorthboundFlowQueryParams):
    """AKShare China Northbound Flow Query."""


class AKShareChinaNorthboundFlowData(ChinaNorthboundFlowData):
    """AKShare China Northbound Flow Data."""


class AKShareChinaNorthboundFlowFetcher(
    Fetcher[
        AKShareChinaNorthboundFlowQueryParams,
        List[AKShareChinaNorthboundFlowData],
    ]
):
    """Transform the query, extract and transform northbound flow data from AKShare."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareChinaNorthboundFlowQueryParams:
        """Transform the query params."""
        return AKShareChinaNorthboundFlowQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareChinaNorthboundFlowQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the AKShare endpoint."""
        import akshare as ak

        data = ak.stock_hsgt_hist_em(symbol=CHANNEL_MAP[query.channel])
        return data.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: AKShareChinaNorthboundFlowQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareChinaNorthboundFlowData]:
        """Return the transformed data."""
        results: List[AKShareChinaNorthboundFlowData] = []
        index_name = _index_name(query.channel)

        for row in data:
            date = parse_date(row.get("日期"))
            if date is None or not in_date_range(date, query.start_date, query.end_date):
                continue
            results.append(
                AKShareChinaNorthboundFlowData.model_validate(
                    {
                        "date": date,
                        "channel": query.channel,
                        "net_buy_amount": to_float(row.get("当日成交净买额")),
                        "buy_amount": to_float(row.get("买入成交额")),
                        "sell_amount": to_float(row.get("卖出成交额")),
                        "cumulative_net_buy_amount": to_float(row.get("历史累计净买额")),
                        "fund_inflow": to_float(row.get("当日资金流入")),
                        "quota_balance": to_float(row.get("当日余额")),
                        "holding_market_cap": to_float(row.get("持股市值")),
                        "leading_stock": row.get("领涨股"),
                        "leading_stock_code": row.get("领涨股-代码"),
                        "leading_stock_change": to_float(row.get("领涨股-涨跌幅")),
                        "index_close": to_float(row.get(index_name)),
                        "index_change": to_float(row.get(f"{index_name}-涨跌幅")),
                    }
                )
            )

        if not results:
            raise EmptyDataError("No northbound flow data was returned.")

        results.sort(key=lambda item: item.date)
        return results


def _index_name(channel: str) -> str:
    """Return AKShare's related index column name for a channel."""
    if channel == "sh_connect":
        return "上证指数"
    if channel == "sz_connect":
        return "深证指数"
    return "沪深300"
