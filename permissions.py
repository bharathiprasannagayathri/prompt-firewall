# permissions.py
# Layer 2: check every action BEFORE the agent runs it.

ALLOWED_DOMAINS = {"college.edu", "company.com"}
RISKY_TOOLS = {"send_email", "delete_file", "export_data"}

def check_action(tool, args):
    if tool not in RISKY_TOOLS:
        return {"allowed": True, "reason": "safe tool"}

    if tool == "send_email":
        domain = args.get("to", "").split("@")[-1].lower()
        if domain in ALLOWED_DOMAINS:
            return {"allowed": True, "reason": f"trusted domain: {domain}"}
        return {"allowed": False, "reason": f"external domain: {domain}"}

    return {"allowed": False, "reason": f"{tool} needs human approval"}