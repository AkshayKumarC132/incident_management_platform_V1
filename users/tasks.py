# tasks.py

from .ml_model import IncidentMLModel
from .models import Incident

def retrain_model():
    # Initialize the model
    model = IncidentMLModel()

    # Train the model with the incidents
    try:
        model.train()
        model.save_model()
        print("Models retrained and saved successfully.")
    except Exception as e:
        print(f"An error occurred during retraining: {e}")
