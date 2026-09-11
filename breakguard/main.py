import sys
import json

from breakguard.parser import load_schema
from breakguard.differ import diff_schemas
from breakguard.rules import assign_risk, overall_risk


def run(old_path: str, new_path: str) -> dict:
    old_schema = load_schema(old_path)
    new_schema = load_schema(new_path)

    changes = diff_schemas(old_schema, new_schema)
    assign_risk(changes)

    return {
        "overall_risk": overall_risk(changes),
        "changes": changes,
    }


def print_report(report: dict) -> None:
    print(f"Overall risk: {report['overall_risk']}")
    print(f"Changes detected: {len(report['changes'])}")
    for change in report["changes"]:
        print(f"  [{change['risk']}] {change['type']} — {change.get('endpoint', '')} {change.get('parameter', '')}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m breakguard.main <old_schema.json> <new_schema.json>")
        sys.exit(1)

    old_path, new_path = sys.argv[1], sys.argv[2]
    result = run(old_path, new_path)

    print_report(result)

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)