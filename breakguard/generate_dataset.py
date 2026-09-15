import csv
import random

ENDPOINTS = ["/users", "/users/{id}", "/orders", "/orders/{id}", "/products", "/products/{id}", "/auth/login"]
FIELDS = ["id", "email", "status", "created_at", "amount", "token", "role"]
TYPES = ["integer", "string", "boolean", "array", "object"]

TEMPLATES = [
    ("endpoint '{endpoint}' was removed", "HIGH"),
    ("required field '{field}' was removed from '{endpoint}'", "HIGH"),
    ("field '{field}' type changed from {old_type} to {new_type} in '{endpoint}'", "MEDIUM"),
    ("optional field '{field}' was added to '{endpoint}'", "LOW"),
    ("new endpoint '{endpoint}' was added", "LOW"),
    ("field '{field}' was renamed in '{endpoint}'", "MEDIUM"),
    ("description updated for '{endpoint}'", "LOW"),
]


def generate_row():
    template, risk = random.choice(TEMPLATES)
    text = template.format(
        endpoint=random.choice(ENDPOINTS),
        field=random.choice(FIELDS),
        old_type=random.choice(TYPES),
        new_type=random.choice(TYPES),
    )
    return text, risk


def generate_dataset(n_rows: int, output_path: str):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["description", "risk"])
        for _ in range(n_rows):
            writer.writerow(generate_row())


if __name__ == "__main__":
    generate_dataset(1000, "schemas/training_data.csv")
    print("Dataset generated: schemas/training_data.csv")