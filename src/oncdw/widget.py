import logging
from typing import TYPE_CHECKING

import pandas as pd
import pydeck as pdk
import streamlit as st

if TYPE_CHECKING:
    from ._client import ONCDW

from ._chart import Chart
from ._query import Query
from ._util import DataPreviewOption, Device, Sensor, parse_datetime_parameters

logger = logging.getLogger(__name__)


def _log_no_data_warning(warning_msg):
    logger.warning(warning_msg)
    return st.warning(warning_msg)


def _error_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            logger.exception(f"Error in {func.__name__}: {e}")

    return inner_function


class Widget:

    def __init__(self, client: "ONCDW"):
        self._query = Query(client)
        self._chart = Chart(client)

    @_error_handler
    def time_series(
        self,
        sensor: int | dict,
        date_from: str = "-P2D",
        date_to: str | None = None,
        color: str = "#1f77b4",
        st_wrapper: bool = True,
    ):
        _sensor = Sensor(sensor)
        sensor_id = _sensor.get_sensor_id()

        date_from, date_to = parse_datetime_parameters(
            date_from=date_from,
            date_to=date_to,
        )

        df, ylabel, _ = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id,
            date_from=date_from,
            date_to=date_to,
        )

        if df.empty and st_wrapper:
            warning_msg = f"No data available for time series plot of {ylabel}."
            return _log_no_data_warning(warning_msg)

        return self._chart.time_series(df, ylabel, color, st_wrapper)

    @_error_handler
    def time_series_two_sensors(
        self,
        sensor1: int | dict,
        sensor2: int | dict,
        date_from: str = "-P2D",
        date_to: str | None = None,
        color1: str = "#57A44C",
        color2: str = "#1f77b4",
        st_wrapper: bool = True,
    ):
        _sensor1 = Sensor(sensor1)
        _sensor2 = Sensor(sensor2)
        sensor_id1 = _sensor1.get_sensor_id()
        sensor_id2 = _sensor2.get_sensor_id()

        date_from, date_to = parse_datetime_parameters(
            date_from=date_from,
            date_to=date_to,
        )

        df1, ylabel1, sensor_type1 = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id1,
            date_from=date_from,
            date_to=date_to,
        )

        df2, ylabel2, sensor_type2 = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id2,
            date_from=date_from,
            date_to=date_to,
        )

        if df1.empty and df2.empty and st_wrapper:
            warning_msg = f"No scalar data available for time series plot of {ylabel1} and {ylabel2}."
            return _log_no_data_warning(warning_msg)

        return self._chart.time_series_two_sensors(
            df1,
            ylabel1,
            sensor_type1,
            color1,
            df2,
            ylabel2,
            sensor_type2,
            color2,
            st_wrapper,
        )

    @_error_handler
    def table_archive_files(
        self,
        device: dict,
        date_from: str = "-P7D",
        date_to: str | None = None,
        st_wrapper: bool = True,
    ):
        _device = Device(device)

        device_code = _device.get_device_code()
        file_extensions = _device.get_file_extensions()

        df = self._query.get_archive_files(
            device_code=device_code,
            date_from=date_from,
            date_to=date_to,
            file_extensions=file_extensions,
        )

        if df.empty:
            warning_msg = f"No archive files available for device {device_code}."
            return _log_no_data_warning(warning_msg)

        return self._chart.table_archive_files(df, st_wrapper)

    @_error_handler
    def data_preview(
        self,
        device: dict,
        data_preview_option: dict,
        st_wrapper=True,
    ):
        _device = Device(device)

        device_category_id = _device.get_device_category_id()
        search_tree_node_id = _device.get_search_tree_node_id()

        _data_preview_option = DataPreviewOption(data_preview_option)

        data_product_format_id = _data_preview_option.get_data_product_format_id()
        plot_number = _data_preview_option.get_plot_number()
        sensor_code_id = _data_preview_option.get_sensor_code_id()

        image_url = self._query.get_data_preview(
            device_category_id=device_category_id,
            search_tree_node_id=search_tree_node_id,
            data_product_format_id=data_product_format_id,
            plot_number=plot_number,
            sensor_code_id=sensor_code_id,
        )

        if not image_url:
            return _log_no_data_warning("No data preview image available.")

        return self._chart.image(image_url, st_wrapper)

    @_error_handler
    def heatmap_archive_files(
        self,
        device: dict,
        date_from: str = "-P7D",
        date_to: str | None = None,
        st_wrapper: bool = True,
    ):
        _device = Device(device)

        device_code = _device.get_device_code()
        file_extensions = _device.get_file_extensions()

        df = self._query.get_archive_files(
            device_code=device_code,
            date_from=date_from,
            date_to=date_to,
            file_extensions=file_extensions,
        )

        if df.empty:
            warning_msg = (
                f"No heatmap archive files available for device {device_code}."
            )
            return _log_no_data_warning(warning_msg)

        return self._chart.heatmap_archive_files(df, st_wrapper)

    @_error_handler
    def scatter_plot_two_sensors(
        self,
        device: dict,
        sensor_category_codes: str,
        date_from: str | None = None,
        date_to: str | None = None,
        resample_period: int | None = None,
        st_wrapper=True,
    ):
        _device = Device(device)
        location_code = _device.get_location_code()
        device_category_code = _device.get_device_category_code()

        resample_period = resample_period if resample_period else 60

        df = self._query.get_scalar_data_two_sensors(
            location_code=location_code,
            device_category_code=device_category_code,
            sensor_category_codes=sensor_category_codes,
            resample_period=resample_period,
            date_from=date_from,
            date_to=date_to,
        )

        col1, col2 = df.columns[0], df.columns[1]

        if df.empty and st_wrapper:
            warning_msg = f"No data available for scatter plot of {col1} and {col2}."
            return _log_no_data_warning(warning_msg)

        return self._chart.scatter_plot(df, st_wrapper)

    @_error_handler
    def map(
        self,
        devices: list[dict],
        center_lat: float | None = None,
        center_lon: float | None = None,
        zoom: int | None = None,
        st_wrapper=True,
    ):
        df = pd.DataFrame(devices)
        if ("lat" not in df.columns or "lon" not in df.columns) and st_wrapper:
            # To correctly render a map, both 'lat' and 'lon' columns are required
            warning_msg = "No location data (lat and lon) for the map widget."
            return _log_no_data_warning(warning_msg)

        initial_view_state = pdk.data_utils.viewport_helpers.compute_view(
            df[["lon", "lat"]]
        )

        if center_lat:
            initial_view_state.latitude = center_lat
        if center_lon:
            initial_view_state.longitude = center_lon
        if zoom:
            initial_view_state.zoom = zoom

        return self._chart.map(
            df,
            initial_view_state=initial_view_state,
            st_wrapper=st_wrapper,
        )
