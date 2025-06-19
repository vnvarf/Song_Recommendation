import joblib

# Load model
model = joblib.load("models/emotion_classifier.pkl")

def detect_emotion(model, text):
    pred = model.predict([text])[0]
    return pred

