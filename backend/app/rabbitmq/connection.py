import os
import json
import pika
from app.services.inference import prediction, batch_prediction
from app.database.connection import SessionLocal
from app.utils.model_manager import ModelManager
from app.utils.cach import redis_client


def get_connection():
    host = os.getenv("RABBITMQ_HOST")
    port = os.getenv("RABBITMQ_PORT")

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = host,
                port = port
            )
        )

        return connection
    except Exception as e:
        print(f"RabbitMQ connection error: {e}")
        return None
