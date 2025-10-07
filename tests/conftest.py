import os
import joblib
from pathlib import Path
import pytest
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@pytest.fixture(scope="session", autouse=True)
def _bootstrap_model_and_env():
    """
    Make tests self-contained:
    - Ensure API_KEY is set so the app imports cleanly
    - Ensure a small text model exists at models/model.pkl
    - Point MODEL_PATH to that file
    """
    os.environ.setdefault("API_KEY", "demo")

    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "model.pkl"

    if not model_path.exists():
        X = [
            "reset your password",
            "please reset your password now",
            "click link to reset password",
            "urgent password reset required",
            "meeting schedule tomorrow",
            "hello how are you",
            "team lunch next week",
            "project update attached",
        ]
        y = [
            "phishing", "phishing", "phishing", "phishing",
            "benign", "benign", "benign", "benign",
        ]

        pipe = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), min_df=1),
            LogisticRegression(max_iter=1000),
        )
        pipe.fit(X, y)
        joblib.dump(pipe, model_path)

    os.environ["MODEL_PATH"] = str(model_path)

