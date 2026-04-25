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

        return gain > gap_ahead, gain
    
    def simulate_strategy_options(self, compound, tyre_age, circuit, gap_ahead):

        stay_loss = self.simulate_stay_out(compound, tyre_age)
        pit_loss = self.simulate_pit(circuit)

        undercut_gain = 0
        for i in range(2):
            your_lap = self.predict_degradation("MEDIUM", i)
            opponent_lap = self.predict_degradation(compound, tyre_age + i)
            undercut_gain += (opponent_lap - your_lap)

        return {
            "stay_out_loss": round(stay_loss, 2),
            "pit_loss": round(pit_loss, 2),
            "undercut_gain": round(undercut_gain, 2),
            "gap_ahead": gap_ahead
        }

    def decide(self, compound, tyre_age, circuit="Default", gap_ahead=5, gap_behind=25):
        stay_loss = self.simulate_stay_out(compound, tyre_age)
        pit_loss = self.simulate_pit(circuit)
        can_undercut, undercut_gain = self.simulate_undercut(compound, tyre_age, gap_ahead)
        will_lose_position = pit_loss > (gap_behind + 3)

        # FINAL DECISION LOGIC
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
        confidence = round(confidence, 2)

        return {
            "action": decision,
            "confidence": round(float(confidence), 2),
            "reasoning": f"Stay loss: {stay_loss:.2f}s vs Pit loss: {pit_loss:.2f}s. Undercut gain: {undercut_gain:.2f}s."
        }


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

    print("\n🏁 Strategy Decision:")
    print("Action:", result["action"])
    print("Confidence:", result["confidence"])
    print("Reasoning:", result["reasoning"])