# train_classifier.py
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from training_data import ATTACKS, NORMALS

texts = ATTACKS + NORMALS
labels = [1] * len(ATTACKS) + [0] * len(NORMALS)  # 1 = attack, 0 = normal

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2), lowercase=True),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(texts, labels)
joblib.dump(model, "model.joblib")
print(f"Trained on {len(texts)} examples. Saved model.joblib")