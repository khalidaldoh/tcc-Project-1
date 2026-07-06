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
    data = {
        "proto": input_data.proto,
        "service": input_data.service,
        "state": input_data.state,
        "dur": input_data.dur,
        "spkts": input_data.spkts,
        "dpkts": input_data.dpkts,
        "sbytes": input_data.sbytes,
        "dbytes": input_data.dbytes,
        "rate": input_data.rate,
        "sttl": input_data.sttl,
        "dttl": input_data.dttl,
        "sload": input_data.sload,
        "dload": input_data.dload,
        "sloss": input_data.sloss,
        "dloss": input_data.dloss,
        "sinpkt": input_data.sinpkt,
        "dinpkt": input_data.dinpkt,
        "sjit": input_data.sjit,
        "djit": input_data.djit,
        "swin": input_data.swin,
        "stcpb": input_data.stcpb,
        "dtcpb": input_data.dtcpb,
        "dwin": input_data.dwin,
        "tcprtt": input_data.tcprtt,
        "synack": input_data.synack,
        "ackdat": input_data.ackdat,
        "smean": input_data.smean,
        "dmean": input_data.dmean,
        "trans_depth": input_data.trans_depth,
        "response_body_len": input_data.response_body_len,
        "ct_srv_src": input_data.ct_srv_src,
        "ct_state_ttl": input_data.ct_state_ttl,
        "ct_dst_ltm": input_data.ct_dst_ltm,
        "ct_src_dport_ltm": input_data.ct_src_dport_ltm,
        "ct_dst_sport_ltm": input_data.ct_dst_sport_ltm,
        "ct_dst_src_ltm": input_data.ct_dst_src_ltm,
        "is_ftp_login": input_data.is_ftp_login,
        "ct_ftp_cmd": input_data.ct_ftp_cmd,
        "ct_flw_http_mthd": input_data.ct_flw_http_mthd,
        "ct_src_ltm": input_data.ct_src_ltm,
        "ct_srv_dst": input_data.ct_srv_dst,
        "is_sm_ips_ports": input_data.is_sm_ips_ports,
    }

    X = pd.DataFrame([data])

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
             "confidence": confidence,}
    return label
    






