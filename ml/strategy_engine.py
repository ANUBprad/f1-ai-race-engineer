import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd


class StrategyEngine:

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, "ml", "models", "tyre_model.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")

        self.tyre_model = joblib.load(model_path)

    # 🔥 NEW: Circuit Data (centralized intelligence)
    def get_circuit_data(self, circuit):
        circuit_data = {
            "Bahrain": {"pit_loss": 20, "degradation": 1.1},
            "Saudi Arabia": {"pit_loss": 19, "degradation": 0.9},
            "Australia": {"pit_loss": 21, "degradation": 1.0},
            "Japan": {"pit_loss": 22, "degradation": 1.2},
            "China": {"pit_loss": 23, "degradation": 1.1},
            "Miami": {"pit_loss": 20, "degradation": 1.0},
            "Imola": {"pit_loss": 21, "degradation": 1.2},
            "Monaco": {"pit_loss": 28, "degradation": 0.8},
            "Canada": {"pit_loss": 22, "degradation": 1.0},
            "Spain": {"pit_loss": 23, "degradation": 1.3},
            "Austria": {"pit_loss": 18, "degradation": 1.1},
            "Silverstone": {"pit_loss": 21, "degradation": 1.4},
            "Hungary": {"pit_loss": 22, "degradation": 1.2},
            "Belgium": {"pit_loss": 23, "degradation": 1.1},
            "Netherlands": {"pit_loss": 21, "degradation": 1.2},
            "Monza": {"pit_loss": 18, "degradation": 0.9},
            "Singapore": {"pit_loss": 24, "degradation": 1.3},
            "Austin": {"pit_loss": 22, "degradation": 1.2},
            "Mexico": {"pit_loss": 21, "degradation": 1.0},
            "Brazil": {"pit_loss": 22, "degradation": 1.1},
            "Las Vegas": {"pit_loss": 19, "degradation": 0.9},
            "Qatar": {"pit_loss": 23, "degradation": 1.5},
            "Abu Dhabi": {"pit_loss": 21, "degradation": 1.1},
        }

        return circuit_data.get(circuit, {"pit_loss": 20, "degradation": 1.0})

    # 🔥 UPDATED: Now includes circuit impact
    def predict_degradation(self, compound, tyre_age, circuit="Bahrain", lap_number=10, track_temp=35, air_temp=25):
        compound_map = {
            "SOFT": 0,
            "MEDIUM": 1,
            "HARD": 2,
            "INTERMEDIATE": 3,
            "WET": 4
        }

        circuit_data = self.get_circuit_data(circuit)
        degradation_factor = circuit_data["degradation"]

        X = pd.DataFrame([{
            "compound_encoded": compound_map.get(compound, 1),
            "tyre_age": tyre_age,
            "lap_number": lap_number,
            "track_temp": track_temp,
            "air_temp": air_temp
        }])

        base_pred = self.tyre_model.predict(X)[0]

        return base_pred * degradation_factor

    # 🔥 UPDATED
    def simulate_stay_out(self, compound, tyre_age, circuit, laps_to_sim=5):
        total_loss = 0

        for i in range(laps_to_sim):
            loss = self.predict_degradation(compound, tyre_age + i, circuit)
            total_loss += loss

        return total_loss

    # 🔥 UPDATED
    def simulate_pit(self, circuit, new_compound="MEDIUM", laps_to_sim=5):
        circuit_data = self.get_circuit_data(circuit)
        pit_loss = circuit_data["pit_loss"]

        total_loss = pit_loss

        for i in range(laps_to_sim):
            loss = self.predict_degradation(new_compound, i, circuit)
            total_loss += loss

        return total_loss

    # 🔥 UPDATED
    def simulate_undercut(self, compound, tyre_age, circuit, gap_ahead, opponent_pit_lap=2):
        gain = 0

        for i in range(opponent_pit_lap):
            your_lap = self.predict_degradation("MEDIUM", i, circuit)
            opponent_lap = self.predict_degradation(compound, tyre_age + i, circuit)
            gain += (opponent_lap - your_lap)

        return gain > gap_ahead, gain

    # 🔥 UPDATED
    def simulate_strategy_options(self, compound, tyre_age, circuit, gap_ahead):
        stay_loss = self.simulate_stay_out(compound, tyre_age, circuit)
        pit_loss = self.simulate_pit(circuit)

        undercut_gain = 0
        for i in range(2):
            your_lap = self.predict_degradation("MEDIUM", i, circuit)
            opponent_lap = self.predict_degradation(compound, tyre_age + i, circuit)
            undercut_gain += (opponent_lap - your_lap)

        return {
            "stay_out_loss": round(stay_loss, 2),
            "pit_loss": round(pit_loss, 2),
            "undercut_gain": round(undercut_gain, 2),
            "gap_ahead": gap_ahead
        }

    # 🔥 UPDATED CORE LOGIC
    def decide(self, compound, tyre_age, circuit="Bahrain", gap_ahead=5, gap_behind=25):
        stay_loss = self.simulate_stay_out(compound, tyre_age, circuit)
        pit_loss = self.simulate_pit(circuit)
        can_undercut, undercut_gain = self.simulate_undercut(compound, tyre_age, circuit, gap_ahead)

        will_lose_position = pit_loss > (gap_behind + 3)

        if can_undercut:
            decision = "PIT NOW (UNDERCUT)"

        elif pit_loss + 2 < stay_loss:
            decision = "PIT NOW"

        elif will_lose_position:
            decision = "DELAY PIT"

        else:
            decision = "STAY OUT"

        confidence = abs(stay_loss - pit_loss) / max(stay_loss, pit_loss)

        if can_undercut:
            confidence += 0.2

        if will_lose_position:
            confidence -= 0.2

        confidence = max(0.2, confidence)
        confidence = min(confidence, 0.95)

        return {
            "action": decision,
            "confidence": round(float(confidence), 2),
            "reasoning": f"Stay loss: {stay_loss:.2f}s vs Pit loss: {pit_loss:.2f}s. Undercut gain: {undercut_gain:.2f}s."
        }


# TEST RUN
if __name__ == "__main__":
    engine = StrategyEngine()

    result = engine.decide(
        compound="MEDIUM",
        tyre_age=12,
        circuit="Monaco",
        gap_ahead=5,
        gap_behind=25
    )

    print("\n🏁 Strategy Decision:")
    print("Action:", result["action"])
    print("Confidence:", result["confidence"])
    print("Reasoning:", result["reasoning"])