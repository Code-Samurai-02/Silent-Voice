import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# 1. Load dataset
data = pd.read_csv("data/index_data.csv")  # change filename

# 2. Features and labels
X = data[['x', 'y', 'z']]
y = data['alphabet']

# 3. Encode labels (A, B → 0,1)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 4. Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# 5. Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Predict
y_pred = model.predict(X_test)

# 7. Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

import joblib

joblib.dump(model, "alphabet_model.pkl")
joblib.dump(le, "label_encoder.pkl")