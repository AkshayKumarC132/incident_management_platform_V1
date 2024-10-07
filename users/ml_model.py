import pandas as pd
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from users.models import Incident, Device, Severity  # Import your actual Django models

class IncidentMLModel:
    def __init__(self):
        self.solution_model = DecisionTreeClassifier()
        self.time_model = DecisionTreeRegressor()

    def extract_features(self, incident):
        """Extract features from the incident object."""
        if not isinstance(incident, Incident):
            raise ValueError("Expected an instance of Incident.")

        # Ensure created_at is a datetime object and calculate timestamp
        created_at_timestamp = incident.created_at.timestamp() if incident.created_at else None

        features = {
            'hour': incident.created_at.hour if incident.created_at else None,
            'day_of_week': incident.created_at.weekday() if incident.created_at else None,
            'device_type': incident.device.device_type if incident.device else None,
            'severity': incident.severity.level,
            'is_weekend': 1 if (incident.created_at and incident.created_at.weekday() >= 5) else 0,
            'resolved': incident.resolved,
            'created_at': created_at_timestamp
        }

        return features

    def prepare_new_incident_df(self, incident, device):
        """Prepare a DataFrame for a new incident."""
        if not isinstance(incident, Incident) or not isinstance(device, Device):
            raise ValueError("Expected instances of Incident and Device.")

        new_incident = {
            'hour': incident.created_at.hour,
            'day_of_week': incident.created_at.weekday(),
            'device_type': device.device_type,
            'severity': incident.severity.level,
            'is_weekend': 1 if incident.created_at.weekday() >= 5 else 0,
            'resolved': incident.resolved,
            'created_at': incident.created_at.timestamp() if incident.created_at else None
        }

        # Convert to DataFrame
        new_incident_df = pd.DataFrame([new_incident])
        return new_incident_df

    def prepare_training_data(self, incidents):
        """Prepare training data from a list of incidents."""
        feature_list = []
        y_solution = []
        y_time = []

        for incident in incidents:
            features = self.extract_features(incident)
            feature_list.append(features)

            # Append target values if not None
            if incident.recommended_solution is not None and incident.predicted_resolution_time is not None:
                y_solution.append(incident.recommended_solution)
                y_time.append(incident.predicted_resolution_time)

        # Ensure we have matching lengths
        if len(y_solution) == 0 or len(y_time) == 0:
            raise ValueError("No valid training data available. Ensure that incidents have recommended solutions and predicted resolution times.")

        # Create DataFrame and one-hot encode features
        df_encoded = pd.get_dummies(pd.DataFrame(feature_list), drop_first=True)
        X = df_encoded.values  # Feature matrix

        # Ensure that the number of samples in y_solution and y_time match the number of samples in X
        if len(y_solution) != len(X) or len(y_time) != len(X):
            raise ValueError("Mismatch between features and target values.")

        return X, np.array(y_solution), np.array(y_time)

    def train(self, incidents):
        """Train both models using the provided incidents."""
        X, y_solution, y_time = self.prepare_training_data(incidents)

        # Fit both models
        self.solution_model.fit(X, y_solution)
        self.time_model.fit(X, y_time)

    def save_models(self):
        """Save the trained models to disk."""
        with open('solution_model.pkl', 'wb') as f:
            pickle.dump(self.solution_model, f)
        with open('time_model.pkl', 'wb') as f:
            pickle.dump(self.time_model, f)

    def load_models(self):
        """Load the trained models from disk."""
        with open('solution_model.pkl', 'rb') as f:
            self.solution_model = pickle.load(f)
        with open('time_model.pkl', 'rb') as f:
            self.time_model = pickle.load(f)

    def predict_solution(self, incident):
        """Predict the solution for a given incident."""
        features = self.extract_features(incident)
        feature_df_encoded = pd.get_dummies(pd.DataFrame([features]), drop_first=True)

        # Reindex to ensure the columns match the training data
        feature_df_encoded = feature_df_encoded.reindex(columns=self.get_model_feature_columns(self.solution_model), fill_value=0)

        prediction = self.solution_model.predict(feature_df_encoded.values)
        return prediction[0]

    def predict_time(self, incident):
        """Predict the resolution time for a given incident."""
        features = self.extract_features(incident)
        feature_df_encoded = pd.get_dummies(pd.DataFrame([features]), drop_first=True)

        # Reindex to ensure the columns match the training data
        feature_df_encoded = feature_df_encoded.reindex(columns=self.get_model_feature_columns(self.time_model), fill_value=0)
        print("feature_df_encoded",feature_df_encoded)
        prediction = self.time_model.predict(feature_df_encoded.values)
        print("Predictions",prediction)
        return prediction[0]

    def get_model_feature_columns(self, model):
        """Get the feature columns used by the model."""
        if hasattr(model, 'tree_'):
            return model.feature_importances_.tolist()
        else:
            return []  # Adjust according to your models
