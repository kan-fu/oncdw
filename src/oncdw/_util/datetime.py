from datetime import datetime, timezone

import pandas as pd
from isodate import parse_duration


def _to_onc_format(dt: datetime) -> str:
    """
    Convert a timezone-aware datetime object to a standardized string format used by ONC web services.
    isoformat will return a string like 2019-11-23T00:00:00.000+00:00.
    The desired format for ONC web services is like 2019-11-23T00:00:00.000Z.

    Examples
    --------
    >>> from datetime import datetime, timezone
    >>> dt = datetime(2019, 11, 23, tzinfo=timezone.utc)
    >>> _to_onc_format(dt)
    '2019-11-23T00:00:00.000Z'
    """
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_datetime_parameters(date_from: str, date_to: str | None) -> tuple[str, str]:
    """
    Parse date_from and date_to parameters to a standardized format.

    This is only used in internal web services. OpenAPI supports duration format.

    Examples
    --------
    >>> date_from, date_to = "-P7D", "2019-11-23T00:00:00.000Z"
    >>> parse_datetime_parameters(date_from, date_to)
    ('2019-11-16T00:00:00.000Z', '2019-11-23T00:00:00.000Z')
    """
    if date_to is None:
        # If date_to is not provided, use current datetime for date_to
        date_to = datetime.now(timezone.utc)
        date_to_str = _to_onc_format(date_to)
    elif "P" in date_to:
        # If date_to is a duration, use current datetime + duration for date_to
        now = datetime.now(timezone.utc)
        duration_date_to = date_to
        date_to = now + parse_duration(duration_date_to)
        date_to_str = _to_onc_format(date_to)
    else:
        # If date_to is in standard format, just use it
        date_to_str = date_to
        date_to = datetime.fromisoformat(date_to.replace("Z", "+00:00"))

    if "P" in date_from:
        # If date_from is a duration, use date_to + duration for date_from
        duration_date_from = date_from
        date_from_str = _to_onc_format(date_to + parse_duration(duration_date_from))
    else:
        # If date_from is in standard format, just use it
        date_from_str = date_from

    return date_from_str, date_to_str


def now():
    return pd.Timestamp.now(timezone.utc).tz_localize(None)
