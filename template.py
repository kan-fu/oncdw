import json

import streamlit as st

from oncdw import ONCDW


def template3(
    json_filename: str,
    page_title: str,
    center_lat: float = 49.3,
    center_lon: float = -126.3,
    zoom: float = 6,
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
        devices: dict = json.load(f)

    client = ONCDW()

    # custom css
    client.ui.import_custom_badge_css(sticky_device=sticky_device)

    st.title(f"{page_title} Monitoring Dashboard")

    if "lat" in devices[0] and "lon" in devices[0]:
        client.widget.map(
            devices, center_lat=center_lat, center_lon=center_lon, zoom=zoom
        )

    with st.sidebar:
        st.title("Device List")

        for device in devices:
            client.ui.location_sidebar(device)
            client.ui.device_sidebar(device)

            for sensor in device.get("sensors", []):
                client.ui.sensor_sidebar(sensor)
            st.divider()

    for device in devices:
        client.ui.location(device)
        client.ui.device(device)

        # Data preview plots
        client.section.data_preview(device)

        # Archive file table
        st.subheader("Archive file table")
        client.widget.table_archive_files(device)

        if "sensors" in device and len(device["sensors"]) == 2:
            # Time series two sensors
            st.subheader("Time series")
            client.section.time_series(device["sensors"], last_days=2)


def template2(
    json_filename: str,
    page_title: str,
    links: dict,
    sticky_device: bool = False,
    sticky_location: bool = False,
):
    """
    template2 is a template for the dashboard of multiple locations that consists of two sections:

    1. Useful links like the Oceans 3.0 Device Console, Oceans 3.0 Annotation, Marine Traffic and Plotting Utility.
    2. List of devices, each having a list of sensors with a time series plot, and optionally some data preview plots,
    which requires non-empty dataPreviewOptions, deviceCategoryId and searchTreeNodeId.

    A sample format for the expected xxx json file is listed below. All are required,
    but dataPreviewOptions, deviceCategoryId and searchTreeNodeId can be empty.
    It is used in the section 2.
    [
          {
            "deviceId": "26099",
            "deviceName": "Sea-Bird SBE 38 (S/N 1048)",
            "sensors": [["29059", "Temperature"]],
            "locationCode": "TWDP",
            "locationName": "Tsawwassen - Duke Point Ferry Route",
            "deviceCode": "SBE381048 in TWDP",
            "searchTreeNodeId": 171,
            "deviceCategoryId": 35,
            "dataPreviewOptions": [[149, 1]]
        },
    ]


    Parameters
    ----------
    json_filename : str
        The name of the JSON file that contains the data. It should have suffix _1.json and _2.json.
    page_title : str
        The title of the page.
    links : dict
        A dictionary of links to be displayed at the top of the page.
        The keys are the link titles, and the values are the URLs.
    sticky_device : bool, default True
        Whether to show the device as sticky in the main part.
    sticky_location : bool, default True
        Whether to show the location as sticky in the sidebar.
    """
    st.set_page_config(layout="wide", page_title=page_title)

    with open(f"pages/{json_filename}.json") as f:
        devices = json.load(f)

    client = ONCDW()

    client.ui.import_custom_badge_css(
        sticky_device=sticky_device, sticky_location=sticky_location
    )

    st.title(f"{page_title} Monitoring Dashboard")

    with st.sidebar:
        client.ui.h2_badge("", "Links", "#links")
        st.divider()

        for device in devices:
            client.section.location_sidebar(device)
            client.ui.device_sidebar(device)
            for sensor in device["sensors"]:
                client.ui.sensor_sidebar(sensor)
            st.divider()

    client.section.links(links)

    for device in devices:
        client.section.location_expander(device)

        client.ui.device(device)

        # data preview
        client.section.data_preview(device)

        # time series
        st.subheader("Time Series plot")
        for sensor in device["sensors"]:
            client.section.time_series(sensor)


def template1(
    json_filename: str,
    location_code: str,
    page_title: str,
    links: dict,
    env: str = "PROD",
    sticky_device: bool = False,
    sticky_location: bool = False,
):
    """
    template1 is a template for the dashboard of only one location that consists of five sections:

    1. Links to the Oceans 3.0 Device Console and Oceans 3.0 Annotation.
    2. Three images: State of Ocean Climate plot, State of Ocean Anomaly plot, and State of Ocean Min/Max plot.
    3. List of devices, each having a list of sensors with a time series plot.
    4. List of double devices, each having a two-sensors time series plot.
    5. List of devices, each having a list of data preview plots and an archive file table.

    A sample format for the expected xxx_1 json file is listed below. All are required.
    It is used in the section 3 and section 4.
    [
        # One-sensor times series plot
        {
            "deviceId": "23580",
            "deviceName": "Sea-Bird SeaCAT SBE19plus V2 7033",
            "sensors": [["15678", "Pressure"]],  # [[sensor id, sensor name]]
            "locationCode": "NC89",
            "locationName": "Bullseye",
            "deviceCode": "SBECTD19p7033",
        },
        # Two-sensors times series plot
        {
            "deviceId": "23840 & 23283",
            "deviceName": "Sea-Bird SeaCAT SBE19plus V2 6002 & Sea-Bird SBE 63 Dissolved Oxygen Sensor 630637",
            # [[[sensor id 1, sensor name 1], [sensor id 2, sensor name 2]]]
            "sensors": [[["16672", "Temperatures"], ["13327", "Temperatures"]]],
            "locationCode": "BACAX",
            "locationName": "Barkley Canyon Axis",
            "deviceCode": "SBECTD19p6002 & SBE63630637",
        }
    ]

    A sample format for the expected xxx_2 json file is listed below.
    All are required except `fileExtensions`. It is used in the section 5.
    [
        {
            "deviceId": "24150",
            "deviceName": "RBRconcerto Tilt Meter ACC.BPR 63055",
            "locationCode": "NC89",
            "locationName": "Bullseye",
            "dataPreviewOptions": [[3, 1], [3, 2]], # [(data_product_format_id, plot_number)]
            "searchTreeNodeId": 1776,
            "deviceCategoryId": 46,
            "deviceCode": "RBRTILTMETERACCBPR63055",
            "fileExtensions": ["txt", "dt4"], # optional
        }
    ]


    Parameters
    ----------
    json_filename : str
        The name of the JSON file that contains the data. It should have suffix _1.json and _2.json.
    location_code : str
        The location code of the devices.
    page_title : str
        The title of the page.
    links : dict
        A dictionary of links to be displayed at the top of the page.
        The keys are the link titles, and the values are the URLs.
    env : str, default "PROD"
        The environment of running the web service. "PROD" or "QA".
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

    client = ONCDW(env=env)

    st.title(f"{page_title} Monitoring Dashboard")

    client.ui.import_custom_badge_css(
        sticky_device=sticky_device, sticky_location=sticky_location
    )

    client.section.links(links)

    state_of_ocean_images_badges = client.section.state_of_ocean_images(location_code)

    with st.sidebar:
        client.ui.h2_badge("", "Links", "#links")

        for key, val, href in state_of_ocean_images_badges:
            client.ui.h2_badge(key, val, href)

        st.divider()

        for device in devices1:
            client.section.location_sidebar(device)
            client.ui.device_sidebar(device)

            for sensor in device["sensors"]:
                client.section.sensor_sidebar(sensor)

            st.divider()

        for device in devices2:
            client.section.location_sidebar(device)

            client.ui.device_sidebar(device)

            st.divider()

    for device in devices1:
        client.section.location_expander(device)
        client.ui.device(device)

        st.subheader("Time Series plot")
        for sensor in device["sensors"]:
            client.section.time_series(sensor)

    for device in devices2:
        client.section.location_expander(device)
        client.ui.device(device)

        # Data preview plots in two columns
        client.section.data_preview(device)

        # Archive file table, only display if deviceCode is present
        if device["deviceCode"]:
            st.subheader("Archive file table")
            client.widget.table_archive_files(device)
