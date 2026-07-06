from fastapi import Depends, FastAPI
from app.schemas.input_data_schema import InputDataSchema
from contextlib import asynccontextmanager
from app.database.connection import get_db
from sqlalchemy.orm import Session 
import sys
import os
from app.utils.cach import redis_client
from app.services.statistics import get_statistics
from app.utils.rabbitmq import connection, channel
import json
import pika
import uuid

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup Python:", sys.executable)
    try:
        redis_client.ping()
        print("Redis connected successfully.")
    except ConnectionError:
        print("Failed to connect to Redis.")
        raise


    yield
    
    redis_client.close()

    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/redis-test")
def redis_test():
    redis_client.set("test", "connected", ex=60)
    value = redis_client.get("test")
    return {"redis": value}

@app.post("/predict")
def predict(input_data: InputDataSchema):
    """
    Endpoint to predict the output based on the input data.

    """
    job_id = str(uuid.uuid4())
    
    channel.basic_publish(
    exchange="",
    routing_key="prediction_queue",
    body=json.dumps({
        "job_id": job_id,
        "type": "single",
        "data": input_data.dict()
    }).encode()
)
    return {"job_id": job_id, "status": "queued"}

@app.post("/predict-batch")
def predict_batch(input_data_list: list[InputDataSchema]):
    """
    Endpoint to predict the output for a batch of input data.
    """
    job_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange="",
        routing_key="prediction_queue",
        body=json.dumps({
            "job_id": job_id,
            "type": "batch",
            "data": [x.dict() for x in input_data_list]
        }).encode()
    )
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    result = redis_client.get(job_id)

    if not result:
        return {"status": "processing"}

    return json.loads(result)

@app.get("/statistics")
def statistics(db: Session=Depends(get_db)):
    """
    Endpoint to retrieve statistics from the database.
    """
    stats = get_statistics(db_session=db)
    return {"statistics": stats}
