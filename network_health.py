import pandas as pd
from datetime import datetime

def network_health():
    maintenance_logs = pd.read_csv('datasets/maintenance_logs.csv')
    failure_data = pd.read_csv('datasets/failure_data.csv')

    # GET TOTAL DEVICES
    total_devices = maintenance_logs['device_id'].nunique()

    # GET DEVICES THAT ARE ACTIVE - RECENTLY MENTAINED ONES
    recent_date_threshold = datetime.now() - pd.Timedelta(days=90)
    maintenance_logs['maintenance_date'] = pd.to_datetime(maintenance_logs['maintenance_date'])
    devices_active = maintenance_logs[maintenance_logs['maintenance_date'] > recent_date_threshold]['device_id'].nunique()

    # GET AVG UPTIME
    average_uptime = (datetime.now() - maintenance_logs['maintenance_date']).dt.days.mean()

    print(devices_active)

network_health()