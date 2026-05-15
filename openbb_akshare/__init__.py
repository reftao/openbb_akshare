"""openbb_akshare OpenBB Platform Provider."""

project_name = __name__

from openbb_core.provider.abstract.provider import Provider
from openbb_akshare.models.available_indices import AKShareAvailableIndicesFetcher
from openbb_akshare.models.balance_sheet import AKShareBalanceSheetFetcher
from openbb_akshare.models.cash_flow import AKShareCashFlowStatementFetcher
from openbb_akshare.models.china_dr007 import AKShareChinaDR007Fetcher
from openbb_akshare.models.china_northbound_flow import AKShareChinaNorthboundFlowFetcher
from openbb_akshare.models.china_pmi import AKShareChinaPMIFetcher
from openbb_akshare.models.china_social_financing import (
    AKShareChinaSocialFinancingFetcher,
)
from openbb_akshare.models.company_news import AKShareCompanyNewsFetcher
from openbb_akshare.models.economy_consumer_price_index import (
    AKShareConsumerPriceIndexFetcher,
)
from openbb_akshare.models.currency_historical import AKShareCurrencyHistoricalFetcher
from openbb_akshare.models.currency_snapshots import AKShareCurrencySnapshotsFetcher
from openbb_akshare.models.economy_money_measures import AKShareMoneyMeasuresFetcher
from openbb_akshare.models.equity_quote import AKShareEquityQuoteFetcher
from openbb_akshare.models.equity_historical import AKShareEquityHistoricalFetcher
from openbb_akshare.models.equity_ownership import AKShareEquityOwnershipFetcher
from openbb_akshare.models.equity_profile import AKShareEquityProfileFetcher
from openbb_akshare.models.equity_screener import AKShareEquityScreenerFetcher
from openbb_akshare.models.equity_search import AKShareEquitySearchFetcher
from openbb_akshare.models.historical_dividends import AKShareHistoricalDividendsFetcher
from openbb_akshare.models.income_statement import AKShareIncomeStatementFetcher
from openbb_akshare.models.key_metrics import AKShareKeyMetricsFetcher
from openbb_akshare.models.price_performance import AKSharePricePerformanceFetcher
from openbb_akshare.models.business_analysis import AkshareBusinessAnalysisFetcher
from openbb_akshare.models.etf_holdings import AkshareEtfHoldingsFetcher
from openbb_akshare.models.etf_search import AKShareEtfSearchFetcher
from openbb_akshare.models.fund_holdings import AkshareFundHoldingsFetcher

# mypy: disable-error-code="list-item"

provider = Provider(
    name="akshare",
    description="Data provider for openbb-akshare.",
    website="https://akshare.akfamily.xyz/",
    # Here, we list out the fetchers showing what our provider can get.
    # The dictionary key is the fetcher's name, used in the `router.py`.
    fetcher_dict={
        "AvailableIndices": AKShareAvailableIndicesFetcher,
        "BalanceSheet": AKShareBalanceSheetFetcher,
        "CashFlowStatement": AKShareCashFlowStatementFetcher,
        "ChinaDR007": AKShareChinaDR007Fetcher,
        "ChinaNorthboundFlow": AKShareChinaNorthboundFlowFetcher,
        "ChinaPMI": AKShareChinaPMIFetcher,
        "ChinaSocialFinancing": AKShareChinaSocialFinancingFetcher,
        "CompanyNews": AKShareCompanyNewsFetcher,
        "ConsumerPriceIndex": AKShareConsumerPriceIndexFetcher,
        "CurrencyHistorical": AKShareCurrencyHistoricalFetcher,
        "CurrencySnapshots": AKShareCurrencySnapshotsFetcher,
        "MoneyMeasures": AKShareMoneyMeasuresFetcher,
        "EquityQuote": AKShareEquityQuoteFetcher,
        "EquityHistorical": AKShareEquityHistoricalFetcher,
        "EquityOwnership": AKShareEquityOwnershipFetcher,
        "EquityInfo": AKShareEquityProfileFetcher,
        "EquityScreener": AKShareEquityScreenerFetcher,
        "EquitySearch": AKShareEquitySearchFetcher,
        "HistoricalDividends": AKShareHistoricalDividendsFetcher,
        "IncomeStatement": AKShareIncomeStatementFetcher,
        "KeyMetrics": AKShareKeyMetricsFetcher,
        "PricePerformance": AKSharePricePerformanceFetcher,
        "BusinessAnalysis": AkshareBusinessAnalysisFetcher,
        "EtfHoldings": AkshareEtfHoldingsFetcher,
        "EtfSearch": AKShareEtfSearchFetcher,
        "FundHoldings": AkshareFundHoldingsFetcher,
    }
)
