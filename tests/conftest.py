import os
import pytest
import joblib
from pathlib import Path
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

@pytest.fixture(scope="session", autouse=True)
def _ensure_model_for_tests(tmp_path_factory):
    """
    Create a tiny text classification pipeline and write it to models/model.pkl,
    then set MODEL_PATH so the app loads it. Runs once per test session.
    """
    # Where we want the model (what app/model.py expects by default)
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "model.pkl"

    # Only (re)build if missing to keep test runs fast
    if not model_path.exists():
        X = [
            "reset your password",
            "please reset your password now",
            "click link to reset password",
            "urgent: password reset required",
            "meeting schedule tomorrow",
            "hello there how are you",
            "team lunch next week",
            "project update attached",
        ]
        y = [1,1,1,1,0,0,0,0]

        pipe = make_pipeline(
            TfidfVectorizer(ngram_range=(1,2), min_df=1),
            LogisticRegression(max_iter=1000)
        )
        pipe.fit(X, y)
        joblib.dump(pipe, model_path)

    # Ensure the app picks up this path
    os.environ["MODEL_PATH"] = str(model_path)

