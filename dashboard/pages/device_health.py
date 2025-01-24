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

# Ensure the page has the right configuration
st.set_page_config(
    page_title="Device Health",
    page_icon="🔍",
    layout="wide"
)

# Mock Data: This should match the mocked data in main.py
def mock_device_data():
    return [
        {"device_id": "Device001", "name": "Router A", "uptime_percentage": 95.0, "status": "Healthy"},
        {"device_id": "Device002", "name": "Switch B", "uptime_percentage": 80.0, "status": "Needs Maintenance"},
        {"device_id": "Device003", "name": "Firewall C", "uptime_percentage": 99.0, "status": "Healthy"},
        {"device_id": "Device004", "name": "Access Point D", "uptime_percentage": 70.0, "status": "Needs Maintenance"},
        {"device_id": "Device005", "name": "Modem E", "uptime_percentage": 88.5, "status": "Healthy"},
    ]

# not done with this one
# Function to fetch device by ID
def get_device_by_id(device_id):
    devices = mock_device_data()
    for device in devices:
        if device["device_id"] == device_id:
            return device
    return None

# Main device health page logic
def render_device_health(device_id):
    device = get_device_by_id(device_id)
    if not device:
        st.error("Device not found.")
        return

    st.title(f"🔍 Device Health: {device['name']}")
    st.write(f"**Device ID:** {device['device_id']}")
    st.write(f"**Uptime Percentage:** {device['uptime_percentage']}%")
    st.write(f"**Health Status:** {device['status']}")

    # Conditional visual feedback
    if device["status"] == "Healthy":
        st.success("The device is operating normally.")
    else:
        st.warning("This device needs maintenance. Please schedule a service.")

# Get the device ID from query parameters
query_params = st.query_params()
device_id = query_params.get("device_id", [None])[0]

if device_id:
    render_device_health(device_id)
else:
    st.error("No device selected. Please go back and choose a device.")
