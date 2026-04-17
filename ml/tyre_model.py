import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


class TyreDegradationModel:
    def __init__(self):
        self.model = None

    def prepare_data(self, laps):
        """
        Prepare tyre degradation dataset
        """

        # CLEAN DATA
        laps = laps.dropna(subset=["LapTime", "Compound"])
        laps = laps[laps["PitOutTime"].isna()]  

        # Convert lap time
        laps["lap_time_sec"] = laps["LapTime"].dt.total_seconds()

        # Sort correctly
        laps = laps.sort_values(by=["Driver", "Stint", "LapNumber"])

        # Tyre age
        laps["tyre_age"] = laps.groupby(["Driver", "Stint"]).cumcount()

        # FIXED BASELINE (FASTEST LAP IN STINT)
        laps["base_lap"] = laps.groupby(["Driver", "Stint"])["lap_time_sec"].transform("min")

        # Degradation
        laps["lap_delta"] = laps["lap_time_sec"] - laps["base_lap"]

        # Encode compound
        compound_map = {
            "SOFT": 0,
            "MEDIUM": 1,
            "HARD": 2,
            "INTERMEDIATE": 3,
            "WET": 4
        }
        laps["compound_encoded"] = laps["Compound"].map(compound_map)

        # ADD CONTEXT FEATURES
        laps["lap_number"] = laps["LapNumber"]

        laps["track_temp"] = laps.get("TrackTemp", np.nan)
        laps["air_temp"] = laps.get("AirTemp", np.nan)

        laps["track_temp"] = laps["track_temp"].fillna(laps["track_temp"].mean())
        laps["air_temp"] = laps["air_temp"].fillna(laps["air_temp"].mean())

        # Drop invalid
        laps = laps.dropna(subset=["compound_encoded", "lap_delta"])
        return laps

    def train(self, laps_df):
        """
        Train tyre degradation model
        """
        df = self.prepare_data(laps_df)

        # FEATURES 
        X = df[[
            "compound_encoded",
            "tyre_age",
            "lap_number",
            "track_temp",
            "air_temp"
        ]]

        y = df["lap_delta"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = xgb.XGBRegressor(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )

        self.model.fit(X_train, y_train)
        preds = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        print(f"\n Tyre Model MAE: {mae:.2f} sec")

        return self.model

    def predict(self, compound, tyre_age, lap_number=10, track_temp=35, air_temp=25):
        """
        Predict degradation
        """

        compound_map = {
            "SOFT": 0,
            "MEDIUM": 1,
            "HARD": 2,
            "INTERMEDIATE": 3,
            "WET": 4
        }

        X = pd.DataFrame([{
            "compound_encoded": compound_map.get(compound, 1),
            "tyre_age": tyre_age,
            "lap_number": lap_number,
            "track_temp": track_temp,
            "air_temp": air_temp
        }])

        return self.model.predict(X)[0]


if __name__ == "__main__":
    from src.data.data_loader import F1DataLoader

    loader = F1DataLoader()

    # Load race
    session = loader.load_session_safe(2023, "Bahrain", "R")
    race_data = loader.get_race_data(session)
    laps = race_data["laps"]

    model = TyreDegradationModel()
    model.train(laps)

    # TEST PREDICTIONS
    print("\nTest Predictions:")
    print("Soft, 5 laps:", model.predict("SOFT", 5))
    print("Medium, 15 laps:", model.predict("MEDIUM", 15))

    # Save model
    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(model.model, "ml/models/tyre_model.pkl")

    print("\n Tyre model saved!")