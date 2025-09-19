import streamlit as st

st.title("Oceans 3.0 Open API Playground")


st.header(":blue[Discovery Services]")

st.subheader(":green[Return locations]")

st.markdown(":blue-badge[GET] `/locations`")

location_code = st.text_input("locationCode", placeholder="FGPD")

if st.button("Run", key="location_button"):
    st.write(f"you input {location_code}")

st.divider()

st.header(":blue[Real-time Services]")

st.subheader(":green[Return archivefiles]")

st.markdown(":blue-badge[GET] `/archivefile`")

device_code = st.text_input("deviceCode", value="BPR_BC")
last_days = st.number_input("last days", value=4)

if st.button("Run", key="archivefile_button"):
    st.write(f"you input {device_code}")
    st.write(f"you input {last_days}")
