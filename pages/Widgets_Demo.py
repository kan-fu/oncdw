import streamlit as st

from oncdw import ONCDW

st.set_page_config(layout="wide")
client = ONCDW()

st.title("ONC Data Web Widgets Demo")

############################################
st.header("Data Preview png data product")
with st.echo():
    device = {"device_category_id": 20, "search_tree_node_id": 172}
    data_preview_options = {"data_product_format_id": 149, "sensor_code_id": 611}
    client.widget.data_preview(device, data_preview_options)

############################################
st.header("Data Preview gif data product")


with st.echo():
    device = {"device_category_id": 65, "search_tree_node_id": 429}
    data_preview_options = {"data_product_format_id": 178}

    client.widget.data_preview(device, data_preview_options)


############################################
st.header(
    "Latest files archived in the data base for a specific device (with hyperlink)"
)

with st.echo():
    client.widget.table_archive_files({"device_code": "BPR_BC"})
    client.widget.table_archive_files(
        {"device_code": "BPR_BC", "file_extensions": ["txt", "csv"]}
    )


############################################
st.header(
    "File types existing in the archive for a specific device (file availability)"
)
with st.echo():
    client.widget.heatmap_archive_files({"device_code": "CODAR25VATK"}, last_days=14)


############################################
st.header("Time series scalar data plot from one sensor")

with st.echo():
    client.widget.time_series({"sensor_id": 4182}, last_days=2)


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
        {"location_code": "BACAX", "device_category_code": "CTD"},
        "salinity,temperature",
    )
