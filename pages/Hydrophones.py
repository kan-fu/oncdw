import json

import streamlit as st

from oncdw import ONCDW

json_filename = "Hydrophones_Devices"
page_title = "Hydrophones Devices"
sticky_device = False
center_lat, center_lon = 49.3, -126.3

st.set_page_config(layout="wide", page_title=page_title)

with open(f"pages/{json_filename}.json") as f:
    devices: dict = json.load(f)

client = ONCDW()

# custom css
client.ui.import_custom_badge_css(sticky_device=sticky_device)

st.title(f"{page_title} Monitoring Dashboard")

client.widget.map(devices, center_lat=center_lat, center_lon=center_lon, zoom=6)

with st.sidebar:
    st.title("Device List")

    for device in devices:
        client.ui.location_sidebar(device)
        client.ui.device_sidebar(device)

        for sensor in device.get("sensors", []):
            client.ui.sensor_sidebar(sensor)
        st.divider()

for device in devices:
    client.section.location_expander(device)
    client.ui.device(device)

    # Heatmap
    client.widget.heatmap_archive_files(device, date_from="-P14D")

    # Data preview plots
    client.section.data_preview(device)

    # Archive file table
    st.subheader("Archive file table")
    client.widget.table_archive_files(device, date_from="-P1D", date_to="-PT23H")
