from fastapi import Depends, FastAPI
from app.schemas.input_data_schema import InputDataSchema
from app.utils.model_manager import ModelManager
from app.services.inference import prediction
from contextlib import asynccontextmanager
from app.database.connection import get_db
from sqlalchemy.orm import Session 
import sys
import os
model_manager = ModelManager("rf_model")

bucket = os.getenv("AWS_BUCKET_NAME")
key = os.getenv("AWS_MODEL_KEY")
local_path = os.getenv("AWS_LOCAL_MODEL_PATH")
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup Python:", sys.executable)
    model_manager.load_from_s3(bucket=bucket, key=key, local_path=local_path)

    yield

    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(input_data: InputDataSchema, db: Session=Depends(get_db)):
    """
    Endpoint to predict the output based on the input data.

    """
    pipeline = model_manager.get_pipeline()
    prediction_result = prediction(pipeline=pipeline, input_data=input_data, db_session=db)
    return {"prediction": prediction_result}
