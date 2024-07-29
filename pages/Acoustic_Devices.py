import json

import streamlit as st

from oncdw import ONCDW

json_filename = "Acoustic_Devices"
page_title = "Acoustic Devices"

st.set_page_config(layout="wide", page_title=page_title)

with open(f"pages/{json_filename}.json") as f:
    devices = json.load(f)

client = ONCDW(file=page_title)
client.ui.import_custom_badge_css()
st.title("Acoustic Devices")
client.ui.show_time_difference(client.now)

with st.sidebar:
    st.title("Acoustic Devices")

    prev_location_code = None
    for device in devices:
        if prev_location_code != device["locationCode"]:
            st.divider()
            client.ui.location_sidebar(device)
        client.ui.device_sidebar(device)
        prev_location_code = device["locationCode"]


for device in devices:
    client.ui.location(device)
    client.ui.device(device)
    # Data Preview png
    st.subheader("Data Preview plot")

    ## Data preview plots in two columns
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
