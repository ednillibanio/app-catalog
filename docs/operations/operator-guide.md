English | [Português](operator-guide.pt-BR.md)

# Operator guide

This repository defines reusable standards for application repositories. It does not track the applications that use them, run application builds or host reusable CI workflows; those belong to each app and the published `ci-workflows` repository. This catalog consumes its versioned pre-commit hooks locally.

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

## Validate links

Validate local Markdown links as part of review with the check in [Maintain both languages](#maintain-both-languages); no CI job runs it yet.

## Maintain standards and iterations

Start with [the standards index](../standards/README.md). The iteration workflow defines plan files, status values, stage approvals, evidence and closure. Keep accepted unplanned work in [`iterations/BACKLOG.md`](../../iterations/BACKLOG.md), with an owner and issue. Update both the iteration record and its master issue checklist when stage status changes. Keep pending work visible until resolved; do not mark a stage done while its acceptance criteria remain unmet.

## Maintain both languages

Reader-facing documents exist in English (`name.md`, canonical) and Brazilian Portuguese (`name.pt-BR.md`); the [documentation standard](../standards/documentation.md#languages) defines which files are bilingual and how they link. When you change one, change the other in the same pull request with the same meaning. To add a document, create both files, each starting with the language switch, and link the Portuguese one from the other Portuguese pages.

Python 3 and Git are required. From the repository root, check the language pairs, relative links and anchors of all Markdown files, including untracked ones:

```sh
python3 scripts/check_docs.py
```

A clean run prints `OK:` with the number of language pairs and exits with status 0. Otherwise it lists each missing pair, missing language switch, heading-count mismatch, broken link or anchor, or Portuguese page that links to the English version of a translated document, and exits with status 1. It understands inline links (with an optional title and one level of parentheses in the destination), angle-bracket destinations and reference definitions, decodes percent-encoded paths and anchors, and ignores fenced code blocks and inline code. Indented code blocks are read as text and Setext headings (underlined with `===` or `---`) are not recognized, so use fenced blocks and `#` headings. The check compares structure, not meaning: review each changed pair side by side before requesting review.

## Troubleshooting

- A link is broken: correct the source Markdown and rerun the relevant validation before opening the PR.
- The language check reports a missing pair or a heading-count mismatch: create or complete the other language's file so both have the same sections, then rerun the check.

## Current limitations

The catalog has no automated CI. Its pre-commit hooks and the language and link check (`scripts/check_docs.py`) run locally; they do not replace a GitHub Actions workflow. Linux and Windows validation are not claimed.
