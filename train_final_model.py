import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

# ===============================
# 1. Load Dataset
# ===============================
data = pd.read_csv("data/finger_data.csv")

# Separate features and labels
X = data.iloc[:, :-1].values   # 15 features
y = data.iloc[:, -1].values

# ===============================
# 2. Normalize Each Finger Vector
# ===============================
def normalize_fingers(X):
    X_norm = X.copy()
    for i in range(0, 15, 3):  # every 3 columns (x,y,z)
        norm = np.linalg.norm(X[:, i:i+3], axis=1, keepdims=True)
        X_norm[:, i:i+3] = X[:, i:i+3] / norm
    return X_norm

X = normalize_fingers(X)

# ===============================
# 3. Encode Labels
# ===============================
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ===============================
# 4. Per-Class Block Split
# ===============================
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

# ===============================
# 5. Train Optimized Model
# ===============================
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ===============================
# 6. Evaluate
# ===============================
y_pred = model.predict(X_test)

print("Final Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# ===============================
# 7. Feature Importance
# ===============================
print("\nFeature Importance:")
importances = model.feature_importances_
for i, imp in enumerate(importances):
    print(f"Feature {i}: {imp:.4f}")

# ===============================
# 8. Save Model
# ===============================
joblib.dump(model, "silent_voice_final_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("\nFinal model saved successfully.")