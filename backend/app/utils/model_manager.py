from pathlib import Path
import joblib
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
        
    def get_pipeline(self):
        return self.pipeline


