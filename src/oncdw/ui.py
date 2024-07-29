from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from ._util import _get_id_from_sensor, _get_name_from_sensor


def _badge(left: str | int, right: str, color) -> str:

    def _sanitize(input):
        return str(input).replace(" ", "%20").replace("-", "--").replace("_", "__")

    encoded_left = _sanitize(left)
    encoded_right = _sanitize(right)
    img_alt_text = f"{left} - {right}"
    return f"![{img_alt_text}](https://img.shields.io/badge/{encoded_left}-{encoded_right}-{color})"


class UI:
    @staticmethod
    def import_custom_badge_css(sticky_device=False, sticky_location=False):
        badge_css = """
            /* Sidebar CSS */
            section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
                gap: 0rem;
            }

            section[data-testid="stSidebar"] h1 img {
                height: 2.25rem;
            }

            section[data-testid="stSidebar"] h2 img {
                height: 2rem;
                padding-left: 0.5rem;
            }

            section[data-testid="stSidebar"] h3 img {
                height: 1.75rem;
                padding-left: 1rem;
            }

            /* Body Badge CSS */
            h1 img {
                height: 2.5rem;
            }

            h2 img {
                height: 2.25rem;
            }

            h3 img {
                height: 2rem;
            }"""
        sticky_devices_css = (
            """
            section[data-testid="stMain"] div[data-testid="stElementContainer"]:has(h2) {
                position: sticky;
                top: 3rem;
                z-index:100;
                background-color: white;
            }"""
            if sticky_device
            else None
        )

        sticky_location_css = (
            """
            section[data-testid="stSidebar"] div[data-testid="stElementContainer"]:has(h1) {
                position: sticky;
                top: 0rem;
                z-index:100;
                padding: 1rem 0;
                background-color: rgb(240, 242, 246);
            }"""
            if sticky_location
            else None
        )

        st.markdown(
            f"""
            <style>
                {badge_css}
                {sticky_devices_css}
                {sticky_location_css}
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def _level_badge(
        level_func,
        left: str,
        right: str,
        href: str | None = None,
        anchor: str | None = None,
        color: str = "lightyellow",
    ):
        if href:
            assert href.startswith("http") or href.startswith("#")
            return level_func(f"[{_badge(left, right, color)}]({href})", anchor=anchor)
        else:
            return level_func(f"{_badge(left, right, color)}", anchor=anchor)

    @staticmethod
    def title_badge(
        left: str,
        right: str,
        href: str | None = None,
        anchor: str | None = None,
        color: str = "aqua",
    ):
        return UI._level_badge(st.title, left, right, href, anchor, color)

    @staticmethod
    def header_badge(
        left: str,
        right: str,
        href: str | None = None,
        anchor: str | None = None,
        color: str = "aqua",
    ):
        return UI._level_badge(st.header, left, right, href, anchor, color)

    @staticmethod
    def subheader_badge(
        left: str,
        right: str,
        href: str | None = None,
        anchor: str | None = None,
        color: str = "aqua",
    ):
        return UI._level_badge(st.subheader, left, right, href, anchor, color)

    @staticmethod
    def location(device: dict):
        left = device["locationCode"]
        right = device["locationName"]
        anchor = f"location-code-{left}"
        return UI.title_badge(left, right, anchor=anchor, color="lightblue")

    @staticmethod
    def location_sidebar(device: dict):
        left = "Site"
        right = device["locationCode"]
        href = f"#location-code-{right}"
        return UI.title_badge(left, right, href=href, color="lightblue")

    @staticmethod
    def device(device: dict):
        left = str(device["deviceId"])

        left_sanitized = left.replace(" & ", "--")

        right = device["deviceName"] if "deviceName" in device else device["deviceCode"]
        anchor = f"device-id-{left_sanitized}"
        if "&" in left:
            # This is a concat two-devices, no href is needed
            return UI.header_badge(left, right, anchor=anchor, color="lightgreen")
        else:
            href = f"https://data.oceannetworks.ca/DeviceListing?DeviceId={left}"
            return UI.header_badge(left, right, href, anchor, color="lightgreen")

    @staticmethod
    def device_sidebar(device: dict):
        left = str(device["deviceId"])

        left_sanitized = left.replace(" & ", "--")

        right = device["deviceCode"]
        href = f"#device-id-{left_sanitized}"

        return UI.header_badge(left, right, href, color="lightgreen")

    @staticmethod
    def sensor(sensor: dict | tuple | list, anchor: str | None = None):
        left = _get_id_from_sensor(sensor)
        right = _get_name_from_sensor(sensor)
        href = f"https://data.oceannetworks.ca/SensorListing?SensorId={left}"
        if anchor is None:
            anchor = f"sensor-id-{left}"

        return UI.subheader_badge(left, right, href, anchor, color="gold")

    @staticmethod
    def sensor_sidebar(sensor: dict | tuple | list, href: str | None = None):
        left = _get_id_from_sensor(sensor)
        right = _get_name_from_sensor(sensor)
        if href is None:
            href = f"#sensor-id-{left}"

        return UI.subheader_badge(left, right, href, color="gold")

    @staticmethod
    def sensors_two(sensor1: dict | tuple | list, sensor2: dict | tuple | list):
        col1, col2 = st.columns(2, gap="large")
        anchor = f"sensor-id-{sensor1[0]},{sensor2[0]}"
        with col1:
            UI.sensor(sensor1, anchor=anchor)
        with col2:
            UI.sensor(sensor2, anchor=anchor)

    @staticmethod
    def sensors_two_sidebar(sensor1: dict | tuple | list, sensor2: dict | tuple | list):
        href = f"#sensor-id-{sensor1[0]},{sensor2[0]}"
        UI.sensor_sidebar(sensor1, href=href)
        UI.sensor_sidebar(sensor2, href=href)

    @staticmethod
    def show_time_difference(latest_datetime: pd.Timestamp):
        time_delta = (
            datetime.now(tz=timezone.utc).replace(tzinfo=None) - latest_datetime
        )
        st.info(
            f"The latest datetime for the cached data is {latest_datetime.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"which is {time_delta.total_seconds()/3600:.2f} hours ago."
        )
