from datetime import datetime, timezone

import pandas as pd
from isodate import parse_duration


def _standardize_datetime_format(dt: datetime) -> str:
    """
    Convert a datetime object to a standardized string format.
    isoformat will return a string like 2019-11-23T00:00:00.000+00:00.
    The desired format for ONC web services is like 2019-11-23T00:00:00.000Z.
    """
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_datetime_parameters(date_from: str, date_to: str | None) -> tuple[str, str]:
    """
    Parse date_from and date_to parameters to a standardized format.

    This is only used in internal web services. OpenAPI supports duration format.
    """
    if date_to is None:
        date_to = datetime.now(timezone.utc)
        date_to_str = _standardize_datetime_format(date_to)
    else:
        date_to_str = date_to
        date_to = datetime.fromisoformat(date_to.replace("Z", "+00:00"))

    if "P" in date_from:
        duration = date_from
        date_from_str = _standardize_datetime_format(date_to + parse_duration(duration))
    else:
        date_from_str = date_from

    return date_from_str, date_to_str


def now():
    return pd.Timestamp.now(timezone.utc).tz_localize(None)
