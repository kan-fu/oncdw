from datetime import datetime, timedelta

from .data_preview_options import DataPreviewOption
from .device import Device
from .sensor import Sensor
from .util import get_archive_file_download_link, natural_size

__all__ = [
    "Device",
    "DataPreviewOption",
    "Sensor",
    "natural_size",
    "get_archive_file_download_link",
]


def get_date_from_last_days(last_days: int, date_to: datetime) -> tuple[str, str]:
    """
    Return dateFrom and dateTo with the format accepted by Oceans 3.0 web service.

    The standard format for a datetime is like 2019-11-23T00:00:00.000Z.

    Parameters
    ----------
    last_days : int
        The number of days between dateFrom and dateTo.
    date_to : datetime
        dateTo used in the web service.

    Returns
    -------
    tuple[str, str]
        dateFrom and dateTo in the desired format

    """  # noqa: E501
    date_from = date_to - timedelta(days=last_days)
    return (
        # Calling isoformat on timezone aware objects will return something
        # like 2019-11-23T00:00:00.000+00:00
        date_from.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        date_to.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    )
