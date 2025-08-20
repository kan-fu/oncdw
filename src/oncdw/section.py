from typing import TYPE_CHECKING

import streamlit as st
from onc import ONC

from ._util import Device

if TYPE_CHECKING:
    from ._client import ONCDW


class Section:
    def __init__(self, client: "ONCDW"):
        self._client = client
        self._prev_location_code = None
        self._prev_location_code_sidebar = None

    def links(self, links: dict, header: str = "Links"):
        """
        Display a section with links.

        Parameters
        ----------
        links : dict
            A dictionary of links to be displayed at the top of the page.
            The keys are the link titles, and the values are the URLs.
        """
        st.header(header)
        for title, url in links.items():
            st.subheader(f"[{title}]({url})")

    def state_of_ocean_images(self, location_code: str):
        """
        Display the State of Ocean images for a given location code.

        Parameters
        ----------
        location_code : str
            The location code to construct the image URLs.

        Returns
        -------
        badges : list of tuples
            A list of tuples containing the badge titles and their corresponding URLs.
        """
        images = [
            (
                "State of Ocean Climate plot",
                f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv-Climate.png",
            ),
            (
                "State of Ocean Anomaly plot",
                f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv-Anomaly.png",
            ),
            (
                "State of Ocean Min/Max plot",
                f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv_MinMaxAvg1day.png",
            ),
        ]

        for title, url in images:
            st.header(title)
            st.image(url)

        # Format is [(badge_left, badge_right, href)]
        badges = [
            ("SOOC", "Climate", "#state-of-ocean-climate-plot"),
            ("SOOA", "Anomaly", "#state-of-ocean-anomaly-plot"),
            ("SOOM", "MinMax", "#state-of-ocean-min-max-plot"),
        ]

        return badges

    def time_series(self, sensor: list | dict, last_days: int = 7):
        """
        Display time series plots for a given sensor or two sensors.

        Parameters
        ----------
        sensor : list
            A list representing a sensor or a pair of sensors.
            The format can be either:
            1. dict: a single sensor, {"sensor_id": sensor_id, "sensor_name": sensor_name}
            2. list: a pair of sensors, [{},{}]. The format of each dict is the same as a single sensor
        """
        if isinstance(sensor, list):
            # The sensor is a pair of sensors
            sensor1, sensor2 = sensor
            self._client.ui.sensors_two(sensor1, sensor2)
            self._client.widget.time_series_two_sensors(
                sensor1, sensor2, last_days=last_days
            )
        elif isinstance(sensor, dict):
            # The sensor is a single sensor
            self._client.ui.sensor(sensor)
            self._client.widget.time_series(sensor, last_days=last_days)
        else:
            raise ValueError(
                f"Invalid sensor format: {sensor}. Expected a list or dict."
            )

    def data_preview(self, device: dict):
        """
        Assume data preview plots are placed in two columns,
        and the options are a dict that has the following format:
        {
            "data_product_format_id": data_product_format_id,
            "plot_number": plot_number,
            "sensor_code_id": sensor_code_id # This is optional
        }
        """
        _device = Device(device)
        data_preview_options = _device.get_data_preview_options()
        if data_preview_options is None:
            return

        st.subheader("Data Preview plot")

        # Data preview plots in two columns
        for i in range(0, len(data_preview_options), 2):
            # Get two data preview options for two columns, if available
            options: list[dict] = data_preview_options[i : i + 2]
            if len(options) == 2:
                option1, option2 = options
            else:
                # Deal with odd length of data preview options
                option1 = options[0]
                option2 = None

            cols = st.columns(2)
            with st.container():
                with cols[0]:
                    self._client.widget.data_preview(device, option1)

                with cols[1]:
                    if option2:
                        self._client.widget.data_preview(device, option2)

    def location_expander(self, location: dict):
        _location = Device(location)
        if self._prev_location_code != _location.get_location_code():
            self._prev_location_code = _location.get_location_code()
            onc = ONC(self._client.token)

            self._client.ui.location(location)
            location_info = onc.getLocations(
                {"locationCode": _location.get_location_code()}
            )
            with st.expander("Location Info", expanded=False):
                st.json(location_info)

    def location_sidebar(self, location: dict):
        _location = Device(location)
        if self._prev_location_code_sidebar != _location.get_location_code():
            self._prev_location_code_sidebar = _location.get_location_code()
            self._client.ui.location_sidebar(location)

    def sensor_sidebar(self, sensor: list | dict):
        if isinstance(sensor, list):
            # The sensor list contains two sensors
            sensor0, sensor2 = sensor
            self._client.ui.sensors_two_sidebar(sensor0, sensor2)
        else:
            # The sensor dict is a single sensor
            self._client.ui.sensor_sidebar(sensor)
