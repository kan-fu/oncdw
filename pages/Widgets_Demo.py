import streamlit as st

from oncdw import ONCDW

st.set_page_config(layout="centered")
client = ONCDW(file=__file__)

st.title("ONC Data Web Widgets Demo")

############################################
st.header("Data Preview png data product")
with st.echo():
    device = {"deviceCategoryId": 20, "searchTreeNodeId": 172}
    sensor = {"sensorCodeId": 611}
    client.widget.data_preview(device, data_product_format_id=149, sensor=sensor)

############################################
st.header("Data Preview gif data product")


with st.echo():
    device = {"deviceCategoryId": 65, "searchTreeNodeId": 429}

    client.widget.data_preview(device, data_product_format_id=178)
    client.widget.data_preview(device, data_product_format_id=261)


############################################
st.header(
    "Latest files archived in the data base for a specific device (with hyperlink)"
)

with st.echo():
    # client.widget.table_archive_files({"deviceCode": "BPR_BC"})
    client.widget.table_archive_files("BPR_BC")


############################################
st.header(
    "File types existing in the archive for a specific device (file availability)"
)
with st.echo():
    client.widget.heatmap_archive_files({"deviceCode": "CODAR25VATK"}, last_days=14)
    # client.widget.heatmap_archive_files("CODAR25VATK", last_days=14)


############################################
st.header("Time series scalar data plot from one sensor")

with st.echo():
    client.widget.time_series(7684, last_days=2)
    # client.widget.time_series({"sensorId": 7684}, last_days=2)


############################################
st.header("Time series scalar data plot with two sensors of the same type")

with st.echo():
    client.widget.time_series_two_sensors(4182, 7712, last_days=2)


############################################
st.header("Time series scalar data plot with two sensors of different type")

with st.echo():
    client.widget.time_series_two_sensors(4176, 3016, last_days=2)


############################################
st.header("Scalar data plot with two sensors of different type on separate axis")
with st.echo():
    client.widget.scatter_plot_two_sensors(
        {"locationCode": "BACAX", "deviceCategoryCode": "CTD"},
        "salinity,temperature",
    )
