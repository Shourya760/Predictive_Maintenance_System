from pydantic import BaseModel

# Data expected from the frontend
class SensorData(BaseModel):
    Installation_Year: int
    Operational_Hours: float
    Temperature_C: float
    Vibration_mms: float
    Sound_dB: float
    Oil_Level_pct: float
    Coolant_Level_pct: float
    Power_Consumption_kW: float
    Last_Maintenance_Days_Ago: int
    Maintenance_History_Count: int
    Failure_History_Count: int
    Error_Codes_Last_30_Days: int


# Response sent back to the frontend
class PredictionResponse(BaseModel):
    prediction: int
    message: str
    failure_probability: float
    risk_factors: list[dict[str, str]]
    recommended_actions: list[str]
