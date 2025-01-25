# import streamlit as st

# st.set_page_config(page_title="Device Health", page_icon="🔧", layout="centered")

# st.title("🔧 Device Health")

# # Retrieve selected device details
# device = st.session_state.get("current_device", None)

# if not device:
#     st.warning("No device selected. Please go back to the main dashboard.")
#     st.stop()

# # Display device information
# st.subheader(f"Device: {device['name']} (ID: {device['device_id']})")
# st.metric("Uptime (%)", f"{device['uptime_percentage']}%")
# st.metric("Health Status", device['status'])

# if device["status"] == "Healthy":
#     st.success("The device is functioning optimally.")
# else:
#     st.error("The device requires maintenance.")


# ////////////////////////////////////////////////////////////////////////////////////////

import streamlit as st
import pandas as pd
import requests

# Endpoint for fetching device data
DEVICES_API = "http://localhost:5000/devices"

# Ensure the page has the right configuration
st.set_page_config(
    page_title="Device Health",
    page_icon="🔍",
    layout="wide"
)

st.title("🛠️ Device Health Details")

# Function to fetch device data
@st.cache_data
def fetch_devices():
    try:
        response = requests.get(DEVICES_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching devices data: {e}")
        return []

# Extract query parameter
query_params = st.query_params 
device_id = query_params.get("device_id", [None])[0]

if not device_id:
    st.error("Device ID not provided in the query parameters.")
else:
    # Fetch all devices
    devices = fetch_devices()

    # Debugging: Display the fetched devices
    st.write("Fetched Devices (for debugging):", devices)

    # Find the specific device by ID
    current_device = next((device for device in devices if device["device_id"] == device_id), None)

    if not current_device:
        st.error(f"No device found with ID: {device_id}")
    else:
        # Display device health details
        st.subheader(f"🔧 {current_device['name']} (ID: {current_device['device_id']})")
        st.metric("Uptime Percentage", f"{current_device['uptime_percentage']}%")
        st.metric("Status", current_device["status"])
        st.metric("Failure Rate", f"{current_device.get('failure_rate', 'N/A')}%")
        st.metric("Average Response Time", f"{current_device.get('avg_response_time', 'N/A')} ms")