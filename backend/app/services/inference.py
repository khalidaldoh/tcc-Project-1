import joblib
from sklearn import pipeline 
from app.schemas.input_data_schema import InputDataSchema
import pandas as pd
from app.database.models import Results
def prediction(pipeline ,input_data: InputDataSchema, db_session):
    """
    Predicts the output based on the input data using the loaded model.

    Args:
        input_data (array-like): The input data for prediction.

    Returns:
        array: The predicted output.
    """
    data = [input_data.model_dump()]

    X = pd.DataFrame(data)

    prediction_result = int(pipeline.predict(X)[0])
    confidence = pipeline.predict_proba(X)[0].max()
    record = Results(
        input_data = data,
        predicted_label = prediction_result,
        confidence = float(confidence)
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
    

def batch_prediction(pipeline, input_data_list: list[InputDataSchema], db_session):
    """
    Predicts the output for a batch of input data using the loaded model.
    """
    data = [record.model_dump() for record in input_data_list]
    X = pd.DataFrame(data)

    prediction_results = pipeline.predict(X)
    proba = pipeline.predict_proba(X)
    confidence = proba.max(axis=1)

    db_records = []
    response = []
    for record, pred, conf in zip(input_data_list, prediction_results, confidence):
        db_records.append(Results(
            input_data=record.model_dump(),
            predicted_label=bool(pred),
            confidence=float(conf)
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
    




