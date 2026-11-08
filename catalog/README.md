# App catalog

Each file under `apps/` is a JSON object validated against [app.schema.json](app.schema.json), using JSON Schema Draft 2020-12. `status` describes adoption, not application health. `owner` identifies the accountable maintainer; `tracking_issue` links the work. Exceptions belong in the app's own tracked record and must have the fields required by the schema.

From the repository root, with Python 3 and the `jsonschema` package installed in your chosen environment, run:

```sh
python - <<'PYCODE'
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

schema = json.loads(Path("catalog/app.schema.json").read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
for entry in Path("catalog/apps").glob("*.json"):
    validator.validate(json.loads(entry.read_text()))
    print(f"Valid: {entry}")
PYCODE
```

A zero exit status means all discovered entries validate; schema validity does not prove the claims in an entry.
