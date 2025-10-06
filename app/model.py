import joblib, os
_model = None
def load_model():
    global _model
    if _model is None:
        _model = joblib.load(os.getenv("MODEL_PATH","models/model.pkl"))
    return _model
def predict(text: str):
    mdl = load_model()
    proba = float(mdl.predict_proba([text])[0][1])
    label = "phishing" if proba >= 0.5 else "benign"
    return label, proba
