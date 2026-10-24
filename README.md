# Prompt-Injection Firewall for AI Agents

A two-layer firewall that protects an AI agent from prompt injection
(hidden instructions inside emails or web pages).

- **Layer 1 (input check):** rules + a machine-learning classifier scan the text
  and return `block`, `safe_mode` or `allow`.
- **Layer 2 (action check):** before the agent runs a risky action (for example,
  sending an email), a permission check allows only trusted domains.

Even if Layer 1 misses an attack, Layer 2 can stop the dangerous action.

## Results (our tests)

| Test | Result |
|---|---|
| Rules only, 5 reworded attacks | 2/5 caught, 0/4 false alarms |
| Rules + ML, same test | 5/5 caught, 0/4 false alarms |
| Harder test after adding hard normal examples | 8/8 caught, 1/8 false alarms |
| Public dataset (116 test examples) | accuracy 0.86, attack precision 0.98, attack recall 0.75 |
| Automated tests (pytest) | 4 passed |

Lowering the threshold catches more attacks but blocks more normal emails
(see `tune_threshold.py`).

## How to run

```
py -3.13 -m venv venv313
venv313\Scripts\activate
pip install -r requirements.txt
python train_classifier.py
python victim_agent.py        # the attack works on an unprotected agent
python protected_agent.py     # the firewall blocks it
python layered_demo.py        # both layers together
python -m pytest tests        # automated tests
python evaluate_public.py     # public dataset (needs internet)
python tune_threshold.py      # threshold trade-off (needs internet)
uvicorn api:app --reload      # web service, open http://127.0.0.1:8000/docs
```

Docker (Docker Desktop must be running):

```
docker build -t prompt-firewall .
docker run -p 8000:8000 prompt-firewall
```

## Files

| File | Purpose |
|---|---|
| `victim_agent.py` | simple agent with no protection |
| `firewall.py` | Layer 1 rules |
| `training_data.py`, `train_classifier.py` | training data and ML model |
| `permissions.py` | Layer 2 permission check |
| `layered_demo.py` | both layers together |
| `api.py` | FastAPI web service |
| `tests/test_security.py` | automated tests |
| `evaluate_public.py`, `tune_threshold.py`, `three_zone_test.py` | public-dataset evaluation |
| `.github/workflows/ci.yml` | GitHub Actions (runs the tests) |
| `Dockerfile` | container image |

## Limitations (honest)

- The agent in the demo is simulated, not a real AI agent.
- Our own training data is small (70 examples), so our own test results are optimistic.
- The public dataset contains German text, which lowers recall.
- The trusted-domain list can be abused if an attacker uses a trusted domain.
- The Docker image was not tested by the author of this package; build it and check.

## Future work

Embedding-based classifier, connection to a real AI agent, user approval screen
for safe mode, cloud deployment, larger multilingual dataset (Telugu, Hindi).
