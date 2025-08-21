from typing import TYPE_CHECKING

import pandas as pd
import streamlit as st

from ._altair import Altair

if TYPE_CHECKING:
    from .._client import ONCDW


def _show_latest_timestamp(
    df, ylabel, now, time_diff_threshold: pd.Timedelta | None = None
):
    time_diff_threshold = (
        time_diff_threshold if time_diff_threshold else pd.Timedelta(1, "h")
    )
    if df.datetime.size > 0:
        latest_df_timestamp = df["datetime"].iloc[-1]
        message = f"The latest UTC timestamp for {ylabel} is: {latest_df_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        time_diff: pd.Timedelta = now - latest_df_timestamp
        if time_diff < time_diff_threshold:
            show = st.info
        else:
            show = st.warning
            message = (
                f"{message}, which is {time_diff.total_seconds()/3600:.2f} hours ago"
            )
        show(message)


class Chart:
    def __init__(self, client: "ONCDW") -> None:
        self._client = client

    def time_series(self, df, ylabel, color, st_wrapper):
        _show_latest_timestamp(df, ylabel, self._client.now)
        return Altair.time_series(df, ylabel, color, st_wrapper)

    def time_series_two_sensors(
        self,
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
    ):
        # If two sensors have the same sensor type, ylabel(i.e. name + uofm)
        # might not be enough to uniquely identify one sensor
        if ylabel1 == ylabel2:
            ylabel1 = f"{ylabel1} - {sensor_id1}"
            ylabel2 = f"{ylabel2} - {sensor_id2}"
        _show_latest_timestamp(df1, ylabel1, self._client.now)
        _show_latest_timestamp(df2, ylabel2, self._client.now)
        return Altair.time_series_two_sensors(
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

    def table_archive_files(self, df, st_wrapper):
        return Altair.table_archive_files(df, st_wrapper)

    def heatmap_archive_files(self, df, st_wrapper):
        return Altair.heatmap_archive_files(df, st_wrapper)

    def image(self, url: str, st_wrapper: bool):
        if not st_wrapper:
            return url
        if not url:
            return st.warning("No data preview image available.")
        return st.image(url)

    def scatter_plot(self, df, st_wrapper):
        return Altair.scatter_plot(df, st_wrapper)

    def map(self, df, center_lat, center_lon, zoom, st_wrapper):
        return Altair.map(
            df,
            center_lat=center_lat,
            center_lon=center_lon,
            zoom=zoom,
            st_wrapper=st_wrapper,
        )
