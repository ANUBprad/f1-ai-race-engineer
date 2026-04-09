import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd


class StrategyEngine:
    def __init__(self):
        self.tyre_model = joblib.load("ml/models/tyre_model.pkl")

    def predict_degradation(self, compound, tyre_age, lap_number=10, track_temp=35, air_temp=25):
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

        return self.tyre_model.predict(X)[0]

    def simulate_stay_out(self, compound, tyre_age, laps_to_sim=5):
        total_loss = 0

        for i in range(laps_to_sim):
            loss = self.predict_degradation(compound, tyre_age + i)
            total_loss += loss

        return total_loss
    
    def get_pit_loss(self, circuit):
        pit_loss_map = {
            "Monaco": 22,
            "Singapore": 24,
            "Bahrain": 20,
            "Monza": 18,
            "Silverstone": 21,
            "Default": 20
        }
        return pit_loss_map.get(circuit, 20)

    def simulate_pit(self, circuit="Default", new_compound="MEDIUM", laps_to_sim=5):
        pit_loss = self.get_pit_loss(circuit)
        total_loss = pit_loss

        for i in range(laps_to_sim):
            loss = self.predict_degradation(new_compound, i)
            total_loss += loss

        return total_loss

    def simulate_undercut(self, compound, tyre_age, gap_ahead, opponent_pit_lap=2):
        gain = 0

        for i in range(opponent_pit_lap):
            your_lap = self.predict_degradation("MEDIUM", i)
            opponent_lap = self.predict_degradation(compound, tyre_age + i)
            gain += (opponent_lap - your_lap)

        print(f"\nUndercut Gain: {gain:.2f}s vs Gap Ahead: {gap_ahead:.2f}s")

        return gain > gap_ahead

    def decide(self, compound, tyre_age, circuit="Default", gap_ahead=5, gap_behind=25):
        stay_loss = self.simulate_stay_out(compound, tyre_age)
        pit_loss = self.simulate_pit(circuit)

        print(f"\nStay Out Loss: {stay_loss:.2f}s")
        print(f"Pit Loss: {pit_loss:.2f}s")
        print(f"Gap Ahead: {gap_ahead:.2f}s")
        print(f"Gap Behind: {gap_behind:.2f}s")

        can_undercut = self.simulate_undercut(compound, tyre_age, gap_ahead)
        will_lose_position = pit_loss > gap_behind

        # FINAL DECISION LOGIC
        if can_undercut and not will_lose_position:
            decision = "PIT NOW (UNDERCUT)"
        elif pit_loss < stay_loss and not will_lose_position:
            decision = "PIT NOW"
        elif will_lose_position:
            decision = "DELAY PIT (TRAFFIC RISK)"
        else:
            decision = "STAY OUT"

        confidence = abs(stay_loss - pit_loss) / (stay_loss + pit_loss)
        if can_undercut:
            confidence += 0.2
        if will_lose_position:
            confidence -= 0.3
        confidence = max(0.5, confidence)   # minimum confidence
        confidence = min(confidence, 0.9)   # cap max
        confidence = float(confidence)

        return {"decision": decision, "confidence": round(confidence, 2)}

# MAIN EXECUTION 
if __name__ == "__main__":
    engine = StrategyEngine()

    result = engine.decide(
        compound="MEDIUM",
        tyre_age=12,
        circuit="Bahrain",
        gap_ahead=5,
        gap_behind=25
    )

    print("\n🚦 Strategy Decision:", result["decision"])
    print("Confidence:", result["confidence"])