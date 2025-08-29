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


# Data preview widget tests


def test_data_preview_with_sensor(caplog, client):
    device = {"device_category_id": 20, "search_tree_node_id": 172}
    data_preview_options = {"data_product_format_id": 149, "sensor_code_id": 611}
    client.widget.data_preview(device, data_preview_options)
    _assert_no_logs(caplog, logging.WARNING)


def test_data_preview_with_sensor_no_data(caplog, client):
    device = {"device_category_id": 201, "search_tree_node_id": 172}
    data_preview_options = {"data_product_format_id": 149, "sensor_code_id": 611}
    client.widget.data_preview(device, data_preview_options)
    _assert_logs(caplog, logging.WARNING)


def test_data_preview_without_sensor(caplog, client):
    device = {"device_category_id": 65, "search_tree_node_id": 429}
    data_preview_options = {"data_product_format_id": 178}
    client.widget.data_preview(device, data_preview_options)
    _assert_no_logs(caplog, logging.WARNING)


def test_data_preview_without_sensor_no_data(caplog, client):
    device = {"device_category_id": 650, "search_tree_node_id": 429}
    data_preview_options = {"data_product_format_id": 178}
    client.widget.data_preview(device, data_preview_options)
    _assert_logs(caplog, logging.WARNING)


# Heat map widget tests


def test_heatmap_archive_files_iso_date_format(caplog, client, device):
    client.widget.heatmap_archive_files(
        device, "2019-11-23T00:00:00.000Z", "2019-11-26T00:00:00.000Z"
    )
    _assert_no_logs(caplog, logging.WARNING)


def test_heatmap_archive_files_iso_date_format_no_data(caplog, client, device):
    client.widget.heatmap_archive_files(
        device, "2025-08-01T00:00:00.000Z", "2025-08-03T00:00:00.000Z"
    )
    _assert_logs(caplog, logging.WARNING)


def test_heatmap_archive_files_duration_date_format(caplog, client, device):
    client.widget.heatmap_archive_files(device, date_from="-P7D")
    _assert_no_logs(caplog, logging.ERROR)


# Scatter plot widget tests


@pytest.fixture()
def device2():
    return {"location_code": "BACAX", "device_category_code": "CTD"}


@pytest.fixture()
def sensor_codes():
    return "salinity,temperature"


def test_scatter_plot_iso_date_format(caplog, client, device2, sensor_codes):
    client.widget.scatter_plot_two_sensors(
        device2,
        sensor_codes,
        date_from="2019-05-14T00:00:00.000Z",
        date_to="2019-05-15T00:00:00.000Z",
    )
    _assert_no_logs(caplog, logging.WARNING)


def test_scatter_plot_iso_date_format_no_data(caplog, client, device2, sensor_codes):
    client.widget.scatter_plot_two_sensors(
        device2,
        sensor_codes,
        date_from="2015-04-23T00:00:00.000Z",
        date_to="2015-04-24T00:00:00.000Z",
    )
    _assert_logs(caplog, logging.WARNING)


def test_scatter_plot_duration_date_format(caplog, client, device2, sensor_codes):
    client.widget.scatter_plot_two_sensors(device2, sensor_codes, date_from="-P1D")
    _assert_no_logs(caplog, logging.ERROR)


# Map widget tests


def test_map_widget(caplog, client):
    devices = [
        {
            "lat": 48.314627,
            "lon": -126.058106,
        },
        {
            "lat": 50.54427,
            "lon": -126.84264,
        },
    ]
    client.widget.map(devices)
    _assert_no_logs(caplog, logging.WARNING)


def test_map_widget_no_lat_key(caplog, client):
    devices = [
        {
            "lon": -126.058106,
        },
        {
            "lon": -126.84264,
        },
    ]
    client.widget.map(devices)
    _assert_logs(caplog, logging.WARNING)
