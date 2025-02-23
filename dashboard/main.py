import streamlit as st
import requests
import pandas as pd

# Replace with the actual API endpoints
Deployed_API = "https://netgaurdian-3f80.onrender.com"
Test_API = "http://localhost:5000"
NETWORK_HEALTH_API = f"{Deployed_API}/network-health" # Update the URL to match your Flask API
DEVICES_API = f"{Deployed_API}/devices"
PREDICT_MAINTENANCE_API = f"{Deployed_API}/predict-maintenance"


st.set_page_config(
    page_title="Connectivity Health Monitoring Dashboard",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Connectivity Health Monitoring Dashboard")
st.write("Monitor your network devices and proactively address issues.")


# Fetch data from the network health API
@st.cache_data
def fetch_network_health():
    try:
        print(f"Fetching network health from: {NETWORK_HEALTH_API}")
        response = requests.get(NETWORK_HEALTH_API)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()
        return response.json()  # This will be the health data from your Flask app
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching network health data: {e}")
        return {}

# Fetch data from the devices API
@st.cache_data
def fetch_devices():
    try:
        print(f"Fetching devices from: {DEVICES_API}")
        response = requests.get(DEVICES_API)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()
        return response.json()  # This will be the devices data from your Flask app
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching devices data: {e}")
        return {}

# Fetch data
health_data = fetch_network_health()
devices_data = fetch_devices()


# Metrics Section
st.subheader("📊 Network Metrics")
if health_data:
    total_devices = health_data.get("total_devices", 0)
    devices_active = health_data.get("devices_active", 0)
    average_uptime = health_data.get("average_uptime", 0)
    failure_rate = health_data.get("failure_rate", 0)
    traffic_load = health_data.get("traffic_load", 0)
    overall_health = health_data.get("overall_health", "Unknown")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌐 Total Devices", total_devices)
    col2.metric("✅ Active Devices", devices_active)
    col3.metric("⚙️ Avg. Uptime (Days)", f"{average_uptime:.2f} days")
    col4.metric("⚠️ Failure Rate", f"{failure_rate:.2f}%")

    st.subheader("🛠️ Network Health Overview")
    st.write(f"**Traffic Load:** {traffic_load} requests/day")
    st.write(f"**Overall Health:** {overall_health}")

# Device List Section
st.subheader("📋 Device List")
if devices_data:
    device_df = pd.DataFrame(devices_data)

    # Initialize session state variables for pagination
    if 'page' not in st.session_state:
        st.session_state.page = 0  # Start at the first page
    if 'devices_per_page' not in st.session_state:
        st.session_state.devices_per_page = 5  # Display 5 devices per page

    # Get the devices for the current page
    start_idx = st.session_state.page * st.session_state.devices_per_page
    end_idx = start_idx + st.session_state.devices_per_page
    devices_to_display = device_df.iloc[start_idx:end_idx]

    
    # Display devices in the current page
    for _, device in devices_to_display.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.text(f"🔧 Device {device['device_id']%1000} (ID: {device['device_id']})")
        col2.text(f"Uptime: {device['average_usage']}%")
        
        if col3.button("View Health", key=device['device_id']):
            # Filter and prepare device data for the API request
            
            device_data = {
                "device_id": device["device_id"],
                "time_since_last_maintenance": device["time_since_last_maintenance"],
                "average_usage": device["average_usage"],
                "failure_count": device["failure_count"],
                }
            try:
                # Send device data to predict-maintenance endpoint
                response = requests.post(PREDICT_MAINTENANCE_API, json=device_data)
                response.raise_for_status()
                
                # Parse and display the prediction result
                prediction = response.json().get('result')
                if prediction['maintenance_required']:
                    st.warning(f"Device {prediction['device_id']} might require maintenance")
                else:
                    st.success(f"Device healthy")
            except requests.exceptions.RequestException as e:
                st.error(f"Error predicting maintenance: {e}")

    # Pagination buttons
    num_pages = len(device_df) // st.session_state.devices_per_page
    if len(device_df) % st.session_state.devices_per_page != 0:
        num_pages += 1  # To account for the remainder page

    st.write(f"Page {st.session_state.page + 1} of {num_pages}")
    pagination_col1, pagination_col2 = st.columns([1, 1])
    with pagination_col1:
        if st.session_state.page > 0:
            if st.button("Previous", key="prev"):
                st.session_state.page -= 1
    with pagination_col2:
        if st.session_state.page < num_pages - 1:
            if st.button("Next", key="next"):
                st.session_state.page += 1

else:
    st.write("No device data available.")
