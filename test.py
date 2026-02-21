import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("data/finger_data.csv")

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test = [], []
y_train, y_test = [], []

unique_labels = np.unique(y_encoded)

for label in unique_labels:
    indices = np.where(y_encoded == label)[0]
    
    split = int(len(indices) * 0.8)
    
    train_idx = indices[:split]
    test_idx = indices[split:]
    
    X_train.extend(X[train_idx])
    y_train.extend(y_encoded[train_idx])
    
    X_test.extend(X[test_idx])
    y_test.extend(y_encoded[test_idx])

X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Per-Class Block Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, "silent_voice_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("\nModel saved successfully.")