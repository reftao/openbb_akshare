"""China Northbound Flow Standard Model."""

from datetime import date as dateType
from typing import Literal, Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from pydantic import Field


class ChinaNorthboundFlowQueryParams(QueryParams):
    """China Northbound Flow Query."""

    start_date: Optional[dateType] = Field(
        default=None,
        description="Start date of the data, in YYYY-MM-DD format.",
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description="End date of the data, in YYYY-MM-DD format.",
    )
    channel: Literal["northbound", "sh_connect", "sz_connect"] = Field(
        default="northbound",
        description="Northbound channel to fetch.",
    )


class ChinaNorthboundFlowData(Data):
    """China Northbound Flow Data."""

    date: dateType = Field(description="Trading date.")
    channel: str = Field(description="Northbound channel.")
    net_buy_amount: Optional[float] = Field(
        default=None,
        description="Daily net buy amount.",
    )
    buy_amount: Optional[float] = Field(default=None, description="Daily buy amount.")
    sell_amount: Optional[float] = Field(default=None, description="Daily sell amount.")
    cumulative_net_buy_amount: Optional[float] = Field(
        default=None,
        description="Historical cumulative net buy amount.",
    )
    fund_inflow: Optional[float] = Field(default=None, description="Daily fund inflow.")
    quota_balance: Optional[float] = Field(default=None, description="Daily quota balance.")
    holding_market_cap: Optional[float] = Field(
        default=None,
        description="Holding market capitalization.",
    )
    leading_stock: Optional[str] = Field(default=None, description="Leading stock name.")
    leading_stock_code: Optional[str] = Field(default=None, description="Leading stock code.")
    leading_stock_change: Optional[float] = Field(
        default=None,
        description="Leading stock percent change.",
    )
    index_close: Optional[float] = Field(default=None, description="Related index close.")
    index_change: Optional[float] = Field(
        default=None,
        description="Related index percent change.",
    )
