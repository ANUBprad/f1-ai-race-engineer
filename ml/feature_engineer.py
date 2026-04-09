import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from tqdm import tqdm

from src.data.data_loader import F1DataLoader

class FeatureEngineer:
    def __init__(self):
        self.loader = F1DataLoader()

    def get_avg_lap_time(self, laps):
        """
        Compute average lap time per driver (excluding pit laps)
        """
        laps = laps[laps['PitOutTime'].isna()]
        return laps.groupby('Driver')['LapTime'].mean().dt.total_seconds()

    def get_weather_condition(self, weather_df):
        """
        Improved weather classification
        """
        if weather_df['Rainfall'].mean() > 0.1:
            return "wet"
        return "dry"

    def process_race(self, year, gp_name):
        """
        Process a single race into feature rows
        """
        try:
            race_session = self.loader.load_session_safe(year, gp_name, "R")
            quali_session = self.loader.load_session_safe(year, gp_name, "Q")

            if race_session is None or quali_session is None:
                print(f"⚠️ Skipping invalid race: {year} {gp_name}")
                return pd.DataFrame()

            race_data = self.loader.get_race_data(race_session)
            laps = race_data["laps"]
            weather = race_data["weather"]
            results = race_data["results"]

            avg_lap_times = self.get_avg_lap_time(laps)
            weather_condition = self.get_weather_condition(weather)

            # NEW FEATURE CALCULATIONS
            lap_std = laps.groupby('Driver')['LapTime'].std().dt.total_seconds()
            fastest_lap = laps['LapTime'].min().total_seconds()

            rows = []
            for _, driver_row in results.iterrows():
                driver = driver_row['Abbreviation']

                try:
                    quali_pos = quali_session.results[
                        quali_session.results['Abbreviation'] == driver
                    ]['Position'].values[0]

                except Exception:
                    quali_pos = np.nan

                avg_time = avg_lap_times.get(driver, np.nan)

                row = {
                    "year": year,
                    "race": gp_name,
                    "driver": driver,
                    "team": driver_row['TeamName'],
                    "grid_position": driver_row['GridPosition'],
                    "finish_position": driver_row['Position'],
                    "quali_position": quali_pos,
                    "avg_lap_time": avg_time,
                    "weather": weather_condition,
                    "driver_consistency": lap_std.get(driver, np.nan),
                    "pace_delta": avg_time - fastest_lap if pd.notna(avg_time) else np.nan,
                    "grid_advantage": driver_row['GridPosition'] - quali_pos if pd.notna(quali_pos) else np.nan,
                    "position_gain": driver_row['GridPosition'] - driver_row['Position']
                }

                rows.append(row)
            df = pd.DataFrame(rows)

            # DATA CLEANING
            df = df[df["grid_position"] > 0]
            df = df[df["finish_position"] > 0]

            df = df.dropna(subset=[
                "avg_lap_time",
                "driver_consistency",
                "pace_delta"
            ])
            return df

        except Exception as e:
            print(f"❌ Error processing {year} {gp_name}: {e}")
            return pd.DataFrame()

    def build_dataset(self, years, races):
        """
        Build dataset across seasons
        """
        all_data = []

        for year in years:
            print(f"\nProcessing {year} season...")
            for race in tqdm(races):
                time.sleep(0.3)  
                df = self.process_race(year, race)

                if not df.empty:
                    all_data.append(df)

        if len(all_data) == 0:
            print("❌ No data collected!")
            return pd.DataFrame()

        final_df = pd.concat(all_data, ignore_index=True)
        return final_df


if __name__ == "__main__":
    fe = FeatureEngineer()
    years = [2021, 2022, 2023]
    races = [
        "Bahrain", "Saudi Arabia", "Australia", "Emilia Romagna",
        "Miami", "Spain", "Monaco", "Azerbaijan", "Canada",
        "Austria", "France", "Hungary", "Belgium",
        "Netherlands", "Italy", "Singapore", "Japan",
        "United States", "Mexico", "Brazil", "Abu Dhabi"
    ]

    dataset = fe.build_dataset(years, races)

    if not dataset.empty:
        dataset["weather"] = dataset["weather"].map({"dry": 0, "wet": 1})

        dataset.to_csv("data/training_data.csv", index=False)
        print("\n✅ Feature upgraded dataset created:", dataset.shape)

    print("\n🔍 Dataset Info:")
    print(dataset.info())

    print("\n📊 Missing values:")
    print(dataset.isnull().sum())