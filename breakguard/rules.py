RISK_LEVELS = {
    "endpoint_removed": "HIGH",
    "parameter_removed": "HIGH",
    "parameter_type_changed": "MEDIUM",
    "endpoint_added": "LOW",
}


def assign_risk(changes: list[dict]) -> list[dict]:
    for change in changes:
        change["risk"] = RISK_LEVELS.get(change["type"], "MEDIUM")
    return changes


def overall_risk(changes: list[dict]) -> str:
    if any(c["risk"] == "HIGH" for c in changes):
        return "HIGH"
    if any(c["risk"] == "MEDIUM" for c in changes):
        return "MEDIUM"
    return "LOW" if changes else "NONE"