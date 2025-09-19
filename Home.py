import streamlit as st
import os
from onc import ONC
import pandas as pd

st.title("Oceans 3.0 Open API Playground")
st.metric("Web Services", 2, 1)

token = os.getenv("ONC_TOKEN")
onc = ONC(token)

with st.sidebar:
    st.markdown("[Discovery Services](#discovery-services)")
    st.markdown("[Real-time Services](#real-time-services)")

# col1, col2 = st.columns(2)
col1, col2 = st.tabs(["Discovery", "Real-time"])

with col1:
    st.header(":blue[Discovery Services]")

    st.subheader(":green[Return locations]")

    st.markdown(":blue-badge[GET] `/locations`")

    location_code = st.text_input("locationCode", placeholder="FGPD")

    if st.button("Run", key="location_button"):
        param = {"locationCode": location_code}
        location_info = onc.getLocations(param)
        st.json(location_info)

with col2:
    st.header(":blue[Real-time Services]")

    st.subheader(":green[Return archivefiles]")

    st.markdown(":blue-badge[GET] `/archivefile`")

    device_code = st.text_input("deviceCode", value="BPR_BC")
    last_days = st.number_input("last days", value=4)

    if st.button("Run", key="archivefile_button"):
        param = {
            "deviceCode": device_code,
            "dateFrom": f"-P{last_days}D",
            "returnOptions": "all",
        }
        archivefile = onc.getArchivefile(param)
        df = pd.DataFrame(archivefile["files"])
        df["dateFrom"] = pd.to_datetime(df["dateFrom"])
        st.line_chart(df, x="dateFrom", y="uncompressedFileSize")
