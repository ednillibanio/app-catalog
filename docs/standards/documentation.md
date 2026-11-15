English | [Português](documentation.pt-BR.md)

# Documentation

Write for a reader unfamiliar with the project. Describe purpose, prerequisites, configuration, commands, effects, validation and troubleshooting when applicable. Establish behavioral claims from implementation, label assumptions and distinguish examples from executed checks. Keep navigation and local links valid. Do not expose credentials or private organization data. Record exceptions and owners as described in the [standards index](README.md).

## Languages

This catalog keeps its reader-facing documents (`README.md`, `CONTRIBUTING.md` and `docs/`) in English and Brazilian Portuguese. `name.md` is the canonical English version and `name.pt-BR.md`, in the same folder, is its translation. Change both in the same pull request and keep every rule, command, link and exception with the same meaning; when they disagree, fix the Portuguese file to match the English one.

Each file starts with a link to the other language. In a Portuguese file, link to the Portuguese version of a translated document and its matching heading; links to English-only files, to non-Markdown files and to external URLs stay as they are. Agent instructions, provenance, iteration records, issues, pull requests and commits are English only. Preserve names and product language where needed.

The catalog does not set an app's product or documentation language. Each app states its language in its own agent instructions and links to the catalog version in that language. Tooling and automation (scripts, task runners, Compose files, `.env.example` and CI workflows) are written in English, one language per file, as the [local development environment](dev-environment.md#10-tooling-language) standard requires.

Each app keeps a language map in its agent instructions: a table that says, for each kind of artifact, which language it uses and why. Contributors then do not have to guess, and a file that mixes languages stands out. For example:

| Artifact | Language | Reason |
| --- | --- | --- |
| Scripts, task runner, Compose files, `.env.example`, CI workflows | English | Tooling commands are in English ([local development environment](dev-environment.md#10-tooling-language)) |
| Code identifiers | The language the app chose | Backend and frontend standards: one vocabulary per app |
| Product text and user messages | The product's language | Users read them |
| Documentation, iterations, issues, pull requests, commit descriptions | The language the app states | Its maintainers and contributors read them |
