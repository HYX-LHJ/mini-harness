# Harness weekly review (Agent)

**Goal**: Ensure everything the Agent reads each round in harness is **actively relevant** — no stale conclusions, no closed tech debt, no historical tasks piled in entry files.

**Executor**: Main Agent reads this document and **writes each item to disk**; no dedicated "weekly review script" replaces judgment. You may dispatch an **explore** Subagent to compare `src/`, deployment, and external docs to verify "active" still holds.

**Triggers** (see root [AGENTS.md](../../AGENTS.md) "Weekly review round"):

- **Every Monday**, the **first Agent session that day** in this repo — weekly review before any other user task.
- **First session of a new calendar week** on a non-Monday if last week was skipped — same requirement.
- User may say "run harness weekly review" anytime; user may explicitly "skip this week's review" to skip.

Regular rounds still follow [AGENTS.md](../../AGENTS.md); this is an **additional** once-per-week archive round.

---

## Round order

1. **Gates (before)** — `lint_src.py` + `pytest`
2. **Register** in [todo.md](../todo.md): `task: harness weekly review (YYYY-MM-DD)`, sub-items per §2 tables below (checkable `- [ ]`)
3. **Process each table row** — move inactive content out first, then rewrite active files
4. **Cross-week todo** — from repo root: `python harness/scripts/archive_harness_todo.py` (moves last week and earlier tasks to [backlog/archive.md](../backlog/archive.md))
5. **`sync_progress.py`** — refresh PROGRESS mechanical sections
6. **Hand-write** PROGRESS "Current state", "Next steps", "Known issues"; add to "Current state": `Harness weekly review completed this week (YYYY-MM-DD)`
7. **Gates (after)** — same as step 1
8. **Check off** todo sub-items; brief user summary: what was archived, what remains active

**This round does not change `src/` by default** (unless the user opens a separate implementation task).

---

## Agent-readable surface — active vs archive

Paths below are the full harness surface an Agent **may read in a regular round** (L0 entry + each `index.md`). Weekly review must ensure: **active files on the left contain none of the "should move out" content on the right**.

### L0 — per-round entry

| Active file | Keep only | Move to | Weekly review action |
|-------------|-----------|---------|----------------------|
| [todo.md](../todo.md) | **Current calendar week** unchecked / checked tasks | [backlog/archive.md](../backlog/archive.md) | Run `archive_harness_todo.py`; confirm no last-week date blocks remain |
| [PROGRESS.md](../PROGRESS.md) § Current state | ≤5 bullets: **current** status and blockers | (delete, do not archive) | Remove delivered/shipped/no-longer-relevant sentences; not a changelog |
| [PROGRESS.md](../PROGRESS.md) § Next steps | Still-valid intent for next 1–2 weeks | (delete, do not archive) | Remove done items; user-confirmed "won't do" → mark deferred + link plan; need not all go to todo |
| [PROGRESS.md](../PROGRESS.md) § Known issues | **open / deferred / observe** P0–P2 only | Closed → open-findings archive | Align with open-findings **active table** row by row; if none, write "None" |
| [PROGRESS.md](../PROGRESS.md) § Completed | **This week** fully checked task names (mechanical) | Earlier → backlog/archive | Via archive script; do not hand-stack history |
| [PROGRESS.md](../PROGRESS.md) § In progress | Tasks with unchecked sub-items (mechanical) | — | Via sync; confirm matches todo |
| [DECISIONS.md](../DECISIONS.md) | Entries still constraining implementation (~15–25) | [backlog/decisions-archive.md](../backlog/decisions-archive.md) | Superseded / historical-only → archive; merge same-topic entries |

### Plans and reviews

| Active file | Keep only | Move to | Weekly review action |
|-------------|-----------|---------|----------------------|
| [plans/index.md](../plans/index.md) | Not implemented, **awaiting user confirmation**, or still affecting schedule | Body kept; index marked "implemented" | Mark implemented; long "pending confirmation" → confirm with user to close or continue |
| [code_review/open-findings.md](../code_review/open-findings.md) | **open / deferred / observe** rows | [open-findings-closed.md](../code_review/open-findings-closed.md) | Move all **closed** rows and `<details>` history blocks out; no placeholder + real row duplication in main table |
| [code_review/index.md](../code_review/index.md) | Last **4 weeks** of report index (~15–20 rows) | [archive-index.md](../code_review/archive-index.md) | Move older table rows down; **do not delete** report `.md` bodies |
| [code_simplifier/index.md](../code_simplifier/index.md) | Last 4 weeks index | Optional `archive-index.md` or backlog note | Same — index table only |

### Indexes and integration docs

| Active file | Keep only | Move to | Weekly review action |
|-------------|-----------|---------|----------------------|
| [index.md](../index.md) | Entry text, **active** maintenance conventions | — | Check no broken links, no duplicate/contradictory rules |
| [docs/index.md](index.md) | Currently valid doc links | — | Remove links to deleted docs |
| Project integration docs (e.g. `docs/api_*.md`) | Matches **current** external contract | — | If DECISIONS / `src/` changed but docs did not → register todo or fix docs this round |
| [plans/*.md](../plans/) bodies | Full text of open plans | — | Mark implemented plans at top; do not delete files |

### Read-only archive (Agent **should not** treat as primary context after weekly review)

| Path | Description |
|------|-------------|
| [backlog/archive.md](../backlog/archive.md) | Historical weekly todos |
| [backlog/decisions-archive.md](../backlog/decisions-archive.md) | Superseded decisions |
| [code_review/open-findings-closed.md](../code_review/open-findings-closed.md) | Closed findings |
| [code_review/archive-index.md](../code_review/archive-index.md) | Historical review index |
| `code_review/YYYY-MM-DD_*.md` | Review bodies (lookup via index, not read every round) |

---

## Acceptance checklist (self-check before done)

- [ ] New session reading L0 + active indexes only can decide in **30 seconds**: what to do, what's blocked, what debt remains
- [ ] open-findings **main table** has no `closed` rows, no large `<details>` history blocks
- [ ] PROGRESS "Known issues" **matches** open-findings active rows
- [ ] PROGRESS "Current state / Next steps" has **no** recap of already-delivered features
- [ ] DECISIONS count is manageable; no constraints **overturned by code**
- [ ] todo contains **this week** task blocks only
- [ ] `archive_harness_todo.py` ran (or equivalent manual archive)
- [ ] `sync_progress.py` ran; all gates green

---

## Project reality check (required judgment)

Archiving is not just cut-and-paste — compare against **current** repo and runtime:

| Check | How |
|-------|-----|
| Tech debt still valid? | deferred / observe vs `src/`, tests, [DECISIONS.md](../DECISIONS.md), project integration docs (e.g. `docs/api_*.md`) |
| Decisions still constrain? | Already implemented in code/docs → merge or archive duplicate decisions |
| Plan still pending? | "Awaiting user confirmation" > 30 days → confirm with user |
| Deploy / DDL gaps | Still blocking → keep in PROGRESS "Current state"; done → remove |
| Integration/deploy assumptions | Do doc assumptions match production and upstream? |

Optional: Task **explore** scans `src/` by module; report only **contradictions** with harness — do not read full diffs.

---

## Do not

- **Do not** delete `code_review/*.md` or `plans/*.md` bodies (only index tables and open-findings main table).
- **Do not** copy closed items back into PROGRESS or todo.
- **Do not** change `src/` in a weekly review round (unless user opens a separate task).
- **Do not** bulk-edit prose with scripts instead of the table above — `archive_harness_todo.py` / `sync_progress.py` only handle todo week boundaries and PROGRESS mechanical sections.
