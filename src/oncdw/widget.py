from typing import TYPE_CHECKING

import pandas as pd
import streamlit as st

if TYPE_CHECKING:
    from ._client import ONCDW

from ._chart import Chart
from ._query import Query
from ._util import DataPreviewOption, Device, Sensor, get_date_from_last_days


def _error_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    return inner_function


def get_date_parameters(
    last_days: int | None,
    date_from: str | None,
    date_to: str | None,
) -> tuple[str, str]:
    """
    Get date parameters for queries.

    Widgets accept either last_days or date_from and date_to.
    If last_days is provided, it will calculate date_from and date_to based on current datetime.
    Else date_from and date_to will be used directly.
    """
    if last_days:
        return get_date_from_last_days(last_days)
    else:
        return date_from, date_to


class Widget:

    def __init__(self, client: "ONCDW"):
        self._query = Query(client)
        self._chart = Chart(client)

    # @_error_handler
    def time_series(
        self,
        sensor: int | dict,
        color: str = "#1f77b4",
        last_days: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        _sensor = Sensor(sensor)
        sensor_id = _sensor.get_sensor_id()

        date_from, date_to = get_date_parameters(
            last_days=last_days,
            date_from=date_from,
            date_to=date_to,
        )

        df, ylabel, _ = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id,
            date_from=date_from,
            date_to=date_to,
        )

        return self._chart.time_series(df, ylabel, color, st_wrapper, engine)

    @_error_handler
    def time_series_two_sensors(
        self,
        sensor1: int | dict,
        sensor2: int | dict,
        color1: str = "#57A44C",
        color2: str = "#1f77b4",
        last_days: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        _sensor1 = Sensor(sensor1)
        _sensor2 = Sensor(sensor2)
        sensor_id1 = _sensor1.get_sensor_id()
        sensor_id2 = _sensor2.get_sensor_id()

        last_days = last_days if last_days else 7
        date_from, date_to = get_date_parameters(
            last_days=last_days,
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

        return self._chart.time_series_two_sensors(
            df1,
            ylabel1,
            sensor_type1,
            sensor_id1,
            color1,
            df2,
            ylabel2,
            sensor_type2,
            sensor_id2,
            color2,
            st_wrapper,
            engine,
        )

    @_error_handler
    def table_archive_files(
        self,
        device: dict,
        last_days: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        _device = Device(device)

        device_code = _device.get_device_code()
        file_extensions = _device.get_file_extensions()

        date_from, date_to = get_date_parameters(
            last_days=last_days,
            date_from=date_from,
            date_to=date_to,
        )

        df = self._query.get_archive_files(
            device_code=device_code,
            date_from=date_from,
            date_to=date_to,
            file_extensions=file_extensions,
        )

        return self._chart.table_archive_files(df, st_wrapper, engine)

    @_error_handler
    def heatmap_archive_files(
        self,
        device: dict,
        last_days: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        _device = Device(device)

        device_code = _device.get_device_code()
        file_extensions = _device.get_file_extensions()

        date_from, date_to = get_date_parameters(
            last_days=last_days,
            date_from=date_from,
            date_to=date_to,
        )

        df = self._query.get_archive_files(
            device_code=device_code,
            date_from=date_from,
            date_to=date_to,
            file_extensions=file_extensions,
        )

        return self._chart.heatmap_archive_files(df, st_wrapper, engine)

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

        return self._chart.image(image_url, st_wrapper)

    @_error_handler
    def scatter_plot_two_sensors(
        self,
        device: dict,
        sensor_category_codes: str,
        last_days: int | None = None,
        resample_period: int | None = None,
        st_wrapper=True,
        engine: str | None = None,
    ):
        _device = Device(device)
        location_code = _device.get_location_code()
        device_category_code = _device.get_device_category_code()

        last_days = last_days if last_days else 1
        resample_period = resample_period if resample_period else 60

        df = self._query.get_scalar_data_two_sensors(
            location_code=location_code,
            device_category_code=device_category_code,
            sensor_category_codes=sensor_category_codes,
            resample_period=resample_period,
            last_days=last_days,
        )

        return self._chart.scatter_plot(df, st_wrapper, engine)

    @_error_handler
    def map(
        self,
        devices: list[dict],
        center_lat,
        center_lon,
        zoom,
        st_wrapper=True,
    ):
        return self._chart.map(
            pd.DataFrame(devices),
            center_lat=center_lat,
            center_lon=center_lon,
            zoom=zoom,
            st_wrapper=st_wrapper,
        )
