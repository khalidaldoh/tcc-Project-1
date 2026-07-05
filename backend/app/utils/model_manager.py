from pathlib import Path
import joblib
import boto3

class ModelManager():

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.pipeline = None

    def load_pipeline(self):
        """
        Loads the model from the specified path.
        """
        
        try:
            MODEL_PATH = 'app/saved_models/rf_model.joblib'
            self.pipeline = joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
        
    def load_from_s3(self, bucket:str, key:str, local_path:str ):
        """
        Loads the model from S3 
        """
        try:
            local_path = Path(local_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)

            s3 = boto3.client("s3")

            s3.download_file(bucket, key, str(local_path))

            self.pipeline = joblib.load(local_path)
            
        except Exception as e:
            print(f"Error loading model from S3: {e}")
            return None


    def get_pipeline(self):
        return self.pipeline


