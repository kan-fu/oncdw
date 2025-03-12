import json

import streamlit as st

from oncdw import ONCDW

json_filename = "Accelerometer_Devices"
page_title = "Accelerometer and Tiltmeter"

st.set_page_config(layout="wide", page_title=page_title)

with open(f"pages/{json_filename}.json") as f:
    devices = json.load(f)

client = ONCDW(file=page_title)

# custom css
client.ui.import_custom_badge_css(sticky_device=True)

st.title("Accelerometer Monitoring Dashboard")
client.ui.show_time_difference(client.now)


client.widget.map(devices)

with st.sidebar:
    st.title("Device List")

    for device in devices:
        client.ui.location_sidebar(device)
        client.ui.device_sidebar(device)
        for sensor in device["sensors"]:
            client.ui.sensor_sidebar(sensor)
        st.divider()


for device in devices:
    client.ui.location(device)
    client.ui.device(device)


    # Archive file table
    st.subheader("Archive file table")
    client.widget.table_archive_files(device)

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
