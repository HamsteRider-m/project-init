# AI Workflow

This repo uses a 7-mode request protocol. Always identify the mode before acting.

## Modes

| Mode | Trigger | Output |
|---|---|---|
| `scrum` | backlog grooming, scope decisions | updated Scrum.md |
| `plan` | new task or feature design | updated Planning.md + CurrentTask.md |
| `execute` | implement a planned task | code changes + updated Execution.md |
| `verify` | check acceptance criteria | evidence recorded in Execution.md |
| `review` | post-implementation quality gate | Review.md with scores |
| `investigate` | debug a failure or unexpected behavior | Investigate.md with root cause |
| `kb` | capture a reusable decision or finding | KB.md + KnowledgeBase/Index.md |

## Durable State Files

| File | Purpose |
|---|---|
| `CurrentTask.md` | active task: title, scope, acceptance criteria |
| `Planning.md` | step-by-step plan with status |
| `Scrum.md` | backlog |
| `Execution.md` | run log, evidence, blockers |
| `Review.md` | review scores and findings |
| `Investigate.md` | debug investigations |
| `KB.md` | knowledge base entries |

## Gates

**Implementation gate**: a task entry in CurrentTask.md AND a plan in Planning.md must exist before writing code.

**Verification gate**: acceptance criteria evidence must be recorded in Execution.md before claiming completion. Evidence = actual command output, not assertions.
