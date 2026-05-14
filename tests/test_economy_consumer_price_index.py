"""Test cases for Economy Consumer Price Index model."""

from datetime import date

from openbb_akshare.models.economy_consumer_price_index import (
    AKShareConsumerPriceIndexFetcher,
)


def test_cpi_transform_query():
    """Test CPI query transformation."""
    fetcher = AKShareConsumerPriceIndexFetcher()
    query = fetcher.transform_query(
        {
            "country": "china",
            "transform": "mom",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
        }
    )

    assert query.country == "china"
    assert query.transform == "period"
    assert query.frequency == "monthly"
    assert query.start_date == date(2025, 1, 1)
    assert query.end_date == date(2025, 12, 31)


def test_cpi_transform_data_yoy():
    """Test CPI YoY data transformation."""
    fetcher = AKShareConsumerPriceIndexFetcher()
    query = fetcher.transform_query({"start_date": "2025-02-01"})
    sample_data = [
        {
            "月份": "2025年01月份",
            "全国-当月": 100.1,
            "全国-同比增长": 0.5,
            "全国-环比增长": -0.1,
        },
        {
            "月份": "2025年02月份",
            "全国-当月": 100.8,
            "全国-同比增长": 0.8,
            "全国-环比增长": 0.2,
        },
    ]

    result = fetcher.transform_data(query, sample_data)

    assert len(result) == 1
    assert result[0].date == date(2025, 2, 1)
    assert result[0].country == "china"
    assert result[0].value == 0.8


def test_cpi_transform_data_index():
    """Test CPI index data transformation."""
    fetcher = AKShareConsumerPriceIndexFetcher()
    query = fetcher.transform_query({"transform": "index"})
    sample_data = [
        {
            "月份": "2025-02-01",
            "全国-当月": 100.8,
            "全国-同比增长": 0.8,
            "全国-环比增长": 0.2,
        },
    ]

    result = fetcher.transform_data(query, sample_data)

    assert len(result) == 1
    assert result[0].date == date(2025, 2, 1)
    assert result[0].value == 100.8
