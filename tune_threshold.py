# tune_threshold.py
# Choose the threshold on a VALIDATION set, then check once on the TEST set.
import numpy as np
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

ds = load_dataset("deepset/prompt-injections")
X, y = ds["train"]["text"], ds["train"]["label"]
test_x, test_y = ds["test"]["text"], ds["test"]["label"]

# keep 20% of TRAIN aside as validation
tr_x, val_x, tr_y, val_y = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(tr_x, tr_y)

def report(name, xs, ys, t):
    ys = np.array(ys)
    pred = (model.predict_proba(xs)[:, 1] >= t).astype(int)
    attacks = int((ys == 1).sum())
    normals = int((ys == 0).sum())
    caught = int(((pred == 1) & (ys == 1)).sum())
    false_alarms = int(((pred == 1) & (ys == 0)).sum())
    print(f"{name} threshold {t:.2f} | caught {caught}/{attacks} | "
          f"false alarms {false_alarms}/{normals}")


print("--- Step 1: look at VALIDATION and choose a threshold ---")
for t in [0.2, 0.3, 0.4, 0.5]:
    report("VAL ", val_x, val_y, t)

print("\n--- Step 2: check the TEST set ---")
for t in [0.2, 0.3, 0.4, 0.5]:
    report("TEST", test_x, test_y, t)
    