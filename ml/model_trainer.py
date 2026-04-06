import pandas as pd
import numpy as np
import os
import shap
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error
from scipy.stats import spearmanr
import xgboost as xgb
import joblib


# =========================
# Load Dataset
# =========================
df = pd.read_csv("data/training_data.csv")
print("✅ Dataset loaded:", df.shape)


# =========================
# Preprocessing
# =========================

# Encode weather
df["weather"] = df["weather"].map({"dry": 0, "wet": 1})

# Sort for time-based features
df = df.sort_values(by=["driver", "year"])


# =========================
#  Historical Features 
# =========================

# Driver historical performance
df["driver_avg_finish"] = df.groupby("driver")["finish_position"].transform(lambda x: x.shift().expanding().mean())
df["race_id"] = df["race"].astype("category").cat.codes
# Team historical performance
df["team_avg_finish"] = df.groupby("team")["finish_position"].transform(lambda x: x.shift().expanding().mean())

df["quali_vs_driver"] = df["quali_position"] - df["driver_avg_finish"]
df["driver_vs_team"] = df["driver_avg_finish"] - df["team_avg_finish"]
df["quali_vs_team"] = df["quali_position"] - df["team_avg_finish"]

# Drop rows where history not available
df = df.dropna(subset=["driver_avg_finish", "team_avg_finish"])


# =========================
# Feature / Target Split
# =========================

X = df[[
    "quali_position",
    "weather",
    "driver_avg_finish",
    "team_avg_finish",
    "quali_vs_driver",
    "driver_vs_team",
    "quali_vs_team",
    "race_id"
]]

y = df["position_gain"]


# =========================
# Train-Test Split (GROUPED)
# =========================

groups = df["race"]

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_idx, test_idx in gss.split(X, y, groups):
    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)


# =========================
# Model (XGBoost)
# =========================

model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)


# =========================
# Predictions
# =========================

preds = model.predict(X_test)


# =========================
# Evaluation
# =========================

mae = mean_absolute_error(y_test, preds)
spearman_corr = spearmanr(y_test, preds).correlation

print("\n📊 MODEL PERFORMANCE")
print(f"MAE: {mae:.2f}")
print(f"Spearman Rank Correlation: {spearman_corr:.2f}")


# =========================
# Save Model
# =========================

os.makedirs("ml/models", exist_ok=True)
joblib.dump(model, "ml/models/race_predictor.pkl")
print("\n✅ Model saved at ml/models/race_predictor.pkl")

explainer = shap.Explainer(model)
shap_values = explainer(X_test)

shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("ml/models/shap_summary.png")

print("\n📊 SHAP summary plot saved!")