# tasks.py

from .ml_model import IncidentMLModel
from .models import Incident

def retrain_model():
    # Fetch all incidents
    incidents = Incident.objects.all()

    # # Check if there are enough incidents to retrain
    # if incidents.count() < 10:  # Or any minimum threshold you choose
    #     print("Not enough incidents for retraining.")
    #     return

    # Initialize the model
    model = IncidentMLModel()

    # Train the model with the incidents
    try:
        model.train(incidents)
        model.save_models()
        print("Models retrained and saved successfully.")
    except Exception as e:
        print(f"An error occurred during retraining: {e}")
