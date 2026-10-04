from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent


print("Loading cleaned dataset")
df = pd.read_csv("data/cleaned_factory_sensor_data.csv")
print(f"Dataset shape: {df.shape}")

feature_cols = [
    "Installation_Year",
    "Operational_Hours",
    "Temperature_C",
    "Vibration_mms",
    "Sound_dB",
    "Oil_Level_pct",
    "Coolant_Level_pct",
    "Power_Consumption_kW",
    "Last_Maintenance_Days_Ago",
    "Maintenance_History_Count",
    "Failure_History_Count",
    "Error_Codes_Last_30_Days",
]

X = df[feature_cols]
Y = df["Failure_Within_7_Days"]

# Stratified 80/20 train/test split to preserve failure proportion
X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42,
    stratify=Y,
)

print(f"Training samples: {len(X_train):,}, Test samples: {len(X_test):,}")
print("Training tuned RandomForestClassifier...")

# creating model and cutting model size by 50%
model = RandomForestClassifier(
    n_estimators=80,
    max_depth=16,
    min_samples_split=8,
    min_samples_leaf=4,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1,
)

model.fit(X_train, Y_train)

# Model evaluation
prediction = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(Y_test, prediction)
roc_auc = roc_auc_score(Y_test, probabilities)


print("\n" + "=" * 50)
print(f"Accuracy:  {acc * 100:.2f}%")
print(f"ROC-AUC:   {roc_auc:.4f}")
print("=" * 50)
print("\nClassification Report:")
print(classification_report(Y_test, prediction, target_names=["Stable (0)", "Failure (1)"], digits=4))

# Save to Backend directory
backend_dir = BASE_DIR / "Backend"
backend_dir.mkdir(exist_ok=True)
backend_model_path = backend_dir / "maintenance_model.pkl"
joblib.dump(model, backend_model_path, compress=3)
print(f"✓ Model saved to Backend: {backend_model_path}")

# Also save to root directory
root_model_path = BASE_DIR / "maintenance_model.pkl"
joblib.dump(model, root_model_path, compress=3)
print(f"✓ Model saved to root:    {root_model_path}")
