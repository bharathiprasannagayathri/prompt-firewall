# three_zone_test.py
# Count how many emails fall into each zone on the TEST set.
import numpy as np
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

BLOCK_AT, SAFE_AT = 0.5, 0.4

ds = load_dataset("deepset/prompt-injections")
X, y = ds["train"]["text"], ds["train"]["label"]
test_x, test_y = ds["test"]["text"], np.array(ds["test"]["label"])

tr_x, _, tr_y, _ = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)
model.fit(tr_x, tr_y)
probs = model.predict_proba(test_x)[:, 1]

for label, name in [(1, "ATTACKS"), (0, "NORMALS")]:
    p = probs[test_y == label]
    blocked = int((p >= BLOCK_AT).sum())
    safe_mode = int(((p >= SAFE_AT) & (p < BLOCK_AT)).sum())
    allowed = int((p < SAFE_AT).sum())
    print(f"{name}: total {len(p)} | blocked {blocked} | "
          f"safe-mode {safe_mode} | allowed {allowed}")
