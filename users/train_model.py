# train_model.py

import numpy as np
from ml_model import IncidentMLModel
from .models import Incident
import pandas as pd

def load_training_data():
    # """
    # Placeholder for loading and preparing the dataset for training.
    # This function should return:
    # - X: the features (incident details)
    # - y_solution: the target for solution recommendation (categorical labels)
    # - y_time: the target for resolution time prediction (numerical values)
    # """
    # print("Loading training data...")
    # TODO: Add code here to load your training data from the database, CSV, etc.
    # X = np.random.rand(100, 5)  # Example feature matrix
    # y_solution = np.random.choice([0, 1, 2], size=(100,))  # Example solution labels
    # y_time = np.random.rand(100) * 10  # Example time to resolution in hours
    # return X, y_solution, y_time
    incidents = Incident.objects.all()
    X = []
    y_solution = []
    y_time = []
    
    for incident in incidents:
        features = {
            'device_type': incident.device.device_type if incident.device else None,
            'severity_level': incident.severity.level,
            'resolved': incident.resolved,
            'created_at': incident.created_at.timestamp()
        }
        X.append(features)
        y_solution.append(incident.recommended_solution)
        y_time.append(incident.predicted_resolution_time)
    
    df = pd.DataFrame(X)
    df = pd.get_dummies(df, drop_first=True)  # Handle categorical features
    return df.values, np.array(y_solution), np.array(y_time)


def main():
    # Load training data
    X, y_solution, y_time = load_training_data()

    # Initialize the ML model handler
    ml_model = IncidentMLModel()

    # Train the models
    ml_model.train(X, y_solution, y_time)

    # Save the trained models
    ml_model.save_model('solution_model.pkl', 'time_model.pkl')

if __name__ == "__main__":
    main()
