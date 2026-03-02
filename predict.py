import numpy as np
import joblib

# ===============================
# 1. Load Model and Encoder
# ===============================
model = joblib.load("silent_voice_model.pkl")
le = joblib.load("label_encoder.pkl")

# ===============================
# 2. Normalize Each Finger Vector
# ===============================
def normalize_fingers(sample):
    sample = np.array(sample).reshape(1, -1)
    for i in range(0, 15, 3):
        norm = np.linalg.norm(sample[:, i:i+3], axis=1, keepdims=True)
        norm[norm == 0] = 1
        sample[:, i:i+3] = sample[:, i:i+3] / norm
    return sample

# ===============================
# 3. Prediction
# ===============================
def predict_alphabet(values):
    sample = normalize_fingers(values)
    prediction = model.predict(sample)
    probabilities = model.predict_proba(sample)

    alphabet = le.inverse_transform(prediction)[0]
    confidence = np.max(probabilities) * 100

    return alphabet, confidence


# ===============================
# 4. Input Format
# ===============================
if __name__ == "__main__":

    print("\nPaste 15 values in this format:")
    print("thumb_x,thumb_y,thumb_z,index_x,index_y,index_z,"
          "middle_x,middle_y,middle_z,ring_x,ring_y,ring_z,"
          "pinky_x,pinky_y,pinky_z\n")

    line = input("Enter values: ")

    try:
        values = [float(v.strip()) for v in line.split(",")]

        if len(values) != 15:
            raise ValueError("You must enter exactly 15 values.")

        letter, confidence = predict_alphabet(values)

        print("\n==============================")
        print("Predicted Alphabet:", letter)
        print(f"Confidence: {confidence:.2f}%")
        print("==============================")

    except Exception as e:
        print("Error:", e)