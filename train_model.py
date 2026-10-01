import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("cleaned_factory_sensor_data.csv")

X = df[
    [
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
        "Error_Codes_Last_30_Days"
    ]
]

Y = df["Failure_Within_7_Days"]

X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42,
    stratify=Y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train, Y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(Y_test, prediction)

joblib.dump(model, "maintenance_model.pkl", compress=3)

print("Model Accuracy:", accuracy)
print("Model saved!")