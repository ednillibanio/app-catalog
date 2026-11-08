# Iteration workflow

A numbered iteration has one master issue and an `iterations/NNN-topic/README.md` with scope, decisions, stages and closure criteria. Each stage has a file under `steps/`, with scope, exclusions, validation, outcome and evidence. The files are the source of truth; the issue tracks progress. Use `todo`, `doing`, `blocked`, `done` and `skipped`, recording reasons for blocked or skipped work.

Plan before execution, review the plan and obtain explicit approval to start each stage. Work one stage at a time. Approvals for actions do not carry over. Track out-of-scope work in an issue or backlog, and close a stage only after validation, review and evidence. Close the iteration only when all stages are done or intentionally skipped, pending work has an owner and issue, and the maintainer authorizes closure. See [templates](../../iterations/_templates/ITERATION.md).
