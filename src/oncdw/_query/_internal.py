from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import pandas as pd
import requests
import streamlit as st

import oncdw._util as util

if TYPE_CHECKING:
    from .._client import ONCDW


@dataclass
class Internal:
    _client: "ONCDW"

    @st.cache_data(ttl="12h")
    def get_scalar_data(
        self, sensor_id: int | str, last_days: int
    ) -> tuple[pd.DataFrame, str, int]:
        """
        Return scalar data in a pd.DataFrame by calling internal `ScalarDataAPIService`,
        together with label (combination of name and uofm) and sensor type id.

        The dataframe would have no empty cells, and have following columns:
        - datetime
        - min
        - max
        - avg
        - qaqcflag
        - label (with the format of "name (uofm)")
        """
        base_url = f"https://{self._client.hostname}/ScalarDataAPIService"
        now = datetime.now(timezone.utc)
        date_from_str, date_to_str = util.get_date_from_last_days(last_days, now)
        params = {
            "datefrom": date_from_str,
            "dateto": date_to_str,
            "sensorid": sensor_id,
            "option": 3,
            "isClean": "true",
            "plotpoints": 1500,
        }

        r = requests.get(base_url, params)

        payload = r.json()["payload"]

        ylabel = f"{payload['name']} ({payload['uofm']})"
        sensor_type_id = payload["sensortypeid"]

        df = pd.DataFrame(
            payload["data"], columns=["datetime", "min", "max", "avg", "qaqcflag"]
        )
        df.mask(df == "", inplace=True)
        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")

        return df, ylabel, sensor_type_id

    @st.cache_data(ttl="12h")
    def get_archive_files(self, device_code: int | str, last_days: int):
        raise NotImplementedError

    @st.cache_data(ttl="12h")
    def get_data_preview(
        self,
        sensor_id: int | None,
        device_category_id: int,
        search_tree_node_id: int,
        data_product_format_id: int,
        plot_number: int,
    ) -> str:
        base_url = f"https://{self._client.hostname}/DataPreviewService"
        params = {
            "searchTreeNodeId": search_tree_node_id,
            "deviceCategoryId": device_category_id,
            "sensorCodeId": sensor_id,
            "timeConfigId": 2,  # Week
            "dataProductFormatId": data_product_format_id,
            "plotNumber": plot_number,
            "operation": 5,  # GET_DATA_PREVIEW_PLOT
        }

        r = requests.get(base_url, params)
        payload = r.json()["payload"]

        if payload:
            return r.json()["payload"]["filePath"]
        else:
            return ""
