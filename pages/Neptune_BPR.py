import json

import streamlit as st

from oncdw import ONCDW

st.set_page_config(layout="wide", page_title="Neptune BPR")
# custom css


devices = json.load(open("pages/Neptune_BPR.json"))

client = ONCDW()

client.ui.import_custom_badge_css()

st.title("Neptune BPR Monitoring Dashboard")
client.ui.show_time_difference(client.now)

client.widget.map(devices)

with st.sidebar:
    st.title("Device List")

    for device in devices:
        client.ui.sidebar_header_location(device)
        client.ui.sidebar_header_device(device)
        for sensor in device["sensors"]:
            client.ui.sidebar_subheader_sensor(sensor)
        st.divider()


for device in devices:
    client.ui.header_location(device)
    client.ui.header_device(device)
    # Data Preview png
    st.subheader("Data Preview plot")
    col1, col2 = st.columns(2)
    with col1:
        client.widget.data_preview(device, 3, plot_number=1)
    with col2:
        client.widget.data_preview(device, 3, plot_number=2)

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
        client.ui.subheader_sensor(sensor1)
    with col2:
        client.ui.subheader_sensor(sensor2)

    client.widget.time_series_two_sensors(sensor1, sensor2, last_days=2)
