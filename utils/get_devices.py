import pandas as pd

def get_devices():
    """
        Returns a list of devices with information from a CSV file
    """
    csv_file_path = "datasets/devices_data_100.csv"
    try:
        df = pd.read_csv(csv_file_path)
         # Correctly map the data to the expected format
        devices = df.to_dict(orient="records")
        return devices
    except FileNotFoundError:
        print(f"Error: Data file not found at {csv_file_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return []