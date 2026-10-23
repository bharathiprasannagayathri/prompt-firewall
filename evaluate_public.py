# evaluate_public.py
# Test on a public dataset, with a proper train/test split.
import joblib
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline

ds = load_dataset("deepset/prompt-injections")
train_x, train_y = ds["train"]["text"], ds["train"]["label"]
test_x, test_y = ds["test"]["text"], ds["test"]["label"]
print(f"Train: {len(train_x)} examples | Test: {len(test_x)} examples")

# A) Our current model (trained on our own 70 examples)
ours = joblib.load("model.joblib")
print("\n=== A) Our small model on the public TEST set ===")
print(classification_report(test_y, ours.predict(test_x),
                            target_names=["normal", "attack"], zero_division=0))

# B) A model trained on the public TRAIN set
big = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
big.fit(train_x, train_y)
print("=== B) Model trained on the public TRAIN set ===")
print(classification_report(test_y, big.predict(test_x),
                            target_names=["normal", "attack"], zero_division=0))