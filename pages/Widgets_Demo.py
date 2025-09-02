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
    client.widget.table_archive_files({"device_code": "BPR_BC"}, date_from="-P7D")
    client.widget.table_archive_files(
        {"device_code": "ICLISTENHF6093", "file_extensions": ["flac"]},
        date_from="-P1D",
        date_to="-PT23H",
    )


############################################
st.header(
    "File types existing in the archive for a specific device (file availability)"
)
with st.echo():
    client.widget.heatmap_archive_files(
        {"device_code": "CODAR25VATK"}, date_from="-P7D"
    )


############################################
st.header("Time series scalar data plot from one sensor")

with st.echo():
    client.widget.time_series({"sensor_id": 4182}, date_from="-P2D")


############################################
st.header("Time series scalar data plot with two sensors of the same type")

with st.echo():
    client.widget.time_series_two_sensors(4182, 7712, date_from="-P2D")


############################################
st.header("Time series scalar data plot with two sensors of different type")

with st.echo():
    client.widget.time_series_two_sensors(4176, 3016, date_from="-P2D")


############################################
st.header("Scalar data plot with two sensors of different type on separate axis")
with st.echo():
    client.widget.scatter_plot_two_sensors(
        {"location_code": "BACAX", "device_category_code": "CTD"},
        "salinity,temperature",
        date_from="-P1D",
    )

############################################
st.header("Map widget")
with st.echo():
    devices = [
        {
            "lat": 48.314627,
            "lon": -126.058106,
            "locationName": "Location X",
            "locationCode": "LocX",
        },
        {
            "lat": 50.54427,
            "lon": -126.84264,
            "locationName": "Location Y",
            "locationCode": "LocY",
        },
    ]
    # Hover over the point to show the tooltip
    client.widget.map(devices, zoom=6)
