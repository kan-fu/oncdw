import streamlit as st

from oncdw import ONCDW

client = ONCDW()
client.ui.import_custom_badge_css()

st.info(
    "The only difference between the hX_badges is the parent html tag that wraps the badge, "
    "which can be used to customize its appearance in the css file."
)

with st.echo():
    client.ui.h1_badge("left", "right", "#href_title", "anchor_title")

with st.echo():
    client.ui.h2_badge("left", "right", "#href_header", "anchor_header")

with st.echo():
    client.ui.h3_badge("left", "right", "#href_subheader", "anchor_subheader")

st.info(
    "The XXX_sidebar is a hyperlink to the XXX badge. "
    "The badge itself is a hyperlink to DMAS 3.0."
)
with st.echo():
    location = {
        "locationCode": "CODE",
        "locationName": "Location Name",
    }
    client.ui.location(location)
    client.ui.location_sidebar(location)

with st.echo():
    device = {
        "deviceId": "12345",
        "deviceName": "Device Name",
        "deviceCode": "CODE",
    }
    client.ui.device(device)
    client.ui.device_sidebar(device)

with st.echo():
    sensor = {
        "sensorId": "67890",
        "sensorName": "Sensor Name",
    }
    client.ui.sensor(sensor)
    client.ui.sensor_sidebar(sensor)

with st.echo():
    sensor1 = {
        "sensorId": "167890",
        "sensorName": "Sensor Name 1",
    }
    sensor2 = {
        "sensorId": "267890",
        "sensorName": "Sensor Name 2",
    }
    client.ui.sensors_two(sensor1, sensor2)
    client.ui.sensors_two_sidebar(sensor1, sensor2)
