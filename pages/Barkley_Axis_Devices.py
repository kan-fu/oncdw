import json
import re

import streamlit as st

from oncdw import ONCDW

json_filename = "Barkley_Axis_Devices"
location_code = "BACAX"
page_title = "Barkley Axis"

st.set_page_config(layout="wide", page_title=page_title)

devices1 = json.load(open(f"pages/{json_filename}_1.json"))
devices2 = json.load(open(f"pages/{json_filename}_2.json"))

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

client = ONCDW(file=__file__)

client.ui.import_custom_badge_css()

st.title(f"{page_title} Devices Monitoring Dashboard")

client.ui.show_time_difference(client.now)

with st.sidebar:
    client.ui.sidebar_header_location(devices1[0])
    client.ui.header_badge("", "Links", "#links")
    for title, _, (key, val) in images:
        # Format "State of Ocean Climate plot" to "state-of-ocean-climate-plot"
        href = "#" + re.sub(r"\W+", "-", title).lower()
        client.ui.header_badge(key, val, href)

    st.title("Device List")

    for device in devices1:
        client.ui.sidebar_header_device(device)
        if "&" not in device["deviceId"]:
            for sensor in device["sensors"]:
                client.ui.sidebar_subheader_sensor(sensor)
        else:
            for sensor1, sensor2 in device["sensors"]:
                client.ui.sidebar_subheader_two_sensors(sensor1, sensor2)
        st.divider()

    for device in devices2:
        client.ui.sidebar_header_device(device)
        st.divider()

# All the devices belong to the same location
client.ui.header_location(devices1[0])
st.header("Links")

st.subheader(
    "[Oceans 3.0 Device Console for OceanWorks Junction Box JB-01 (10515)](https://data.oceannetworks.ca/DC?TREETYPE=10&OBSERVATORY=8&STATION=102&DEVICE=10501&DEVICE=10515&TAB=Device%20Control)"
)

st.subheader(
    "[Oceans 3.0 Annotation for OceanWorks Junction Box JB-01 (10515)](https://data.oceannetworks.ca/AnnotationsV2?sourceFilter=3&sourceFilter=5&resourceFilter.resourceTypeId=1000&resourceFilter.resource.id=10515&resourceFilter.resource.name=OceanWorks%20Junction%20Box%20JB-01%20%2810515%29&resourceFilter.includeTopology=true&fieldFilter)"
)

for title, url, _ in images:
    st.header(title)
    st.image(url)


for device in devices1:
    client.ui.header_device(device)
    if "&" not in device["deviceId"]:
        for sensor in device["sensors"]:
            client.ui.subheader_sensor(sensor)
            client.widget.time_series(sensor)
    else:
        for sensor1, sensor2 in device["sensors"]:
            client.ui.subheader_two_sensors(sensor1, sensor2)
            client.widget.time_series_two_sensors(sensor1, sensor2)


for device in devices2:
    client.ui.header_device(device)
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
