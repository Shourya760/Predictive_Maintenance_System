from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import SensorData, PredictionResponse


# FastAPI
app = FastAPI(title="Factory Maintenance Prediction API")

# CORS Configuration
app.add_middleware( CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Trained ML Model
model = joblib.load("maintenance_model.pkl")
# Feature Names
# Must match the model's training features

FEATURE_NAMES = [
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

# Telemetry Risk Analysis
def analyze_telemetry_risks(data: SensorData):

    factors = []
    actions = []

    # Vibration checks
    if data.Vibration_mms > 20.0:
        factors.append({
            "sensor": "Vibration",
            "severity": "critical",
            "value": f"{data.Vibration_mms:.1f} mm/s",
            "threshold": "> 20 mm/s",
            "message": "Critical mechanical vibration spike",
        })
        actions.append(
            "Halt operation or inspect rotor balancing and shaft alignment immediately."
        )
    elif data.Vibration_mms > 12.0:
        factors.append({
            "sensor": "Vibration",
            "severity": "warning",
            "value": f"{data.Vibration_mms:.1f} mm/s",
            "threshold": "> 12 mm/s",
            "message": "Elevated vibration above normal threshold",
        })
        actions.append(
            "Schedule bearing and mount vibration inspection."
        )
    
    # Temperature checks
    if data.Temperature_C > 95.0:
        factors.append({
            "sensor": "Temperature",
            "severity": "critical",
            "value": f"{data.Temperature_C:.1f} °C",
            "threshold": "> 95 °C",
            "message": "Dangerous thermal overheating",
        })
        actions.append(
            "Verify coolant circulation and check for heat exchanger blockage."
        )
    elif data.Temperature_C > 80.0:
        factors.append({
            "sensor": "Temperature",
            "severity": "warning",
            "value": f"{data.Temperature_C:.1f} °C",
            "threshold": "> 80 °C",
            "message": "High operating temperature",
        })

        actions.append(
            "Monitor thermal gradient and inspect radiator fan operation."
        )

    # Oil level checks
    if data.Oil_Level_pct < 15.0:
        factors.append({
            "sensor": "Oil Level",
            "severity": "critical",
            "value": f"{data.Oil_Level_pct:.1f}%",
            "threshold": "< 15%",
            "message": "Critically low lubricant reservoir",
        })
        actions.append(
            "Replenish lubricating oil immediately to prevent mechanical seizure."
        )
    elif data.Oil_Level_pct < 35.0:
        factors.append({
            "sensor": "Oil Level",
            "severity": "warning",
            "value": f"{data.Oil_Level_pct:.1f}%",
            "threshold": "< 35%",
            "message": "Depleted oil reservoir",
        })
        actions.append(
            "Top up oil reservoir during next maintenance cycle."
        )

    # Coolant level checks
    if data.Coolant_Level_pct < 15.0:
        factors.append({
            "sensor": "Coolant Level",
            "severity": "critical",
            "value": f"{data.Coolant_Level_pct:.1f}%",
            "threshold": "< 15%",
            "message": "Severe coolant loss",
        })
        actions.append(
            "Refill coolant and perform pressure leak test on fluid lines."
        )
    elif data.Coolant_Level_pct < 35.0:
        factors.append({
            "sensor": "Coolant Level",
            "severity": "warning",
            "value": f"{data.Coolant_Level_pct:.1f}%",
            "threshold": "< 35%",
            "message": "Low coolant level",
        })

    # Error code checks
    if data.Error_Codes_Last_30_Days >= 10:
        factors.append({
            "sensor": "Error Codes",
            "severity": "critical",
            "value": f"{data.Error_Codes_Last_30_Days} errors",
            "threshold": ">= 10",
            "message": "Excessive recurring controller error codes",
        })
        actions.append(
            "Clear and diagnose controller fault codes via diagnostic interface."
        )
    elif data.Error_Codes_Last_30_Days >= 5:
        factors.append({
            "sensor": "Error Codes",
            "severity": "warning",
            "value": f"{data.Error_Codes_Last_30_Days} errors",
            "threshold": ">= 5",
            "message": "Elevated fault code frequency",
       } )

    # Maintenance recency checks
    if data.Last_Maintenance_Days_Ago > 300:
        factors.append({
            "sensor": "Maintenance Recency",
            "severity": "warning",
            "value": f"{data.Last_Maintenance_Days_Ago} days ago",
            "threshold": "> 300 days",
            "message": "Significantly overdue for routine maintenance",
        })
        actions.append(
            "Execute overdue standard preventative maintenance checkup."
        )

    # Sound check
    if data.Sound_dB > 95.0:
        factors.append({
            "sensor": "Acoustic Noise",
            "severity": "warning",
            "value": f"{data.Sound_dB:.1f} dB",
            "threshold": "> 95 dB",
            "message": "Excessive acoustic noise detected",
        })

    # Default action
    if not actions:
        actions.append(
            "All primary sensor telemetry within safe operating envelopes. "
            "Maintain standard inspection schedule."
        )

    return factors, actions


# Home Endpoint
@app.get("/")

def home():
    return {
        "message": "Maintenance Prediction API is running ✅"
    }

# Prediction Endpoint
@app.post("/predict", response_model=PredictionResponse)

def predict(data: SensorData):
    # input data
    input_row = [
        data.Installation_Year,
        data.Operational_Hours,
        data.Temperature_C,
        data.Vibration_mms,
        data.Sound_dB,
        data.Oil_Level_pct,
        data.Coolant_Level_pct,
        data.Power_Consumption_kW,
        data.Last_Maintenance_Days_Ago,
        data.Maintenance_History_Count,
        data.Failure_History_Count,
        data.Error_Codes_Last_30_Days,
    ]

    # Convert input into DataFrame
    input_df = pd.DataFrame(
        [input_row],
        columns=FEATURE_NAMES,
    )

    # Make prediction
    prediction = model.predict(input_df)
    probabilities = model.predict_proba(input_df)

    prediction_value = int(prediction[0])
    failure_probability = float(probabilities[0][1])

    # Generate prediction message
    if prediction_value == 1:
        message = "Failure predicted within 7 days"
    else:
        message = "No failure predicted within 7 days"

    # Analyze sensor risks
    risk_factors, recommended_actions = analyze_telemetry_risks(data)

    # Return response
    return {
        "prediction": prediction_value,
        "message": message,
        "failure_probability": failure_probability,
        "risk_factors": risk_factors,
        "recommended_actions": recommended_actions,
    }
