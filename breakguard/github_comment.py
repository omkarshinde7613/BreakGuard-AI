import json
import os
import sys

import requests

API = "https://api.github.com"
MARKER = "<!-- breakguard-report -->"


def get_pr_number() -> int:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        return json.load(f)["pull_request"]["number"]


def find_existing_comment(headers: dict, comments_url: str) -> int | None:
    response = requests.get(
        comments_url, headers=headers, params={"per_page": 100}, timeout=30
    )
    response.raise_for_status()
    for comment in response.json():
        if MARKER in comment["body"]:
            return comment["id"]
    return None


def post_report(report_path: str) -> None:
    repo = os.environ["GITHUB_REPOSITORY"]
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }
    comments_url = f"{API}/repos/{repo}/issues/{get_pr_number()}/comments"

    with open(report_path, encoding="utf-8") as f:
        body = f"{MARKER}\n{f.read()}"

    existing_id = find_existing_comment(headers, comments_url)
    if existing_id:
        url = f"{API}/repos/{repo}/issues/comments/{existing_id}"
        response = requests.patch(url, headers=headers, json={"body": body}, timeout=30)
    else:
        response = requests.post(comments_url, headers=headers, json={"body": body}, timeout=30)
    response.raise_for_status()


if __name__ == "__main__":
    post_report(sys.argv[1] if len(sys.argv) > 1 else "report.md")