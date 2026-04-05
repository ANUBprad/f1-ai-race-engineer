import fastf1
import pandas as pd
from typing import Dict, Any
import logging
import time

logging.basicConfig(level=logging.INFO)


class F1DataLoader:
    def __init__(self):
        pass

    def load_session(self, year: int, gp_name: str, session_type: str = "R"):
        """
        Load a FastF1 session.

        Args:
            year: e.g. 2023
            gp_name: e.g. 'Monza'
            session_type: 'R' (Race), 'Q', 'FP1', etc.

        Returns:
            session object
        """
        try:
            logging.info(f"Loading {year} {gp_name} {session_type} session...")
            session = fastf1.get_session(year, gp_name, session_type)
            session.load()
            return session

        except Exception as e:
            logging.error(f"Failed to load session: {e}")
            raise
    
    def load_session_safe(self, year, gp_name, session_type="R"):
        """
        Safe loader with retry + rate limit handling
        """
        for attempt in range(3):
            try:
                return self.load_session(year, gp_name, session_type)

            except Exception as e:
                if "500 calls/h" in str(e):
                    print("⚠️ Rate limit hit. Waiting 60 seconds...")
                    time.sleep(60)
                else:
                    print(f"❌ Error: {e}")
                    break

        return None

    def get_race_data(self, session) -> Dict[str, Any]:
        """
        Extract structured race data.

        Returns:
            dict with laps, telemetry, weather, results
        """
        try:
            laps = session.laps.copy()
            weather = session.weather_data.copy()
            results = session.results.copy()

            return {
                "laps": laps,
                "weather": weather,
                "results": results
            }

        except Exception as e:
            logging.error(f"Error extracting race data: {e}")
            raise

    def get_driver_telemetry(self, session, driver: str, lap_number: int):
        """
        Fetch telemetry for a driver on a specific lap.

        Args:
            driver: e.g. 'VER', 'HAM'
            lap_number: lap index

        Returns:
            telemetry dataframe
        """
        try:
            lap = session.laps.pick_driver(driver).pick_lap(lap_number)

            if lap.empty:
                raise ValueError("No lap data found")

            car_data = lap.get_car_data().add_distance()

            return car_data

        except Exception as e:
            logging.error(f"Telemetry fetch error: {e}")
            raise