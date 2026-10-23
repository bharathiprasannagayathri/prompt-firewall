# firewall.py
# Firewall v1: rule-based scanner for prompt injection.
import re

RULES = [
    ("override_instruction",
     r"ignore (all |your )?(previous|prior|above) instructions"),
    ("send_secret",
     r"send .*(password|passwords|private data|secret|api key)"),
    ("reveal_prompt",
     r"(reveal|show|print) .*(system prompt|hidden instructions)"),
    ("role_change",
     r"(you are now|pretend to be)"),
]

def scan(text):
    """Check the text. Return whether it is safe, and why not."""
    lowered = text.lower()
    findings = []
    for name, pattern in RULES:
        if re.search(pattern, lowered):
            findings.append(name)
    return {"safe": len(findings) == 0, "findings": findings}