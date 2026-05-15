"""Test cases for China macro models."""

from datetime import date

from openbb_akshare.models.china_dr007 import AKShareChinaDR007Fetcher
from openbb_akshare.models.china_northbound_flow import AKShareChinaNorthboundFlowFetcher
from openbb_akshare.models.china_pmi import AKShareChinaPMIFetcher
from openbb_akshare.models.china_social_financing import (
    AKShareChinaSocialFinancingFetcher,
)


def test_china_dr007_transform_data():
    """Test DR007 data transformation."""
    fetcher = AKShareChinaDR007Fetcher()
    query = fetcher.transform_query({"start_date": "2025-01-02"})
    data = [
        {"报告日": "2025-01-01", "利率": 1.7, "涨跌": -0.1},
        {"报告日": "2025-01-02", "利率": 1.8, "涨跌": 0.1},
    ]

    result = fetcher.transform_data(query, data)

    assert len(result) == 1
    assert result[0].date == date(2025, 1, 2)
    assert result[0].rate == 1.8
    assert result[0].maturity == "1W"
    assert result[0].change == 0.1


def test_china_social_financing_transform_data():
    """Test social financing data transformation."""
    fetcher = AKShareChinaSocialFinancingFetcher()
    query = fetcher.transform_query({"start_date": "2025-02-01"})
    data = [
        {"月份": "2025年01月", "社会融资规模增量": 1000, "其中-人民币贷款": 500},
        {
            "月份": "2025年02月",
            "社会融资规模增量": 2000,
            "其中-人民币贷款": 800,
            "其中-委托贷款外币贷款": 100,
            "其中-委托贷款": 50,
            "其中-信托贷款": 40,
            "其中-未贴现银行承兑汇票": 30,
            "其中-企业债券": 20,
            "其中-非金融企业境内股票融资": 10,
        },
    ]

    result = fetcher.transform_data(query, data)

    assert len(result) == 1
    assert result[0].date == date(2025, 2, 1)
    assert result[0].total_social_financing == 200
    assert result[0].rmb_loans == 80
    assert result[0].corporate_bonds == 2


def test_china_pmi_transform_data():
    """Test PMI data transformation."""
    fetcher = AKShareChinaPMIFetcher()
    query = fetcher.transform_query({})
    data = [
        {
            "月份": "2025-02-01",
            "制造业-指数": 50.2,
            "制造业-同比增长": 0.3,
            "非制造业-指数": 51.0,
            "非制造业-同比增长": 0.4,
        }
    ]

    result = fetcher.transform_data(query, data)

    assert len(result) == 1
    assert result[0].date == date(2025, 2, 1)
    assert result[0].manufacturing_pmi == 50.2
    assert result[0].non_manufacturing_pmi == 51.0


def test_china_northbound_flow_transform_data():
    """Test northbound flow data transformation."""
    fetcher = AKShareChinaNorthboundFlowFetcher()
    query = fetcher.transform_query({"channel": "northbound"})
    data = [
        {
            "日期": "2025-02-05",
            "当日成交净买额": 12.3,
            "买入成交额": 100.1,
            "卖出成交额": 87.8,
            "历史累计净买额": 5000.0,
            "当日资金流入": 20.0,
            "当日余额": 1000.0,
            "持股市值": 32000.0,
            "领涨股": "测试股份",
            "领涨股-代码": "600000",
            "领涨股-涨跌幅": 3.2,
            "沪深300": 4100.5,
            "沪深300-涨跌幅": 0.8,
        }
    ]

    result = fetcher.transform_data(query, data)

    assert len(result) == 1
    assert result[0].date == date(2025, 2, 5)
    assert result[0].channel == "northbound"
    assert result[0].net_buy_amount == 12.3
    assert result[0].leading_stock == "测试股份"
    assert result[0].index_close == 4100.5
