import logging

import pytest


@pytest.fixture()
def sensor():
    return {"sensor_id": 7684, "sensor_name": "True Heading"}


@pytest.fixture()
def sensor1():
    return {"sensor_id": 4182, "sensor_name": "Seafloor Pressure"}


@pytest.fixture()
def sensor2():
    return {"sensor_id": 7712, "sensor_name": "Uncompensated Seafloor Pressure"}


@pytest.fixture()
def device():
    return {
        "device_code": "BPR-Folger-59",
    }


def _assert_no_logs(caplog, log_level: int):
    # Sometimes sensor does not have real time data when using duration format,
    # which will generate a warning log.
    for record in caplog.records:
        assert (
            record.levelno < log_level
        ), f"There should be no {logging.getLevelName(log_level)} and above logs"


def _assert_logs(caplog, log_level: int):
    has_logs = False
    for record in caplog.records:
        if record.levelno == log_level:
            has_logs = True
    assert (
        has_logs
    ), f"There should be at least one {logging.getLevelName(log_level)} log"


# Time series widget tests


def test_time_series_iso_date_format(caplog, client, sensor1):
    client.widget.time_series(
        sensor1, "2010-02-21T00:00:00.000Z", "2010-02-23T00:00:00.000Z"
    )
    _assert_no_logs(caplog, logging.WARNING)


def test_time_series_iso_date_forma_no_data(caplog, client, sensor1):
    client.widget.time_series(
        sensor1, "2005-08-01T00:00:00.000Z", "2005-08-03T00:00:00.000Z"
    )
    _assert_logs(caplog, logging.WARNING)


def test_time_series_duration_date_format(caplog, client, sensor1):
    client.widget.time_series(sensor1, "-P2D")
    _assert_no_logs(caplog, logging.ERROR)


# Time series two sensors widget tests


def test_time_series_two_sensors_iso_date_format(caplog, client, sensor1, sensor2):
    client.widget.time_series_two_sensors(
        sensor1, sensor2, "2010-02-21T00:00:00.000Z", "2010-02-23T00:00:00.000Z"
    )
    _assert_no_logs(caplog, logging.WARNING)


def test_time_series_two_sensors_iso_date_format_no_data(
    caplog, client, sensor1, sensor2
):
    client.widget.time_series_two_sensors(
        sensor1, sensor2, "2005-08-01T00:00:00.000Z", "2005-08-03T00:00:00.000Z"
    )
    _assert_logs(caplog, logging.WARNING)


def test_time_series_two_sensors_duration_date_format(caplog, client, sensor1, sensor2):
    client.widget.time_series_two_sensors(sensor1, sensor2, date_from="-P2D")
    _assert_no_logs(caplog, logging.ERROR)


# Table archive files widget tests


def test_table_archive_files_iso_date_format(caplog, client, device):
    client.widget.table_archive_files(
        device, "2019-11-23T00:00:00.000Z", "2019-11-26T00:00:00.000Z"
    )
    _assert_no_logs(caplog, logging.WARNING)


def test_table_archive_files_iso_date_format_no_data(caplog, client, device):
    client.widget.table_archive_files(
        device, "2025-08-01T00:00:00.000Z", "2025-08-03T00:00:00.000Z"
    )
    _assert_logs(caplog, logging.WARNING)


def test_table_archive_files_duration_date_format(caplog, client, device):
    client.widget.table_archive_files(device, date_from="-P7D")
    _assert_no_logs(caplog, logging.ERROR)


