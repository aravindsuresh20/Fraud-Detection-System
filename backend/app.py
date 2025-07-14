from flask import Flask, request, render_template
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Use current working directory
base_dir = os.getcwd()

# Paths for model and scaler files
model_dir = os.path.join(base_dir, 'model')
model_path = os.path.join(model_dir, 'fraud_model.pkl')
scaler_path = os.path.join(model_dir, 'scaler.pkl')

# Load model and scaler if they exist
model = joblib.load(model_path) if os.path.exists(model_path) else None
scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None

@app.route('/')
def home():
    try:
        eda()  # Run EDA every time home is accessed
    except Exception as e:
        print(f"EDA failed on home: {e}")
    return render_template('home.html')

@app.route('/analyze')
def analyze():
    try:
        eda()  # Run EDA every time analyze is accessed
        return render_template('analysis_complete.html')  # Optional: create this template
    except Exception as e:
        return f"EDA failed on analyze: {str(e)}"

@app.route('/predict-page')
def predict_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return "Model or scaler file not found. Please ensure they exist in the 'model/' directory."
    try:
        features = [float(request.form[key]) for key in request.form]
        input_df = pd.DataFrame([features], columns=scaler.feature_names_in_)
        scaled = scaler.transform(input_df)
        prediction = model.predict(scaled)[0]
        result = 'FRAUD ❌' if prediction == 1 else 'NOT fraud ✅'
        return render_template('index.html', prediction_text=f"Prediction: Transaction is {result}")
    except Exception as e:
        return f"Error: {str(e)}"

def eda():
    file_path = "C:/Users/AS5560/Downloads/Controller Projects/Fraud Detection System/data/fraud_dataset.csv"
    df = pd.read_csv(file_path)

    eda_summary = []

    eda_summary.append("DATASET SHAPE:")
    eda_summary.append(str(df.shape))

    eda_summary.append("\nCOLUMN NAMES AND DATA TYPES:")
    eda_summary.append(str(df.dtypes))

    eda_summary.append("\nSUMMARY STATISTICS:")
    eda_summary.append(str(df.describe(include='all')))

    eda_summary.append("\nMISSING VALUES PER COLUMN:")
    eda_summary.append(str(df.isnull().sum()))

    eda_summary.append("\nUNIQUE VALUES PER COLUMN:")
    eda_summary.append(str(df.nunique()))

    eda_summary.append("\nFIRST 5 ROWS OF DATA:")
    eda_summary.append(str(df.head()))

    eda_text = "\n\n".join(eda_summary)

    output_dir = "C:/Users/AS5560/Downloads/Controller Projects/Fraud Detection System/backend"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "eda_summary.txt")

    with open(output_file, "w") as f:
        f.write(eda_text)

    print(f"✅ EDA summary saved to: {output_file}")

# Run EDA once when the app starts
try:
    print("Performing EDA on startup...", flush=True)
    eda()
except Exception as e:
    print(f"EDA failed on startup: {e}", flush=True)

if __name__ == "__main__":
    app.run(debug=True)
