# Operator guide

This repository defines standards and records which personal applications adopt them. It does not run application builds or host reusable CI workflows; those belong to each app and the published `ci-workflows` repository. This catalog consumes its versioned pre-commit hooks locally.

## Prepare a checkout

Install Git. Clone the public repository and enter its directory:

```sh
git clone https://github.com/ednillibanio/app-catalog.git
cd app-catalog
```

The integration branch is `main`. To contribute, first identify an issue in this repository; cross-repository work should also have an issue in each affected repository, linked to the master issue. Create a short topic branch from the current `main`, make one focused change, validate it, and open a pull request to `main`. Do not edit application code from this catalog checkout.

## Run repository hooks

Install Git, Python 3, and `pre-commit` (for example, `pipx install pre-commit`). From the repository root, install the Git hook and validate all tracked files:

```sh
pre-commit install
pre-commit run --all-files
```

The `.pre-commit-config.yaml` pins `sem-env`, `check-exec-bit`, and `check-shdoc` to the published `ci-workflows` tag `v0.1.0`. Keep real environment files out of the repository; only `.env.example` and `.env.prod.example` are allowed. The shell checks validate executable modes and documentation headers when shell scripts are present.

## Inspect app adoption

Each `catalog/apps/*.json` file describes an app's repository, accountable owner, adoption status, tracking issue, and any documented exceptions. `planned`, `in-progress`, and `adopted` describe catalog adoption only; they do not report application health or prove that a CI workflow ran. Check the linked issue and evidence before relying on a status. Exceptions must state scope, reason, owner, review date, and issue.

## Validate catalog data and links

Use Python 3 with the `jsonschema` package installed. From the repository root, run:

```sh
python - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

schema = json.loads(Path("catalog/app.schema.json").read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
for entry in Path("catalog/apps").glob("*.json"):
    validator.validate(json.loads(entry.read_text()))
    print(f"Valid: {entry}")
PY
```

A successful run prints each valid entry and exits with status 0. Invalid JSON or a schema violation raises an error and exits nonzero. Validate local Markdown links as part of review; this repository does not yet provide an automated link-check command.

## Maintain standards and iterations

Start with [the standards index](../standards/README.md). The iteration workflow defines plan files, status values, stage approvals, evidence and closure. Keep accepted unplanned work in [`iterations/BACKLOG.md`](../../iterations/BACKLOG.md), with an owner and issue. Update both the iteration record and its master issue checklist when stage status changes. Keep pending work visible until resolved; do not mark a stage done while its acceptance criteria remain unmet.

## Troubleshooting

- `ModuleNotFoundError: No module named 'jsonschema'`: install `jsonschema` into the Python environment used for validation, then rerun the command.
- Schema validation fails: check required fields and the allowed `status` values in [`catalog/app.schema.json`](../../catalog/app.schema.json); validate URLs and exception fields.
- An adoption status looks stale: inspect the tracking issue and ask its owner to update the catalog with current evidence.
- A link is broken: correct the source Markdown or catalog URL and rerun the relevant validation before opening the PR.

## Current limitations

The catalog has no automated CI or link checker. Its pre-commit hooks run locally; they do not replace a GitHub Actions workflow. The reusable workflows are published, but a real sapl-next consumer PR remains to be validated in stage 03. Linux and Windows validation are not claimed.
