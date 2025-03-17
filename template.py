import json
import re

import streamlit as st

from oncdw import ONCDW


def Barkley(
    json_filename: str,
    location_code: str,
    page_title: str,
    device_name_id: str,
    device_console_url: str,
    annotation_url: str,
    sticky_device: bool = True,
    sticky_location: bool = True,
):
    """
    Barkely is a template for the dashboard that consists of five sections:

    1. Links to the Oceans 3.0 Device Console and Oceans 3.0 Annotation.
    2. Three images: State of Ocean Climate plot, State of Ocean Anomaly plot, and State of Ocean Min/Max plot.
    3. List of devices, each having a list of sensors with a time series plot.
    4. List of dual devices, each having a two-sensors time series plot.
    5. List of devices, each having a list of data preview plots and an archive file table.

    Parameters
    ----------
    json_filename : str
        The name of the JSON file that contains the data. It should have suffix _1.json (for section 3 and 4)
        and _2.json (for section 5).
    location_code : str
        The location code of the devices.
    page_title : str
        The title of the page.
    device_name_id : str
        The name and ID of the device shown in the Oceans 3.0 device console link.
    device_console_url : str
        The URL of the device for the Oceans 3.0 device console.
    annotation_url : str
        The URL of the device for the Oceans 3.0 annotation.
    sticky_device : bool, default True
        Whether to show the device as sticky in the main part.
    sticky_location : bool, default True
        Whether to show the location as sticky in the sidebar.
    """
    st.set_page_config(layout="wide", page_title=page_title)

    with open(f"pages/{json_filename}_1.json") as f:
        devices1 = json.load(f)

    with open(f"pages/{json_filename}_2.json") as f:
        devices2 = json.load(f)

    images = [
        (
            "State of Ocean Climate plot",
            f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv-Climate.png",
            ("SOOC", "Climate"),
        ),
        (
            "State of Ocean Anomaly plot",
            f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv-Anomaly.png",
            ("SOOA", "Anomaly"),
        ),
        (
            "State of Ocean Min/Max plot",
            f"https://ftp.oceannetworks.ca/pub/DataProducts/SOO/{location_code}/{location_code}-StateOfOceanEnv_MinMaxAvg1day.png",
            ("SOOM", "MinMax"),
        ),
    ]

    client = ONCDW(file=page_title)

    client.ui.import_custom_badge_css(
        sticky_device=sticky_device, sticky_location=sticky_location
    )

    st.title(f"{page_title} Monitoring Dashboard")

    client.ui.show_time_difference(client.now)

    with st.sidebar:
        client.ui.location_sidebar(devices1[0])
        client.ui.header_badge("", "Links", "#links")
        for title, _, (key, val) in images:
            # Format "State of Ocean Climate plot" to "state-of-ocean-climate-plot"
            href = "#" + re.sub(r"\W+", "-", title).lower()
            client.ui.header_badge(key, val, href)

        st.divider()

        for device in devices1:
            client.ui.device_sidebar(device)
            if "&" not in device["deviceId"]:
                for sensor in device["sensors"]:
                    client.ui.sensor_sidebar(sensor)
            else:
                for sensor1, sensor2 in device["sensors"]:
                    client.ui.sensors_two_sidebar(sensor1, sensor2)
            st.divider()

        for device in devices2:
            client.ui.device_sidebar(device)
            st.divider()

    # All the devices belong to the same location
    client.ui.location(devices1[0])
    st.header("Links")

    st.subheader(
        f"[Oceans 3.0 Device Console for {device_name_id}]({device_console_url})"
    )

    st.subheader(f"[Oceans 3.0 Annotation for {device_name_id}]({annotation_url})")

    for title, url, _ in images:
        st.header(title)
        st.image(url)

    for device in devices1:
        client.ui.device(device)
        if "&" not in device["deviceId"]:
            for sensor in device["sensors"]:
                client.ui.sensor(sensor)
                client.widget.time_series(sensor)
        else:
            for sensor1, sensor2 in device["sensors"]:
                client.ui.sensors_two(sensor1, sensor2)
                client.widget.time_series_two_sensors(sensor1, sensor2)

    for device in devices2:
        client.ui.device(device)
        # Data preview plots in two columns
        for i in range(len(device["dataPreviewOptions"]) // 2):
            # The format of options is (data_product_format_id, plot_number)
            option1, option2 = (
                device["dataPreviewOptions"][2 * i],
                device["dataPreviewOptions"][2 * i + 1],
            )

            data_product_format_id = option1[0]
            # Assumption check
            assert (
                option2[0] == data_product_format_id
            ), "two options should have the same format id"
            assert (
                option1[1] + 1 == option2[1]
            ), "two options should have correct plot number"

            cols = st.columns(2)
            with st.container():
                for plot_number in (option1[1], option2[1]):
                    with cols[(plot_number - 1) % 2]:
                        client.widget.data_preview(
                            device, data_product_format_id, plot_number=plot_number
                        )

        # Archive file table
        st.subheader("Archive file table")
        client.widget.table_archive_files(device)


def Neptune(
    json_filename: str,
    page_title: str,
    center_lat: float = 49.3,
    center_lon: float = -126.3,
    zoom: float = 6,
    data_preview_widget: bool = True,
    time_series_widget: bool = True,
    map_widget: bool = True,
    sticky_device: bool = True,
):
    """
    Neptune is a template for the dashboard that consists of two sections:

    1. A map of the locations.
    2. A list of devices, each having three widgets
        - Data Preview plot, optional
        - Archive file table
        - Time series two sensors, optional

    A sample format for the expected json file is listed below.
    Some optional keys can be left out if the corresponding widget is not present.
    [
        {
            "locationCode": "CDFM",  # required
            "deviceCode": "RBRQUARTZ3BPRZERO207600",  # required
            "locationName": "Clayoquot Deformation Front Middle",  # requried
            "deviceId": 67660,  # required
            "deviceCategoryId": 3,  # optional for data preview widget
            "lat": 48.598887,  # optional for map widget
            "lon": -127.079527,  # optional for map widget
            "sensors": [
                {"sensorId": 77540, "sensorName": "AZA Seafloor Pressure"},
                {"sensorId": 77600, "sensorName": "AZA Raw Pressure"},
            ],  # optional for time series widget
            "searchTreeNodeId": 2868,  # optional for data preview widget
            "dataPreviewOptions": [[3, 1], [3, 2]], # optional for data preview widget [(data_product_format_id, plot_number)]
        }
    ]

    Parameters
    ----------
    json_filename : str
        The name of the JSON file that contains the data.
    page_title : str
        The title of the page.
    center_lat : float, optional
        The latitude of the center of the map.
    center_lon : float, optional
        The longitude of the center of the map.
    zoom : float, optional
        The zoom level of the map.
    data_preview_widget : bool, default True
        Whether to show the data preview widget.
    map_widget: bool, default True
        Whether to show the map widget.
    sticky_device : bool, default True
        Whether to show the device as sticky in the main part.
    """
    st.set_page_config(layout="wide", page_title=page_title)

    with open(f"pages/{json_filename}.json") as f:
        devices = json.load(f)

    client = ONCDW(file=page_title)

    # custom css
    client.ui.import_custom_badge_css(sticky_device=sticky_device)

    st.title(f"{page_title} Monitoring Dashboard")
    client.ui.show_time_difference(client.now)

    if map_widget:
        client.widget.map(
            devices, center_lat=center_lat, center_lon=center_lon, zoom=zoom
        )

    with st.sidebar:
        st.title("Device List")

        for device in devices:
            client.ui.location_sidebar(device)
            client.ui.device_sidebar(device)
            if time_series_widget:
                # Only list sensors if times series widget is present
                for sensor in device["sensors"]:
                    client.ui.sensor_sidebar(sensor)
            st.divider()

    for device in devices:
        client.ui.location(device)
        client.ui.device(device)
        if data_preview_widget:
            # Data Preview png
            st.subheader("Data Preview plot")

            # Data preview plots in two columns
            for i in range(len(device["dataPreviewOptions"]) // 2):
                # The format of options is (data_product_format_id, plot_number)
                option1, option2 = (
                    device["dataPreviewOptions"][2 * i],
                    device["dataPreviewOptions"][2 * i + 1],
                )

                data_product_format_id = option1[0]
                # Assumption check
                assert (
                    option2[0] == data_product_format_id
                ), "two options should have the same format id"
                assert (
                    option1[1] + 1 == option2[1]
                ), "two options should have correct plot number"

                cols = st.columns(2)
                with st.container():
                    for plot_number in (option1[1], option2[1]):
                        with cols[(plot_number - 1) % 2]:
                            client.widget.data_preview(
                                device, data_product_format_id, plot_number=plot_number
                            )

        # Archive file table
        st.subheader("Archive file table")
        client.widget.table_archive_files(device)

        if time_series_widget:
            # Time series two sensors
            st.subheader("Time series")
            sensor1, sensor2 = (
                device["sensors"][0],
                device["sensors"][1],
            )
            col1, col2 = st.columns(2, gap="large")
            with col1:
                client.ui.sensor(sensor1)
            with col2:
                client.ui.sensor(sensor2)

            client.widget.time_series_two_sensors(sensor1, sensor2, last_days=2)
