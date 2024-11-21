from confluent_kafka import Producer
from datetime import datetime
import json

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'insurance-api'
}

producer = Producer(KAFKA_CONFIG)


def send_log_message(user_id: int, action: str, timestamp: datetime):
    message = {
        "user_id": user_id,
        "action": action,
        "timestamp": timestamp.isoformat()
    }
    producer.produce('insurance-logs', key=str(user_id), value=json.dumps(message))
    producer.flush()
