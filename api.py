# api.py
# The firewall as a web service.
import joblib
from fastapi.responses import FileResponse
from fastapi import FastAPI
from pydantic import BaseModel
from firewall import scan

app = FastAPI(title="Prompt Injection Firewall")
model = joblib.load("model.joblib")

BLOCK_AT = 0.5
SAFE_AT = 0.5


class ScanRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scan")
def scan_text(req: ScanRequest):
    rules = scan(req.text)
    prob = float(model.predict_proba([req.text])[0][1])

    if not rules["safe"] or prob >= BLOCK_AT:
        decision = "block"
    elif prob >= SAFE_AT:

        decision = "safe_mode"
    else:
        decision = "allow"

    return {
        "decision": decision,
        "ml_score": round(prob, 3),
        "rule_findings": rules["findings"],
    }