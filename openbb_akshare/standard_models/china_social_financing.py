"""China Social Financing Standard Model."""

from datetime import date as dateType
from typing import Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.query_params import QueryParams
from pydantic import Field


class ChinaSocialFinancingQueryParams(QueryParams):
    """China Social Financing Query."""

    start_date: Optional[dateType] = Field(
        default=None,
        description="Start date of the data, in YYYY-MM-DD format.",
    )
    end_date: Optional[dateType] = Field(
        default=None,
        description="End date of the data, in YYYY-MM-DD format.",
    )


class ChinaSocialFinancingData(Data):
    """China Social Financing Data."""

    date: dateType = Field(description="Observation month.")
    total_social_financing: Optional[float] = Field(
        default=None,
        description="Incremental aggregate financing to the real economy, in billion CNY.",
    )
    rmb_loans: Optional[float] = Field(default=None, description="RMB loans, in billion CNY.")
    foreign_currency_loans: Optional[float] = Field(
        default=None,
        description="Foreign currency loans, in billion CNY.",
    )
    entrusted_loans: Optional[float] = Field(
        default=None,
        description="Entrusted loans, in billion CNY.",
    )
    trust_loans: Optional[float] = Field(default=None, description="Trust loans, in billion CNY.")
    undiscounted_bank_acceptances: Optional[float] = Field(
        default=None,
        description="Undiscounted bankers' acceptances, in billion CNY.",
    )
    corporate_bonds: Optional[float] = Field(
        default=None,
        description="Corporate bonds, in billion CNY.",
    )
    non_financial_enterprise_equity: Optional[float] = Field(
        default=None,
        description="Domestic equity financing by non-financial enterprises, in billion CNY.",
    )
