import os 
import pika

host = os.getenv("RABBITMQ_HOST")
port = os.getenv("RABBITMQ_PORT")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=host,
        port=port
    )
)

channel = connection.channel()

channel.queue_declare(
    queue="prediction_queue",
    durable=True
)

