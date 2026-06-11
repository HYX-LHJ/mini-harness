# todo / PROGRESS / DECISIONS

## todo.md

Current weekly task board — **register changes before making them**.

```markdown
# Current weekly task board

**This week**: YYYY-MM-DD ~ YYYY-MM-DD

Historical weekly tasks: [backlog/archive.md](backlog/archive.md).

---
YYYY-MM-DD

task: <one-line task name>

- [ ] Checkable acceptance item 1
- [ ] Checkable acceptance item 2
```

Rules:

- Each `task:` must have checkable, verifiable sub-items.
- Mark `[x]` when done; when all sub-items under a task are `[x]`, `sync_progress.py` rolls it into PROGRESS "Completed".
- Cross-week archive: project `archive_harness_todo.py` or manually move to `backlog/archive.md`.
- **Weekly review** (first session each Monday): Agent organizes readable surface to active state per `docs/weekly-review.md`.

## PROGRESS.md

### Mechanical sections (sync_progress.py or manual)

- Latest git info
- Test status
- lint
- Completed (fully checked tasks this week)
- In progress (tasks with unchecked sub-items)

### Human-written sections (Main Agent each round)

| Section | How to write |
|---------|--------------|
| **Current state** | ≤5 bullets; what a new session needs in 30 seconds; **not** a changelog |
| **Next steps** | Near-term intent (deploy, integration, pending Plan); **need not** go in todo; remove when done |
| **Known issues** | Only **open** P0/P1/P2; if none, write "None" |

**After commit/push** you must refresh again so "Current state" matches git hashes.

## DECISIONS.md

Active constraints; target ~15–25 entries.

**Add when**: changes how code is written, API contracts, query semantics, deploy constraints.  
**Archive**: superseded → `backlog/decisions-archive.md`.  
**Format**: dated heading + rationale + rejected alternatives + constraint bullets.

Normal feature delivery goes in `plans/` + `todo.md`; not every commit needs DECISIONS.
