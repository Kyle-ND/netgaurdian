import requests

def send_ntfy_notification(message):
    url = "https://ntfy.sh/device_maintenance_alerts"
    payload = {"message": message}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Notification sent to ntfy.sh")
    else:
        print("Failed to send notification")

