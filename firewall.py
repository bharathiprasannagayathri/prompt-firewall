# firewall.py
# Firewall v1: rule-based scanner for prompt injection.
import re


RULES = [
    ("override_instruction",
     r"\b(ignore|disregard|forget|override)\s+(all\s+|your\s+)?(previous|prior|above|earlier)\s+(instructions|rules)\b"),
    ("send_secret",
     r"\b(send|share|reveal|email|forward|export|leak)\b.{0,100}\b(passwords?|private data|secrets?|api keys?|tokens|credentials)\b"),
    ("reveal_prompt",
     r"\b(reveal|show|print|expose|disclose)\b.{0,100}\b(system prompt|hidden instructions|secret instructions)\b"),
    ("role_change",
     r"\b(you are now an unrestricted assistant|pretend to be an unrestricted assistant|act as an unrestricted assistant)\b"),
]

def scan(text):
    """Check the text. Return whether it is safe, and why not."""
    lowered = text.lower()
    findings = []
    for name, pattern in RULES:
        if re.search(pattern, lowered):
            findings.append(name)
    return {"safe": len(findings) == 0, "findings": findings}