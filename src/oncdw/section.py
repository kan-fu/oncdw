from typing import TYPE_CHECKING

import streamlit as st
from onc import ONC

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

    def time_series(self, sensor: list, last_days: int | None = None):
        """
        Display time series plots for a given sensor or two sensors.

        Parameters
        ----------
        sensor : list
            A list representing a sensor or a pair of sensors.
            The format can be either:
            1. A single sensor, [sensor_id, sensor_name]
            2. A pair of sensors, [[sensor1_id, sensor1_name], [sensor2_id, sensor2_name]]
        """
        if isinstance(sensor[0], list | tuple):
            # If the sensor is a pair of sensors
            sensor1, sensor2 = sensor
            self._client.ui.sensors_two(sensor1, sensor2)
            self._client.widget.time_series_two_sensors(
                sensor1, sensor2, last_days=last_days
            )
        else:
            # If the sensor is a single sensor
            self._client.ui.sensor(sensor)
            self._client.widget.time_series(sensor, last_days=last_days)

    def data_preview(self, device: dict):
        """
        Assume data preview plots are placed in two columns,
        and the options are like
        1. [[x,1],[x,2],[x,3],[x,4],[y,1],[y,2]], or
        2. [[x,1,y],[x,2,y],[x,3,y],[x,4,y],[y,1,y],[y,2,y]] if it has sensor code id.

        """
        if "dataPreviewOptions" not in device:
            return

        st.subheader("Data Preview plot")

        # Data preview plots in two columns
        for i in range(0, len(device["dataPreviewOptions"]), 2):
            # The format of options is (data_product_format_id, plot_number, sensor_code_id)
            options = device["dataPreviewOptions"][i : i + 2]
            if len(options) == 2:
                option1, option2 = options
            else:
                # Deal with odd length of data preview options
                option1 = options[0]
                option2 = []

            # Manually add a dummy sensor code id if not present
            if len(option1) == 2:
                option1.append(0)
            if len(option2) == 2:
                option2.append(0)

            cols = st.columns(2)
            with st.container():
                with cols[0]:
                    self._client.widget.data_preview(
                        device,
                        data_product_format_id=option1[0],
                        plot_number=option1[1],
                        sensor_code_id=option1[2],
                    )

                with cols[1]:
                    if option2:
                        self._client.widget.data_preview(
                            device,
                            data_product_format_id=option2[0],
                            plot_number=option2[1],
                            sensor_code_id=option2[2],
                        )

    def location_expander(self, location: dict):
        if self._prev_location_code != location["locationCode"]:
            self._prev_location_code = location["locationCode"]
            onc = ONC(self._client.token)

            self._client.ui.location(location)
            location_info = onc.getLocations({"locationCode": location["locationCode"]})
            with st.expander("Location Info", expanded=False):
                st.json(location_info)

    def location_sidebar(self, location: dict):
        if self._prev_location_code_sidebar != location["locationCode"]:
            self._prev_location_code_sidebar = location["locationCode"]
            self._client.ui.location_sidebar(location)

    def sensor_sidebar(self, sensor: list):
        if isinstance(sensor[-1], list):
            # meaning the sensor list contains two sensors
            sensor0, sensor2 = sensor
            self._client.ui.sensors_two_sidebar(sensor0, sensor2)
        else:
            self._client.ui.sensor_sidebar(sensor)
