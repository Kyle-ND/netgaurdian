import pandas as pd

def get_devices():
    """
        Returns a list of devices with information from a CSV file
    """
    csv_file_path = "datasets/devices_data_100.csv"
    try:
        df = pd.read_csv(csv_file_path)
         # Correctly map the data to the expected format
        devices = df.apply(lambda row: {
                "device_id": f"Device{row['device_id']}",
                "name": f"Device {row['device_id']}",
                "uptime_percentage": round((1 - row['failure_count'] / row['days_in_service'])*100, 2) if row['days_in_service'] > 0 else 0 ,
                "status": "Healthy" if row['failure_count'] < (row['days_in_service'] / 100) else "Needs Maintenance"
            }, axis=1).to_list()
        return devices
    except FileNotFoundError:
        print(f"Error: Data file not found at {csv_file_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return []