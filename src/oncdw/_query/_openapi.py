from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd
import streamlit as st
from onc import ONC

import oncdw._util as util

if TYPE_CHECKING:
    from .._client import ONCDW


@dataclass
class OpenAPI:
    _client: "ONCDW"

    def _get_onc(self) -> ONC:
        is_prod = self._client.hostname == "data.oceannetworks.ca"
        return ONC(
            self._client.token, production=is_prod, showInfo=self._client.showInfo
        )

    def get_scalar_data(self, sensor_id: int | str, last_days: int):
        raise NotImplementedError

    @st.cache_data(ttl="12h")
    def get_archive_files(
        self, device_code: str, file_extensions: list[str], last_days: int
    ) -> pd.DataFrame:
        archive_files = self._get_onc().getArchivefile(
            {
                "deviceCode": device_code,
                "dateFrom": f"-P{last_days}D",
                "returnOptions": "all",
            }
        )["files"]

        df = pd.DataFrame(
            archive_files,
            columns=[
                "dataProductCode",
                "filename",
                "dateFrom",
                "dateTo",
                "uncompressedFileSize",
            ],
        )
        if file_extensions:
            df = df[
                df["filename"]
                .str.extract(r".(\w+)$", expand=False)
                .isin(file_extensions)
            ]

        if df.empty:
            return df

        df["dataProductCode"] = df.apply(
            lambda row: f"{row.dataProductCode} ({Path(row.filename).suffix})", axis=1
        )
        df["dateFrom"] = pd.to_datetime(df["dateFrom"]).dt.tz_localize(None)
        df["dateTo"] = pd.to_datetime(df["dateTo"]).dt.tz_localize(None)

        df["uncompressedFileSize"] = df["uncompressedFileSize"].apply(
            lambda x: f"{x / 1024 ** 2:.2f} MB"
        )
        df["filename"] = df["filename"].apply(
            util.get_archive_file_download_link, token=self._client.token
        )

        return df

    @st.cache_data(ttl="12h")
    def get_scalar_data_two_sensors(
        self,
        location_code: str,
        device_category_code: str,
        sensor_category_codes: str,
        resample_period: int | None,
        last_days: int = 1,
    ) -> pd.DataFrame:
        scalar_data = self._get_onc().getScalardata(
            {
                "locationCode": location_code,
                "dateFrom": f"-P{last_days}D",
                "deviceCategoryCode": device_category_code,
                "sensorCategoryCodes": sensor_category_codes,
                "resamplePeriod": resample_period,
            }
        )

        if scalar_data["sensorData"] is None:
            return pd.DataFrame(columns=sensor_category_codes.split(","))

        df = pd.DataFrame(
            {
                data["sensorCategoryCode"]: data["data"]["values"]
                for data in scalar_data["sensorData"]
            }
        )
        df["sampleTimes"] = pd.to_datetime(
            scalar_data["sensorData"][0]["data"]["sampleTimes"]
        ).tz_localize(None)

        return df
