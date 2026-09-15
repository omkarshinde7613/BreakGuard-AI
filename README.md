# BreakGuard AI

An open-source tool that detects breaking changes in API schemas (OpenAPI/JSON) between two versions, scores their risk, and reports them — combining a rule-based engine with a machine learning classifier.

## How it works

1. **Rule-based diffing** — parses two OpenAPI schema files and detects structural changes (removed endpoints, removed/changed parameters, added endpoints).
2. **Risk scoring** — assigns HIGH/MEDIUM/LOW risk to each change type based on real-world impact.
3. **ML classification** — an independently trained Logistic Regression model (TF-IDF features) predicts risk from the change description, run alongside the rule engine for cross-validation.

## Usage

\`\`\`bash
python -m breakguard.main schemas/old.json schemas/new.json
\`\`\`

Outputs a terminal report and saves a full `report.json`.

## Limitations / Future Work

- Training data is currently synthetic (template-generated), not real-world PRs — planned for Phase 3 alongside GitHub integration.
- The ML model currently classifies text *derived from* the rule engine's own output rather than the raw diff — meaning the two layers aren't fully independent yet. A future version will train directly on raw diff text.
- Next: GitHub Action integration to comment risk reports directly on pull requests.