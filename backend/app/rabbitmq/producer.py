from app.rabbitmq.connection import get_connection
import json
import pika
def publish_prediction(job_id: str, job_type:str, payload: dict | list[dict]):
    try:
        connection = get_connection()
        channel = connection.channel()

        channel.queue_declare(
            queue = "prediction_queue",
            durable= True,
        )

        message = {
            "job_id":job_id,
            "job_type":job_type,
            "payload":payload
        }


        body = json.dumps(message)

        channel.basic_publish(
            exchange = "",
            routing_key = "prediction_queue",
            body = body,
            properties=pika.BasicProperties(
            delivery_mode=2)
        )
    except Exception as e :
        print(f"Exception {e}")
        raise e
    finally:
        connection.close()




