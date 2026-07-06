from app.utils.cach import redis_client
import json
from sqlalchemy import func
from app.database.models import Results
def get_statistics(db_session):
    """
    Retrieves statistics from the database.
    """

    cached = redis_client.get("statistics")
    if cached:
        print("cache hit")
        return json.loads(cached)
    
    print("cache miss")


    normal = (
        db_session.query(func.count(Results.id))
        .filter(Results.predicted_label == "Normal")
        .scalar()
    )
    attack = (
        db_session.query(func.count(Results.id))
        .filter(Results.predicted_label == "Attack")
        .scalar()
    )
    total = normal + attack

    response = {
        "normal": normal,
        "attack": attack,
        "total": total,
    }
    redis_client.set(
        "statistics",
        json.dumps(response),
        ex=3000
    )

    return response
