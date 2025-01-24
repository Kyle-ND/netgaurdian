import pika
import ntfy
import logging
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv('RABBITMQ_URL')
NTFY_TOPIC = os.getenv('NTFY_TOPIC')

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def alert_admin_callback(ch, method, properties, body):
    """Callback function to handle incoming messages."""
    message = body.decode('utf-8')
    logging.info(f"Received alert: {message}")

    try:
        ntfy.publish(topic=NTFY_TOPIC,message=message,
                        title="PC Maintenance Alert",
                        priority="high")
        logging.info("Sent notification using ntfy.")
    except Exception as e:
        logging.error(f"Error sending ntfy notification: {e}")


def start_alert_service():
    """Sets up the RabbitMQ connection and starts consuming messages."""
    try:
        url = urllib.parse.urlparse(RABBITMQ_URL)
        credentials = pika.PlainCredentials(url.username, url.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=url.hostname,port=url.port,
                                        virtual_host=url.path[1:],
                                        credentials=credentials))

        channel = connection.channel()
        channel.queue_declare(queue=url.path[1:])

        channel.basic_consume(queue=url.path[1:],
                                on_message_callback=alert_admin_callback,
                                auto_ack=True)
        logging.info("Waiting for alerts...")
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Error consuming from queue: {e}")
    finally:
        if 'connection' in locals() and connection and connection.is_open:
            connection.close()


if __name__ == "__main__":
    start_alert_service()