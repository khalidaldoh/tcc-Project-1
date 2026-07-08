from fastapi import Depends, FastAPI
from app.schemas.input_data_schema import InputDataSchema
from app.utils.model_manager import ModelManager
from app.services.inference import prediction, batch_prediction
from contextlib import asynccontextmanager
from app.database.connection import get_db
from sqlalchemy.orm import Session 
import sys
import os
import uuid
from app.utils.cach import redis_client
from app.services.statistics import get_statistics
from app.rabbitmq.connection import get_connection
from app.rabbitmq.producer import publish_prediction
from app.database.models import PredictionResults
model_manager = ModelManager("rf_model")
bucket = os.getenv("AWS_BUCKET_NAME")
key = os.getenv("AWS_MODEL_KEY")
local_path = os.getenv("AWS_LOCAL_MODEL_PATH")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """    print("Startup Python:", sys.executable) 
    model_manager.load_from_s3(bucket=bucket, key=key, local_path=local_path)
    try:
       redis_client.ping()
       print("Redis connected successfully.")
    except ConnectionError:
        print("Failed to connect to Redis.")
        raise"""
    yield
    """    redis_client.close()
    print("Application is shutting down...")"""

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tests/redis-test")
def redis_test():
    redis_client.set("test", "connected", ex=60)
    value = redis_client.get("test")
    return {"redis": value}


@app.post("/without_queue/predict")
def predict(input_data: InputDataSchema, db: Session=Depends(get_db)):
    """
    Endpoint to predict the output based on the input data.
    """
    pipeline = model_manager.get_pipeline()
    prediction_result = prediction(pipeline=pipeline, input_data=input_data.model_dump(), db_session=db)
    redis_client.delete("statistics")
    return {"prediction": prediction_result}

@app.post("/without_queue/predict-batch")
def predict_batch(input_data_list: list[InputDataSchema], db: Session=Depends(get_db)):
    """
    Endpoint to predict the output for a batch of input data.
    """
    pipeline = model_manager.get_pipeline()
    prediction_results = batch_prediction(pipeline=pipeline,
                         input_data_list=[record.model_dump() for record in input_data_list],
                           db_session=db)
    redis_client.delete("statistics")
    return {"predictions": prediction_results}

@app.post("/with_queue/predict")
def queued_predict(input_data: InputDataSchema,db: Session=Depends(get_db)):
    """
    Endpoint to predict the output based on the input data with queue.
    """
    record = PredictionResults(
        input_data=input_data.model_dump(),
        status="queued"
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    publish_prediction(job_id=record.id,job_type="prediction", payload= input_data.model_dump())
    return {
    "job_id": record.id,
    "status": "queued"
    }
    
@app.post("/with_queue/predict_batch")
def queued_predict_batch(input_data_list: list[InputDataSchema],db: Session=Depends(get_db)):
    """
    Endpoint to predict the output for a batch of input data with queue
    """
    records = []
    for item in input_data_list:
        records.append(
            PredictionResults(
                input_data=item.model_dump(),
                status="queued"
            )
        )

    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    publish_prediction(job_id=[record.id for record in records],job_type= "batch_prediction",
                        payload= [record.model_dump() for record in input_data_list])   

    return {
    "job_id": [record.id for record in records],
    "status": "queued"
    }

@app.get("/statistics")
def statistics(db: Session=Depends(get_db)):
    """
    Endpoint to retrieve statistics from the database.
    """
    stats = get_statistics(db_session=db)
    return {"statistics": stats}
