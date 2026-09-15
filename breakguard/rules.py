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

def describe_change(change: dict) -> str:
    change_type = change["type"]
    endpoint = change.get("endpoint", "")
    parameter = change.get("parameter", "")

    if change_type == "endpoint_removed":
        return f"endpoint '{endpoint}' was removed"
    if change_type == "endpoint_added":
        return f"new endpoint '{endpoint}' was added"
    if change_type == "parameter_removed":
        return f"required field '{parameter}' was removed from '{endpoint}'"
    if change_type == "parameter_type_changed":
        return f"field '{parameter}' type changed from {change.get('old_type')} to {change.get('new_type')} in '{endpoint}'"

    return f"{change_type} in '{endpoint}'"