from django.core.management.base import BaseCommand
from users.ml_model import IncidentMLModel
from users.models import Incident

class Command(BaseCommand):
    help = 'Train the ML model for incident recommendations'

    def handle(self, *args, **kwargs):
        ml_model = IncidentMLModel()

        # Load existing incidents from the database
        incidents = Incident.objects.all()
        for incident in incidents:
            if incident.recommended_solution is None or incident.predicted_resolution_time is None:
                print(f"Missing data in incident {incident.id}")

        if incidents.exists():
            incidents = Incident.objects.all()

            # Train the models and save them
            ml_model.train()
            ml_model.save_model()

            print("Models saved successfully.")
        else:
            print("No incidents available for training.")
