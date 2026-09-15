import sys
import json
import joblib

from breakguard.parser import load_schema
from breakguard.differ import diff_schemas
from breakguard.rules import assign_risk, overall_risk, describe_change

MODEL_PATH = "breakguard/risk_model.joblib"
VECTORIZER_PATH = "breakguard/vectorizer.joblib"


def load_ml_components():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def add_ml_predictions(changes: list[dict], model, vectorizer) -> None:
    for change in changes:
        description = describe_change(change)
        vector = vectorizer.transform([description])
        change["ml_risk"] = model.predict(vector)[0]
        change["description"] = description


def run(old_path: str, new_path: str) -> dict:
    old_schema = load_schema(old_path)
    new_schema = load_schema(new_path)

    changes = diff_schemas(old_schema, new_schema)
    assign_risk(changes)

    model, vectorizer = load_ml_components()
    add_ml_predictions(changes, model, vectorizer)

    return {
        "overall_risk": overall_risk(changes),
        "changes": changes,
    }


def print_report(report: dict) -> None:
    print(f"Overall risk (rules): {report['overall_risk']}")
    print(f"Changes detected: {len(report['changes'])}")
    for change in report["changes"]:
        agree = "✓" if change["risk"] == change["ml_risk"] else "✗ DISAGREEMENT"
        print(f"  [rule: {change['risk']} | ml: {change['ml_risk']}] {agree}")
        print(f"    {change['description']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m breakguard.main <old_schema.json> <new_schema.json>")
        sys.exit(1)

    old_path, new_path = sys.argv[1], sys.argv[2]
    result = run(old_path, new_path)

    print_report(result)

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)