"""Utilities for AKShare macro models."""

from datetime import date as dateType
from datetime import datetime
from typing import Any, Optional


def parse_month(value: Any) -> Optional[dateType]:
    """Parse AKShare month-like values to a month-start date."""
    parsed = parse_date(value)
    if parsed is None:
        return None
    return dateType(parsed.year, parsed.month, 1)


def parse_date(value: Any) -> Optional[dateType]:
    """Parse AKShare date-like values to a date."""
    if value is None:
        return None
    if isinstance(value, dateType):
        return value

    text = str(value).strip()
    if not text:
        return None

    import re

    match = re.search(r"(?P<year>\d{4})\D*(?P<month>\d{1,2})(?:\D*(?P<day>\d{1,2}))?", text)
    if match:
        return dateType(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day") or 1),
        )

    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    return None


def to_float(value: Any) -> Optional[float]:
    """Convert a value to float while preserving missing values."""
    if value is None:
        return None

    import pandas as pd

    if pd.isna(value):
        return None
    return float(value)


def yi_yuan_to_billions(value: Any) -> Optional[float]:
    """Convert 100 million yuan units to billion yuan units."""
    number = to_float(value)
    return None if number is None else number * 0.1


def in_date_range(
    value: dateType,
    start_date: Optional[dateType],
    end_date: Optional[dateType],
) -> bool:
    """Return whether a date is within the optional inclusive range."""
    if start_date and value < start_date:
        return False
    if end_date and value > end_date:
        return False
    return True
