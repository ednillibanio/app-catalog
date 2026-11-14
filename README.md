English | [Português](README.pt-BR.md)

# Personal app catalog

Standards and lightweight inventory for applications maintained by ednillibanio. The catalog states expected outcomes; implementation belongs to each application and, once published, the personal `ci-workflows` repository. No reusable workflow is available from this catalog.

- [Standards](docs/standards/README.md) cover contribution, iterations, review, documentation and CI/DevSecOps.
- [Operator guide](docs/operations/operator-guide.md) explains how to use and maintain this repository.
- [Catalog](catalog/README.md) describes the schema and registered apps.
- [Iterations](iterations/README.md) track planned work and evidence.
- [Provenance](PROVENANCE.md) records the design references.

The catalog uses `main`. App repositories can retain stricter local rules and their own integration branches. The initial adoption is tracked provisionally in [sapl-next #103](https://github.com/ednillibanio/sapl-next/issues/103); the catalog's master issue is [#1](https://github.com/ednillibanio/app-catalog/issues/1).

## Validation

From the repository root, validate `catalog/apps/*.json` against `catalog/app.schema.json` with a JSON Schema Draft 2020-12 validator. Check local Markdown links and language pairs with `python3 scripts/check_docs.py` (see the [operator guide](docs/operations/operator-guide.md#maintain-both-languages)) and verify iteration links and evidence before review. See [catalog validation](catalog/README.md). The schema and entry are data, not evidence of adoption.

Licensed under [Apache License 2.0](LICENSE).
