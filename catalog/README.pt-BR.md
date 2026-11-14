[English](README.md) | Português

# Catálogo de apps

Cada arquivo em `apps/` é um objeto JSON validado contra o [app.schema.json](app.schema.json), com JSON Schema Draft 2020-12. `status` descreve a adoção, não a saúde da aplicação. `owner` identifica o mantenedor responsável; `tracking_issue` aponta para o trabalho. As exceções ficam no registro do próprio app e devem ter os campos exigidos pelo schema.

Na raiz do repositório, com Python 3 e o pacote `jsonschema` instalados no ambiente escolhido, rode:

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

Saída com status zero significa que todas as entradas encontradas são válidas; a validade do schema não prova o que uma entrada afirma.
