import json
import re

import streamlit as st

from oncdw import ONCDW


def Barkley(
    json_filename,
    location_code,
    page_title,
    device_name_id,
    device_console_url,
    annotation_url,
    sticky_device=True,
    sticky_location=True,
):
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
