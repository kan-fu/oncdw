from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from ._util import _get_id_from_sensor, _get_name_from_sensor


def _badge_shields(left: str | int, right: str, color) -> str:

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
    def _badge(
        st_func,
        left: str,
        right: str,
        href: str,
        anchor: str,
        color: str,
    ):
        """
        Basic function to create a badge with an anchor and an optional href link.
        """
        if href:
            assert href.startswith("http") or href.startswith("#")
            return st_func(
                f"[{_badge_shields(left, right, color)}]({href})", anchor=anchor
            )
        else:
            return st_func(f"{_badge_shields(left, right, color)}", anchor=anchor)

    @staticmethod
    def h1_badge(
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        return UI._badge(st.title, left, right, href, anchor, color)

    @staticmethod
    def h2_badge(
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        return UI._badge(st.header, left, right, href, anchor, color)

    @staticmethod
    def h3_badge(
        left: str,
        right: str,
        href: str = "",
        anchor: str = "",
        color: str = "aqua",
    ):
        return UI._badge(st.subheader, left, right, href, anchor, color)

    @staticmethod
    def location(location: dict):
        """
        Location badge wrapped inside a h1 tag.

        The href is a link to the Data Search page for the location code.
        The anchor is matched with the href of `location_sidebar()`.

        Parameters
        ----------
        location: dict
            A dictionary containing the location code and name.
            Usually it is a device dict that has location info inside.

        Example
        -------
        >>> device = {
        ...     "locationCode": "CODE",
        ...     "locationName": "Location Name",
        ... }
        >>> UI.location(device)
        """
        left = location["locationCode"]
        right = location["locationName"]
        href = f"https://data.oceannetworks.ca/DataSearch?location={left}"
        anchor = f"location-code-{left}"

        return UI.h1_badge(left, right, href=href, anchor=anchor, color="lightblue")

    @staticmethod
    def location_sidebar(location: dict):
        """
        Location badge for the sidebar wrapped inside a h1 tag.

        The href is a link to the anchor of `location()`.

        Parameters
        ----------
        location: dict
            A dictionary containing the location code and name.
            Usually it is a device dict that has location info inside.

        Example
        -------
        >>> device = {
        ...     "locationCode": "CODE",
        ...     "locationName": "Location Name",
        ... }
        >>> UI.location_sidebar(device)
        """
        left = "Site"
        right = location["locationCode"]
        href = f"#location-code-{right}"
        return UI.h1_badge(left, right, href=href, color="lightblue")

    @staticmethod
    def device(device: dict):
        """
        Device badge wrapped inside a h2 tag.

        The href is a link to the Data Details page for the device id.
        The anchor is matched with the href of `device_sidebar()`.
        Device name is used as the right side of the badge if present, otherwise device code is used.

        Parameters
        ----------
        device: dict
            A dictionary containing the device id, device code and device name.

        Example
        -------
        >>> device = {
        ...     "deviceId": "12345",
        ...     "deviceName": "Device Name",
        ...     "deviceCode": "CODE"
        ... }
        >>> UI.device(device)
        """

        left = str(device["deviceId"])

        left_sanitized = left.replace(" & ", "--")

        right = device["deviceName"] if "deviceName" in device else device["deviceCode"]
        anchor = f"device-id-{left_sanitized}"
        if "&" in left:
            # This is a concat two-devices, no href is needed
            return UI.h2_badge(left, right, anchor=anchor, color="lightgreen")
        else:
            href = f"https://data.oceannetworks.ca/DeviceListing?DeviceId={left}"
            return UI.h2_badge(left, right, href, anchor, color="lightgreen")

    @staticmethod
    def device_sidebar(device: dict):
        """
        Device badge for the side bar wrapped inside a h2 tag.

        The href a link to the anchor of `device()`.

        Parameters
        ----------
        device: dict
            A dictionary containing the device id and device code.

        Example
        -------
        >>> device = {
        ...     "deviceId": "12345",
        ...     "deviceCode": "CODE"
        ... }
        >>> UI.device_sidebar(device)
        """
        left = str(device["deviceId"])

        left_sanitized = left.replace(" & ", "--")

        right = device["deviceCode"]
        href = f"#device-id-{left_sanitized}"

        return UI.h2_badge(left, right, href, color="lightgreen")

    @staticmethod
    def sensor(sensor: dict | tuple | list, anchor: str = ""):
        """
        Sensor badge wrapped inside a h3 tag.

        The href is a link to the Sensor Details page for the sensor id.
        The anchor is matched with the href of `sensor_sidebar()`.

        Parameters
        ----------
        sensor: dict | tuple | list
            A dictionary containing the sensor id and sensor name, or a tuple/list with sensor id and name.

        Example
        -------
        >>> sensor = {
        ...     "sensorId": "67900",
        ...     "sensorName": "Sensor Name"
        ... }
        >>> UI.sensor_sidebar(sensor)
        """
        left = _get_id_from_sensor(sensor)
        right = _get_name_from_sensor(sensor)
        href = f"https://data.oceannetworks.ca/SensorListing?SensorId={left}"
        if not anchor:
            anchor = f"sensor-id-{left}"

        return UI.h3_badge(left, right, href, anchor, color="gold")

    @staticmethod
    def sensor_sidebar(sensor: dict | tuple | list, href: str | None = None):
        """
        Sensor badge for the side bar wrapped inside a h3 tag.

        The href a link to the anchor of `sensor()`.

        Parameters
        ----------
        sensor: dict
            A dictionary containing the sensor id and sensor name.

        Example
        -------
        >>> sensor = {
        ...     "sensorId": "67900",
        ...     "sensorName": "Sensor Name"
        ... }
        >>> UI.sensor_sidebar(sensor)
        """
        left = _get_id_from_sensor(sensor)
        right = _get_name_from_sensor(sensor)
        if href is None:
            href = f"#sensor-id-{left}"

        return UI.h3_badge(left, right, href, color="gold")

    @staticmethod
    def sensors_two(sensor1: dict | tuple | list, sensor2: dict | tuple | list):
        """
        Two sensor badges for two sensors wrapped inside a h3 tag.

        The href is a link to the Sensor Details page for the individual sensor id.
        The anchor is matched with the href of `sensors_two_sidebar()`.

        Parameters
        ----------
        sensor1, sensor2: dict | tuple | list
            A dictionary containing the sensor id and sensor name, or a tuple/list with sensor id and name.

        Example
        -------
        >>> sensor1 = {
        ...     "sensorId": "167900",
        ...     "sensorName": "Sensor Name 1"
        ... }
        >>> sensor2 = {
        ...     "sensorId": "267900",
        ...     "sensorName": "Sensor Name 2"
        ... }
        >>> UI.sensor_sidebar(sensor1, sensor2)
        """
        col1, col2 = st.columns(2, gap="large")
        anchor = (
            f"sensor-id-{_get_id_from_sensor(sensor1)},{_get_id_from_sensor(sensor2)}"
        )
        with col1:
            UI.sensor(sensor1, anchor=anchor)
        with col2:
            UI.sensor(sensor2, anchor=anchor)

    @staticmethod
    def sensors_two_sidebar(sensor1: dict | tuple | list, sensor2: dict | tuple | list):
        """
        One sensor badge for two sensors for the sidebar wrapped inside a h3 tag.

        The href a link to the anchor of `sensors_two()`.

        Parameters
        ----------
        sensor1, sensor2: dict | tuple | list
            A dictionary containing the sensor id and sensor name, or a tuple/list with sensor id and name.

        Example
        -------
        >>> sensor1 = {
        ...     "sensorId": "167900",
        ...     "sensorName": "Sensor Name 1"
        ... }
        >>> sensor2 = {
        ...     "sensorId": "267900",
        ...     "sensorName": "Sensor Name 2"
        ... }
        >>> UI.sensors_two_sidebar(sensor1, sensor2)
        """
        href = (
            f"#sensor-id-{_get_id_from_sensor(sensor1)},{_get_id_from_sensor(sensor2)}"
        )
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
