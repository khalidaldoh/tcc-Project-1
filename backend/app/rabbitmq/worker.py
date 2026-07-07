from app.rabbitmq.connection import get_connection
import json
from app.services.inference import queue_batch_prediction, queue_prediction
from app.utils.model_manager import ModelManager
import os
from app.database.connection import SessionLocal

model_manager = ModelManager("rf_model")
bucket = os.getenv("AWS_BUCKET_NAME")
key = os.getenv("AWS_MODEL_KEY")
local_path = os.getenv("AWS_LOCAL_MODEL_PATH")
model_manager.load_from_s3(bucket=bucket, key=key, local_path=local_path)


def callback(ch, method, properties, body):

    message = json.loads(body)

    job_id = message["job_id"]
    job_type = message["job_type"]
    payload = message["payload"]

    db_session = SessionLocal()
    try:
        pipeline = model_manager.get_pipeline()
        if job_type == "prediction":
            queue_prediction(pipeline=pipeline, input_data=payload, db_session=db_session,result_id=job_id)
            
        elif job_type == "batch_prediction":
            queue_batch_prediction(pipeline=pipeline, input_data=payload, db_session=db_session,result_ids=job_id)
        ch.basic_ack(
        delivery_tag=method.delivery_tag
        )
    except Exception as e:
        print(
            f"Job {job_id} failed: {e}"
        )
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
 
    finally:
         db_session.close()

def start_worker():

    connection = get_connection()

    try:
        channel = connection.channel()

        channel.queue_declare(
            queue="prediction_queue",
            durable=True
        )

        channel.basic_qos(
            prefetch_count=1
        )

        channel.basic_consume(
            queue="prediction_queue",
            on_message_callback=callback
        )

        print("Worker started...")

        channel.start_consuming()

    except KeyboardInterrupt:
        print("Worker stopped")

    finally:
        connection.close()


