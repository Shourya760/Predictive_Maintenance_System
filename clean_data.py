import pandas as pd

df = pd.read_csv("factory_sensor_data.csv")

print("Original shape:", df.shape)

# Convert target
df["Failure_Within_7_Days"] = (
    df["Failure_Within_7_Days"]
    .astype(int)
)

# Drop unwanted columns
df = df.drop(
    [
        "Machine_ID",
        "Machine_Type",
        "AI_Supervision",
        "Remaining_Useful_Life_days"
    ],
    axis=1,
    errors="ignore"
)

# Remove duplicate rows
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())


# Vibration cannot be negative
df = df[df["Vibration_mms"] >= 0]

# Power consumption cannot be negative
df = df[df["Power_Consumption_kW"] >= 0]

# Oil and coolant percentages must be 0-100
df = df[
    df["Oil_Level_pct"].between(0, 100) &
    df["Coolant_Level_pct"].between(0, 100)
]

# Check target values
print("\nTarget values:")
print(df["Failure_Within_7_Days"].value_counts())

# Final information
print("\nFinal shape:", df.shape)

# Save
df.to_csv(
    "cleaned_factory_sensor_data.csv",
    index=False
)

print("\nCleaning completed!")
print("Saved as cleaned_factory_sensor_data.csv")