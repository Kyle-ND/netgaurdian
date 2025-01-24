import pandas as pd
from datetime import datetime

def get_health():
    try:
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

        # GET FAILURE RATE
        failure_data['failure_date'] = pd.to_datetime(failure_data['failure_date'])
        total_failures = len(failure_data)
        total_days_in_service = total_devices * average_uptime
        failures_per_device = total_failures / total_devices
        failure_rate =  failures_per_device / (total_days_in_service / total_devices)

        # GET TRAFFIC LOAD
        traffic_load = total_failures * 10

        # GET OVERALL HEALTH
        overall_health = ""

        if failure_rate < 0.01 and traffic_load < (traffic_load / 2):
            overall_health = "Excellent"
        elif failure_rate < 0.05:
            overall_health = "Good"
        elif failure_rate < 0.10:
            overall_health = "Fair"
        else:
            overall_health = "Poor"

        # MAKE RESPONSE
        response = {
            "total_devices": total_devices,
            "devices_active": devices_active,
            "average_uptime": float(average_uptime),
            "failure_rate": float(failure_rate),
            "traffic_load": traffic_load,
            "overall_health": overall_health
        }

        return response

    except FileNotFoundError as e:
        return {"error": f"File not found: {str(e)}"}
    except pd.errors.EmptyDataError as e:
        return {"error": f"Empty data: {str(e)}"}
    except KeyError as e:
        return {"error": f"Missing expected column(s): {str(e)}"}
    except ValueError as e:
        return {"error": f"Value error: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}