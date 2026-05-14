"""Test cases for Economy Money Measures model."""

from datetime import date

from openbb_akshare.models.economy_money_measures import AKShareMoneyMeasuresFetcher


def test_money_measures_transform_query():
    """Test money measures query transformation."""
    fetcher = AKShareMoneyMeasuresFetcher()
    query = fetcher.transform_query(
        {
            "country": "china",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
        }
    )

    assert query.country == "china"
    assert query.start_date == date(2025, 1, 1)
    assert query.end_date == date(2025, 12, 31)


def test_money_measures_transform_data():
    """Test money measures data transformation."""
    fetcher = AKShareMoneyMeasuresFetcher()
    query = fetcher.transform_query(
        {
            "start_date": "2025-02-01",
            "end_date": "2025-12-31",
        }
    )
    sample_data = [
        {
            "月份": "2025年01月份",
            "货币和准货币(M2)-数量(亿元)": 1000,
            "货币(M1)-数量(亿元)": 500,
            "流通中的现金(M0)-数量(亿元)": 100,
        },
        {
            "月份": "2025年02月份",
            "货币和准货币(M2)-数量(亿元)": 2000,
            "货币(M1)-数量(亿元)": 800,
            "流通中的现金(M0)-数量(亿元)": 200,
        },
    ]

    result = fetcher.transform_data(query, sample_data)

    assert len(result) == 1
    assert result[0].month == date(2025, 2, 1)
    assert result[0].m2 == 200
    assert result[0].m1 == 80
    assert result[0].currency == 20
