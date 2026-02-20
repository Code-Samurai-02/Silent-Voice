import joblib
import numpy as np

# Load trained model and label encoder
model = joblib.load("alphabet_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

def predict_alphabet(x, y, z):
    # Create feature array
    features = np.array([[x, y, z]])
    
    # Predict
    prediction = model.predict(features)
    
    # Convert back to letter
    alphabet = label_encoder.inverse_transform(prediction)
    
    return alphabet[0]

# -------- Manual Input --------
if __name__ == "__main__":
    x = float(input("Enter x: "))
    y = float(input("Enter y: "))
    z = float(input("Enter z: "))
    
    result = predict_alphabet(x, y, z)
    print("Predicted Alphabet:", result)