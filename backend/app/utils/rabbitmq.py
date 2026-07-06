"""import os
import json
import pika

from app.services.inference import prediction, batch_prediction
from app.database.connection import SessionLocal
from app.utils.model_manager import ModelManager
from app.utils.cach import redis_client

pipeline = None
channel = None
connection = None


def init():
    global pipeline, channel, connection

    bucket = os.getenv("AWS_BUCKET_NAME")
    key = os.getenv("AWS_MODEL_KEY")
    local_path = os.getenv("AWS_LOCAL_MODEL_PATH")

    model_manager = ModelManager("rf_model")
    model_manager.load_from_s3(bucket, key, local_path)
    pipeline = model_manager.get_pipeline()

    host = os.getenv("RABBITMQ_HOST")
    port = int(os.getenv("RABBITMQ_PORT"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )

    channel = connection.channel()
    channel.queue_declare(queue="prediction_queue", durable=True)

def get_channel():
    host = os.getenv("RABBITMQ_HOST")
    port = int(os.getenv("RABBITMQ_PORT"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port)
    )

    channel = connection.channel()
    channel.queue_declare(queue="prediction_queue", durable=True)

    return connection, channel
def callback(ch, method, properties, body):
    payload = json.loads(body)

    job_id = payload["job_id"]
    task_type = payload["type"]
    data = payload["data"]

    db = SessionLocal()

    try:
        if task_type == "single":
            result = prediction(
                pipeline=pipeline,
                input_data=data,
                db_session=db
            )
        else:
            result = batch_prediction(
                pipeline=pipeline,
                input_data_list=data,
                db_session=db
            )

        redis_client.set(job_id, json.dumps({"result": result}))
        db.commit()

    except Exception as e:
        db.rollback()
        print("ERROR:", e)

    finally:
        db.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)


# ✅ ENTRY POINT (THIS IS THE KEY FIX)
if __name__ == "__main__":
    init()

    channel.basic_consume(
        queue="prediction_queue",
        on_message_callback=callback
    )

    print("Worker running...")
    channel.start_consuming()"""