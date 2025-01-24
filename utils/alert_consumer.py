ACTIVEMQ_HOST = os.getenv('ACTIVEMQ_HOST')
ACTIVEMQ_PORT = int(os.getenv('ACTIVEMQ_PORT'))
ACTIVEMQ_USER = os.getenv('ACTIVEMQ_USER')
ACTIVEMQ_PASSWORD = os.getenv('ACTIVEMQ_PASSWORD')
ACTIVEMQ_QUEUE = os.getenv('ACTIVEMQ_QUEUE')

def alert_admin_callback(frame):
    """Callback function to handle incoming messages."""
    message = frame.body

    try:
        send_ntfy_notification(message)
    except Exception as e:
        send_ntfy_notification(f"Error processing alert: {e}")

    print(f"Received alert: {message}")

def start_alert_service():
    """Sets up the ActiveMQ connection and starts consuming messages."""
    try:
        conn = Connection([(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
        conn.set_listener('', AlertListener())
        conn.connect(ACTIVEMQ_USER, ACTIVEMQ_PASSWORD, wait=True)
        conn.subscribe(destination=f'/queue/{ACTIVEMQ_QUEUE}', id=1, ack='auto')
        
        while True:
            time.sleep(1)
    except Exception as e:
        send_ntfy_notification(f"Error starting alert service: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.disconnect()

def push_alert_to_queue(message):
    """Pushes an alert message to the ActiveMQ queue."""
    try:
        conn = Connection([(ACTIVEMQ_HOST, ACTIVEMQ_PORT)])
        conn.connect(ACTIVEMQ_USER, ACTIVEMQ_PASSWORD, wait=True)
        conn.send(body=message, destination=f'/queue/{ACTIVEMQ_QUEUE}')
    except Exception as e:
        send_ntfy_notification(f"Error sending alert: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.disconnect()

class AlertListener:
    def on_message(self, frame):
        alert_admin_callback(frame)


def send_ntfy_notification(message):
    url = "https://ntfy.sh/device_maintenance_alerts"
    payload = {"message": message}
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Notification sent to ntfy.sh")
    else:
        print("Failed to send notification")


if __name__ == "__main__":
    start_alert_service()