from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib, os
X = [
  "reset your password at this link",
  "verify account now",
  "download invoice",
  "meeting at 3pm",
  "lunch tomorrow",
  "see attached notes"
]
y = [1,1,1,0,0,0]
pipe = Pipeline([
  ("tfidf", TfidfVectorizer(stop_words="english")),
  ("lr", LogisticRegression(max_iter=1000))
])
pipe.fit(X, y)
os.makedirs("models", exist_ok=True)
joblib.dump(pipe, "models/model.pkl")
print("Saved models/model.pkl")
