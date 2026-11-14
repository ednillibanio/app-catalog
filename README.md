English | [Português](README.pt-BR.md)

# Personal app catalog

Reusable standards for application repositories maintained by ednillibanio. The repository is public and independent: application repositories link to the standards they follow, and this repository does not list or track them. The standards state expected outcomes; implementation belongs to each application and to the personal `ci-workflows` repository. No reusable workflow is available from this repository.

- [Standards](docs/standards/README.md) cover contribution, iterations, review, documentation, CI/DevSecOps and the Java/Quarkus backend, and explain how an application uses them.
- [Operator guide](docs/operations/operator-guide.md) explains how to use and maintain this repository.
- [Iterations](iterations/README.md) track planned work and evidence.
- [Provenance](PROVENANCE.md) records the design references.

This repository uses `main`. Application repositories keep their stricter local rules, exceptions and integration branches in their own repositories.

## Validation

From the repository root, check local Markdown links and language pairs with `python3 scripts/check_docs.py` (see the [operator guide](docs/operations/operator-guide.md#maintain-both-languages)) and verify iteration links and evidence before review.

Licensed under [Apache License 2.0](LICENSE).
