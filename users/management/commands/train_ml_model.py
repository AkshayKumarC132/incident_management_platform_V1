from django.core.management.base import BaseCommand
from users.ml_model import IncidentMLModel
from users.models import Incident

class Command(BaseCommand):
    help = 'Train the ML model for incident recommendations'

    def handle(self, *args, **kwargs):
        ml_model = IncidentMLModel()

        # Load existing incidents from the database
        incidents = Incident.objects.all()

        if incidents.exists():
            print("Building solution recommendation model...")
            ml_model.train(incidents)

            # Save the trained models
            ml_model.save_models()
            print("Models saved successfully.")
        else:
            print("No incidents available for training.")
