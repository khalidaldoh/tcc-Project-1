import pandas as pd
from app.database.connection import SessionLocal
from app.database.models import Logs


def load_dataset():
    df = pd.read_csv("ml/dataset_eda/UNSW_NB15_training-set.csv")
    df = df.drop(columns=["id"])
    records = df.to_dict(orient="records")

    session = SessionLocal()

    try:

        session.bulk_insert_mappings(Logs, records)
        session.commit()
        print(f"Inserted {len(records)} records into the database.")
    except Exception as e:
        session.rollback()
        print(f"Error inserting records: {e}")
    finally: 
        session.close()


if __name__ == "__main__":
    load_dataset()