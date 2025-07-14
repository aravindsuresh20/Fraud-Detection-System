import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
data_path = 'data/fraud_dataset.csv'  # make sure this file exists
df = pd.read_csv(data_path)

# Features and target
X = df.drop('fraud', axis=1)
y = df['fraud']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline: Standardize + Train
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', DecisionTreeClassifier(random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model
os.makedirs('model', exist_ok=True)
joblib.dump(pipeline, 'backend/model/fraud_model.pkl')

print("✅ Model trained and saved to 'model/fraud_model.pkl'")
