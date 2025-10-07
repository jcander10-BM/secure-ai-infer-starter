import os
import joblib
from pathlib import Path
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

_MODEL = None

def _build_fallback_model():
    texts = [
        "reset your password",
        "please reset password",
        "click link to reset",
        "urgent password reset",
        "team lunch tomorrow",
        "hello world",
        "project update attached",
        "standup meeting notes",
    ]
    labels = ["phishing","phishing","phishing","phishing","benign","benign","benign","benign"]
    pipe = make_pipeline(CountVectorizer(), MultinomialNB())
    pipe.fit(texts, labels)
    return pipe

def load_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    model_path = Path(os.getenv("MODEL_PATH", "models/model.pkl"))
    if model_path.exists():
        _MODEL = joblib.load(model_path)
    else:
        _MODEL = _build_fallback_model()
    return _MODEL

def predict(text: str):
    mdl = load_model()
    # Naive Bayes supports predict_proba
    probs = mdl.predict_proba([text])[0]
    idx = probs.argmax()
    label = mdl.classes_[idx]
    score = float(probs[idx])
    return label, score

