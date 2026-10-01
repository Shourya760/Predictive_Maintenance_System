import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Predictive Maintenance", page_icon="⚙️", layout="wide")

st.title("⚙️ Predictive Maintenance")
st.caption("Machine Failure Forecasting System • 7-Day Horizon")
st.divider()

def load_model():
    return joblib.load("maintenance_model.pkl")

model = load_model()

st.subheader("📊 Machine Sensor Data")

c1, c2 = st.columns(2)

with c1:
    installation_year = st.number_input("🏭 Installation Year", 1950, 2030, 2020)
    operational_hours = st.number_input("⏱️ Operational Hours", 0, 100000, 25000)
    temperature = st.number_input("🌡️ Temperature (°C)", -20.0, 150.0, 55.0)
    vibration = st.number_input("〰️ Vibration (mm/s)", 0.0, 50.0, 8.0)
    sound = st.number_input("🔊 Sound (dB)", 0.0, 150.0, 70.0)
    oil = st.number_input("🛢️ Oil Level (%)", 0.0, 100.0, 75.0)

with c2:
    coolant = st.number_input("💧 Coolant Level (%)", 0.0, 100.0, 70.0)
    power = st.number_input("⚡ Power Consumption (kW)", 0.0, 600.0, 120.0)
    last_maintenance = st.number_input("🔧 Last Maintenance (Days Ago)", 0, 5000, 30)
    maintenance_history = st.number_input("🛠️ Maintenance History Count", 0, 100, 5)
    failure_history = st.number_input("❌ Failure History Count", 0, 100, 0)
    errors = st.number_input("⚠️ Error Codes (Last 30 Days)", 0, 30, 0)

if st.button("🔮 Predict Failure Risk", type="primary", use_container_width=True):

    data = pd.DataFrame([[
        installation_year, operational_hours, temperature, vibration,
        sound, oil, coolant, power, last_maintenance,
        maintenance_history, failure_history, errors
    ]], columns=[
        "Installation_Year", "Operational_Hours", "Temperature_C",
        "Vibration_mms", "Sound_dB", "Oil_Level_pct",
        "Coolant_Level_pct", "Power_Consumption_kW",
        "Last_Maintenance_Days_Ago", "Maintenance_History_Count",
        "Failure_History_Count", "Error_Codes_Last_30_Days"
    ])

    warnings = []

    if temperature > 85:
        warnings.append(f"Temperature critical: {temperature:.1f} °C")
    if vibration > 20:
        warnings.append(f"Vibration too high: {vibration:.1f} mm/s")
    if oil < 20:
        warnings.append(f"Oil level critically low: {oil:.1f}%")
    if coolant < 20:
        warnings.append(f"Coolant level critically low: {coolant:.1f}%")
    if errors >= 5:
        warnings.append(f"Frequent error codes: {errors}")

    ml_prob = float(model.predict_proba(data)[0][1])

    sensor_risk = min(0.50 + 0.15 * len(warnings), 0.98) if warnings else 0
    final_risk = max(ml_prob, sensor_risk)

    is_failure = final_risk >= 0.50 or model.predict(data)[0] == 1

    st.divider()
    st.subheader("🔎 Prediction Result")

    r1, r2 = st.columns(2)

    with r1:
        if is_failure:
            st.error("🚨 FAILURE RISK DETECTED")
            st.markdown("**Failure_Within_7_Days: `TRUE`**")
        else:
            st.success("✅ MACHINE IS NORMAL")
            st.markdown("**Failure_Within_7_Days: `FALSE`**")

    with r2:
        st.metric("Failure Risk", f"{final_risk * 100:.1f}%")
        st.progress(min(final_risk, 1.0))

    if warnings:
        st.warning("⚠️ **Active Sensor Alerts:**\n\n- " + "\n- ".join(warnings))
    else:
        st.success("✅ All sensor values are within defined limits.")

st.divider()
st.caption("Predictive Maintenance Project • Random Forest")

