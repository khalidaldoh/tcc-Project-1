import pandas as pd
from app.database.models import PredictionResults
import uuid
def prediction(pipeline ,input_data: dict, db_session):
    """
    Predicts the output based on the input data using the loaded model.

    Args:
        input_data (array-like): The input data for prediction.

    Returns:
        array: The predicted output.
    """
    job_id = str(uuid.uuid4())
    X = pd.DataFrame([input_data])

    prediction_result = int(pipeline.predict(X)[0])
    confidence = pipeline.predict_proba(X)[0].max()

    record = PredictionResults(
        job_id=job_id,
        input_data = input_data,
        predicted_label = prediction_result,
        confidence = float(confidence),
        status = "completed" 
                  )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    print(pipeline.classes_)
    print(pipeline.predict_proba(X)[0])
    label = {"timestamp": record.created_at.isoformat(),
             "Prediction":"attack" if prediction_result == 1 else "normal",
             "label": prediction_result,
             "confidence": float(confidence),}
    return label
    

def batch_prediction(pipeline, input_data_list: list[dict], db_session):
    """
    Predicts the output for a batch of input data using the loaded model.
    """
    X = pd.DataFrame(input_data_list)
    job_id = str(uuid.uuid4())
    prediction_results = pipeline.predict(X)
    proba = pipeline.predict_proba(X)
    confidence = proba.max(axis=1)

    db_records = []
    response = []
    for record, pred, conf in zip(input_data_list, prediction_results, confidence):
        db_records.append(PredictionResults(
            job_id=job_id,
            input_data=record,
            predicted_label=bool(pred),
            confidence = float(conf),
            status = "completed"            
                )
            )

            
        response.append({
             "Prediction":"attack" if int(pred) == 1 else "normal",
             "label": int(pred),
             "confidence": float(conf),
                }
             )
        
    db_session.add_all(db_records)
    db_session.commit()

    
    return response
    

def queue_prediction(pipeline, input_data: dict, db_session, result_id):
    record = db_session.get(PredictionResults, result_id)
    if record is None:
        raise ValueError(f"Result {result_id} not found")
    record.status = "processing"
    db_session.commit()
    X = pd.DataFrame([input_data])
    prediction_result = int(pipeline.predict(X)[0])
    confidence = pipeline.predict_proba(X)[0].max()
    record.predicted_label = bool(prediction_result)
    record.confidence = float(confidence)
    record.status = "completed"

    db_session.commit()


def queue_batch_prediction(pipeline, input_data_list: list[dict], db_session, result_ids):
    for result_id in result_ids:
        record = db_session.get(PredictionResults, result_id)
        if record is None:
            raise ValueError(f"Result {result_id} not found")
        record.status = "processing"
    db_session.commit()
    X = pd.DataFrame(input_data_list)
    prediction_results = pipeline.predict(X)
    proba = pipeline.predict_proba(X)
    confidence = proba.max(axis=1)

    for result_id, pred, conf in zip(
        result_ids,
        prediction_results,
        confidence
    ):
        record = db_session.get(PredictionResults,result_id)
        if record is None:
            raise ValueError(f"Result {result_id} not found")
        record.predicted_label = bool(pred)
        record.confidence = float(conf)
        record.status = "completed"

    db_session.commit()





