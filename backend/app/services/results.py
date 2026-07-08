from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.models import PredictionResults


def get_results_by_job_id(job_id: str, db_session: Session):
    """
    Retrieves all prediction result records that share the given job_id.
    - Single prediction jobs return a list with one item.
    - Batch prediction jobs return a list with all records in that batch.
    Raises 404 if no records found for the given job_id.
    """
    records = (
        db_session.query(PredictionResults)
        .filter(PredictionResults.job_id == job_id)
        .order_by(PredictionResults.id.asc())
        .all()
    )
    if not records:
        raise HTTPException(status_code=404, detail=f"No results found for job_id '{job_id}'.")
    return [
        {
            "id": r.id,
            "job_id": r.job_id,
            "created_at": r.created_at,
            "status": r.status,
            "predicted_label": r.predicted_label,
            "confidence": r.confidence,
        }
        for r in records
    ]
