# Factory Sensor Predictive Maintenance System

A machine learning and web dashboard system that analyzes real-time machine telemetry data (12 sensor features) to predict whether equipment will experience a critical failure within the next 7 days.

---

## 🏗️ Architecture

- **Machine Learning**: Scikit-Learn `RandomForestClassifier` trained with class-weight balancing on 500,000 factory sensor readings.
- **Backend**: FastAPI REST API providing fast model inference with automatic schema validation via Pydantic.
- **Frontend**: Modern React 19 single-page dashboard built with Vite and Tailwind CSS.

---

## 📁 Project Structure

```
Pridictive_Maintenance/
├── Backend/
│   ├── main.py                   # FastAPI REST API & inference endpoints
│   └── maintenance_model.pkl     # Trained Random Forest model binary
├── Frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx        # Navigation header & live status
│   │   │   ├── PredictionDashboard.jsx # 12-channel telemetry form & results
│   │   │   └── Footer.jsx        # System footer
│   │   ├── App.jsx               # Root layout
│   │   ├── main.jsx              # React DOM mounting
│   │   └── index.css             # Tailwind CSS entry
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── factory_sensor_data.csv   # Raw sensor telemetry dataset
│   └── cleaned_factory_sensor_data.csv # Pre-processed dataset
├── clean_data.py                 # Data cleaning and sanity validation script
├── train_model.py                # Model training and artifact generation script
├── requirements.txt              # Python virtual environment dependencies
└── README.md
```

---

## 🎛️ Monitored Sensor Channels (12 Features)

1. **Installation Year** (`Installation_Year`)
2. **Operational Hours** (`Operational_Hours`)
3. **Temperature (°C)** (`Temperature_C`)
4. **Vibration (mm/s)** (`Vibration_mms`)
5. **Sound (dB)** (`Sound_dB`)
6. **Oil Level (%)** (`Oil_Level_pct`)
7. **Coolant Level (%)** (`Coolant_Level_pct`)
8. **Power Consumption (kW)** (`Power_Consumption_kW`)
9. **Days Since Last Maintenance** (`Last_Maintenance_Days_Ago`)
10. **Maintenance History Count** (`Maintenance_History_Count`)
11. **Past Failure Count** (`Failure_History_Count`)
12. **Error Codes in Last 30 Days** (`Error_Codes_Last_30_Days`)

---

## 🚀 Getting Started

### 1. Python Environment Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. (Optional) Data Cleaning & Model Retraining

The pre-trained model and cleaned dataset are already bundled. If you wish to re-run the pipeline:

```bash
# Clean raw sensor telemetry
python clean_data.py

# Train Random Forest classifier and save model binaries
python train_model.py
```

### 3. Start the Backend API

From the project root:

```bash
uvicorn Backend.main:app --reload --port 8000
```

- API Base URL: `http://127.0.0.1:8000`
- Interactive API Docs (Swagger): `http://127.0.0.1:8000/docs`

### 4. Start the Frontend Dashboard

In a separate terminal:

```bash
cd Frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🧪 Testing the API directly

You can test the prediction endpoint directly via `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Installation_Year": 2018,
    "Operational_Hours": 8500,
    "Temperature_C": 82.5,
    "Vibration_mms": 4.2,
    "Sound_dB": 78,
    "Oil_Level_pct": 45,
    "Coolant_Level_pct": 60,
    "Power_Consumption_kW": 15.2,
    "Last_Maintenance_Days_Ago": 120,
    "Maintenance_History_Count": 5,
    "Failure_History_Count": 2,
    "Error_Codes_Last_30_Days": 3
  }'
```

**Sample Response:**

```json
{
  "prediction": 0,
  "message": "No failure predicted within 7 days",
  "failure_probability": 0.16
}
```