from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from ._client import ONCDW

from ._chart import Chart
from ._query import Query
from ._util import _get_id_from_sensor


def _get_code_from_device(device: str | dict) -> str:
    if isinstance(device, dict):
        device_code = device["deviceCode"]
    elif isinstance(device, str):
        device_code = device
    else:
        raise ValueError(
            "Please provide an str or a dict that contains 'deviceCode' as key and an str as value"
        )
    return device_code


class Widget:

    def __init__(self, client: "ONCDW"):
        self._query = Query(client)
        self._chart = Chart(client)

    def time_series(
        self,
        sensor: int | dict,
        color: str = "#1f77b4",
        last_days: int = 7,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        sensor_id = _get_id_from_sensor(sensor)

        df, ylabel, _ = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id,
            last_days=last_days,
        )

        return self._chart.time_series(df, ylabel, color, st_wrapper, engine)

    def time_series_two_sensors(
        self,
        sensor1: int | dict,
        sensor2: int | dict,
        color1: str = "#57A44C",
        color2: str = "#1f77b4",
        last_days: int = 7,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        sensor_id1 = _get_id_from_sensor(sensor1)
        sensor_id2 = _get_id_from_sensor(sensor2)

        df1, ylabel1, sensor_type1 = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id1,
            last_days=last_days,
        )

        df2, ylabel2, sensor_type2 = self._query.get_scalar_data(
            source="internal",
            sensor_id=sensor_id2,
            last_days=last_days,
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

    def table_archive_files(
        self,
        device: str | dict,
        file_extensions: list | None = None,
        last_days: int = 4,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        device_code = _get_code_from_device(device)

        if isinstance(device, dict) and file_extensions is None:
            file_extensions = device.get("fileExtensions")

        df = self._query.get_archive_files(
            device_code=device_code,
            last_days=last_days,
            file_extensions=file_extensions,
        )

        return self._chart.table_archive_files(df, st_wrapper, engine)

    def heatmap_archive_files(
        self,
        device: str | dict,
        file_extensions: list[str] | None = None,
        last_days: int = 7,
        st_wrapper: bool = True,
        engine: str | None = None,
    ):
        device_code = _get_code_from_device(device)

        if isinstance(device, dict) and file_extensions is None:
            file_extensions = device.get("fileExtensions")

        df = self._query.get_archive_files(
            device_code=device_code,
            last_days=last_days,
            file_extensions=file_extensions,
        )

        return self._chart.heatmap_archive_files(df, st_wrapper, engine)

    def data_preview(
        self,
        device: dict,
        data_product_format_id: int,
        plot_number: int = 1,
        sensor_code_id: int | None = None,
        st_wrapper=True,
    ):
        device_category_id = device["deviceCategoryId"]
        search_tree_node_id = device["searchTreeNodeId"]
        sensor_code_id = sensor_code_id if sensor_code_id else None

        image_url = self._query.get_data_preview(
            sensor_code_id=sensor_code_id,
            device_category_id=device_category_id,
            search_tree_node_id=search_tree_node_id,
            data_product_format_id=data_product_format_id,
            plot_number=plot_number,
        )

        return self._chart.image(image_url, st_wrapper)

    def scatter_plot_two_sensors(
        self,
        device: dict,
        sensor_category_codes: str,
        last_days: int = 1,
        resample_period=60,
        st_wrapper=True,
        engine: str | None = None,
    ):
        location_code = device["locationCode"]
        device_category_code = device["deviceCategoryCode"]

        df = self._query.get_scalar_data_two_sensors(
            location_code=location_code,
            device_category_code=device_category_code,
            sensor_category_codes=sensor_category_codes,
            resample_period=resample_period,
            last_days=last_days,
        )

        return self._chart.scatter_plot(df, st_wrapper, engine)

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
