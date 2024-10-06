import pandas as pd
import numpy as np
import pickle
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor

class IncidentMLModel:
    def __init__(self):
        self.solution_model = DecisionTreeClassifier()  # You can choose a different model
        # self.time_model = DecisionTreeClassifier()  # For predicting time if needed
        self.time_model = DecisionTreeRegressor()  # Use a regression model
        
    # def extract_features(self, incident):
    #     # Extract features from the incident
    #     features = {
    #         'device_type': incident.device.device_type,
    #         'severity_level': incident.severity.level,
    #         'resolved': incident.resolved,
    #         'created_at': incident.created_at.timestamp()  # Convert to timestamp
    #         # Add any other features that may be relevant
    #     }
    #     return features
    def extract_features(self, incident):
        # Extract features from the incident
        features = {
            'device_type': incident.device.device_type if incident.device else None,
            'severity_level': incident.severity.level,  # Ensure this matches your training data
            'resolved': incident.resolved,
            'created_at': incident.created_at.timestamp()  # Convert to timestamp
            # Add any other features that may be relevant
        }
        return features

    def prepare_training_data(self, incidents):
        feature_list = []
        y_solution = []
        y_time = []

        for incident in incidents:
            features = self.extract_features(incident)
            feature_list.append(features)
            y_solution.append(incident.recommended_solution)
            y_time.append(incident.predicted_resolution_time)

        df = pd.DataFrame(feature_list)
        df_encoded = pd.get_dummies(df, drop_first=True)  # One-Hot Encoding

        X = df_encoded.values  # Feature matrix
        return X, np.array(y_solution), np.array(y_time)

    def train(self, incidents):
        X, y_solution, y_time = self.prepare_training_data(incidents)
        
        # Fit the solution model
        self.solution_model.fit(X, y_solution)
        # Optionally, fit the time model if required
        self.time_model.fit(X, y_time)

    def save_models(self):
        with open('solution_model.pkl', 'wb') as f:
            pickle.dump(self.solution_model, f)
        with open('time_model.pkl', 'wb') as f:
            pickle.dump(self.time_model, f)

    def load_models(self):
        with open('solution_model.pkl', 'rb') as f:
            self.solution_model = pickle.load(f)
        with open('time_model.pkl', 'rb') as f:
            self.time_model = pickle.load(f)

    def predict_solution(self, incident):
        
        features = self.extract_features(incident)
        print(f"Predicting solution with features: {features}")  # Debugging line
        feature_df = pd.DataFrame([features])
        feature_df_encoded = pd.get_dummies(feature_df, drop_first=True)  # One-Hot Encoding
        prediction = self.solution_model.predict(feature_df_encoded.values)
        print(prediction)
        return prediction[0]  # Return the first prediction

    def predict_time(self, incident):
        features = self.extract_features(incident)
        feature_df = pd.DataFrame([features])
        feature_df_encoded = pd.get_dummies(feature_df, drop_first=True)  # One-Hot Encoding
        prediction = self.time_model.predict(feature_df_encoded.values)
        return prediction[0]  # Return the first prediction
