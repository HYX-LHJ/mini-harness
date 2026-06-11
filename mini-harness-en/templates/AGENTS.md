# {{PROJECT_NAME}} — Agent Playbook

For agents: what to do each round, when to stop, where artifacts go. **Skill details live in each Skill**; this file only orchestrates and enforces hard constraints.

**Priority**: this file > Skills. Do not skip todo registration, do not bypass lint + pytest gates, **any change to `{{SRC_DIR}}/` must include tests** (no exceptions).

---

## Role split

| Role | Responsibility |
|------|----------------|
| **Main Agent** (current session) | Gates, `harness/todo.md` / `PROGRESS.md`, implementation and small fixes, user summary |
| **Subagent** (Cursor **Task**) | **code-review**, **code-simplifier**, codebase exploration, large-context reconnaissance; Main Agent registers → dispatches → collects → **writes to disk** |

**Forbidden**: Main Agent reads a large diff in chat and writes the full review/refinement report body (Subagent owns that; Main Agent only organizes on-disk artifacts and user summary).

---

## Flow overview

Each user input = one round. Start with a **regular round**; when the user asks to commit, append a **commit round** after regular wrap-up.

```
Regular: gates(before) → read harness → [Plan] → register todo → [change {{SRC_DIR}}/? → start tdd] → implement → [code-review] → gates(after) → PROGRESS

Weekly review: gates(before) → weekly-review.md → archive/rewrite harness → archive_harness_todo + sync_progress → gates(after) → PROGRESS

Commit: …regular wrap-up… → code-simplifier → second code-review → commit {{DEV_BRANCH}} → sync {{TEST_BRANCH}} → refresh PROGRESS again
```

| Path | Trigger | Extra steps |
|------|---------|-------------|
| **Regular round** | Every user input | Changing `{{SRC_DIR}}/` requires tdd right after todo; code-review at wrap-up |
| **Weekly review round** | **First session on Monday**, or first session of a new calendar week if last week was skipped | Read [weekly-review.md](harness/docs/weekly-review.md) first; process harness per active/archive checklist; then user tasks |
| **Commit round** | "commit", "push", etc. | Delivery with `{{SRC_DIR}}/` needs simplify + second code-review, then Git workflow |

**Weekly review hard constraint**: When triggered, **complete weekly review first** before registering/executing other user tasks (unless user explicitly says "skip this week's review"). Details: [harness/docs/weekly-review.md](harness/docs/weekly-review.md).

---

## Skill triggers

| Skill | When | Executor | Skip when |
|-------|------|----------|-----------|
| **`tdd`** | **After** todo registration, **before** changing `{{SRC_DIR}}/` | Main Agent | This round does not change `{{SRC_DIR}}/` |
| **`code-review-expert`** | Changed `{{SRC_DIR}}/` this round (wrap-up) | **Subagent** | Did not change `{{SRC_DIR}}/`, or user explicitly skips |
| **`code-simplifier`** | User asks to commit and delivery includes `{{SRC_DIR}}/` | **Subagent** | Harness docs/scripts only |
| **`code-review-expert`** (second) | After `code-simplifier`, before commit | **Subagent** | Same as code-simplifier |

---

## Subagent artifacts (hard constraints)

The round **must not wrap up** until these are done (commit round: no `git commit` without reports).

### code-review-expert

1. **Dispatch**: Task + this round's diff + `code-review-expert` Skill.
2. **Body**: Structured review (severity; verdict APPROVE / REQUEST_CHANGES / COMMENT).
3. **Write to disk** (Main Agent, **required**):
   - `harness/code_review/YYYY-MM-DD_topic-summary.md`
   - Add row at top of [code_review/index.md](harness/code_review/index.md)
   - Open **P0/P1** → [open-findings.md](harness/code_review/open-findings.md)
4. **Forbidden**: chat-only instead of on-disk artifacts.

### code-simplifier

1. **Dispatch**: Task + pending-commit `{{SRC_DIR}}/` diff + `code-simplifier` Skill.
2. **Execute**: Subagent simplifies code and summarizes changes.
3. **Write to disk** (Main Agent, **required**):
   - `harness/code_simplifier/YYYY-MM-DD_topic-summary.md`
   - Add row at top of [code_simplifier/index.md](harness/code_simplifier/index.md)
4. **Follow-up**: re-run gates after refinement; `{{SRC_DIR}}/` changes need second code-review.

---

## Regular round

### 1. Gates (before)

If gates fail, **fix gates only** — do not advance the user's task.

```powershell
{{LINT_CMD}}
{{PYTEST_CMD}}
```

### 2. Read context

If this round is a **weekly review round** (see table above), **first** read and execute [harness/docs/weekly-review.md](harness/docs/weekly-review.md), then read the files below.

`harness/PROGRESS.md`, `harness/todo.md`; before major tasks [plan-mode.md](harness/docs/plan-mode.md); architecture boundaries `harness/DECISIONS.md`.

### 3. Plan (major tasks)

When plan-mode triggers apply → `harness/plans/` → **wait for user confirmation** → then register todo. **Do not change `{{SRC_DIR}}/` before confirmation**.

### 4. Register todo

Any change must be registered in `harness/todo.md` first.

### 5. Start tdd → implement (when changing `{{SRC_DIR}}/`)

1. **Immediately** enable **tdd** Skill after todo registration; **do not** change `{{SRC_DIR}}/` first and add tests later.
2. `harness/tests/` first → then `{{SRC_DIR}}/`.
3. Changing only `{{SRC_DIR}}/` without tests: cannot wrap up or commit.

### 6. Wrap-up

- Changed `{{SRC_DIR}}/` → Task + code-review-expert → write to `harness/code_review/`
- Check todo → gates (after)
- `sync_progress.py` → hand-write PROGRESS (see [harness/index.md](harness/index.md))

---

## Commit round

### A. Pre-commit refinement (cannot skip when `{{SRC_DIR}}/` included)

1. code-simplifier → write to disk → gates
2. Second code-review-expert → write to disk
3. Harness-only delivery may skip

### B. Git workflow ({{DEV_BRANCH}} → {{TEST_BRANCH}})

1. Confirm on `{{DEV_BRANCH}}`
2. `git status` / `git diff` — exclude secrets and local integration scratch
3. All gates green → commit → push `{{DEV_BRANCH}}`
4. Merge `{{TEST_BRANCH}}` → push → return to `{{DEV_BRANCH}}`
5. After push: `sync_progress.py` + hand-write PROGRESS

### Commit discipline

- `{{DEV_BRANCH}}` first, then `{{TEST_BRANCH}}`
- Default do-not-commit: secrets, `.env` values, `harness/out/`, `harness/pre/`, unrequested integration code
- Project-specific do-not-commit paths go in `harness/DECISIONS.md`

---

## Testing and verification

| Stage | Requirement |
|-------|-------------|
| **Writing** | Changing `{{SRC_DIR}}/` requires tdd first; tests and implementation delivered together |
| **Running** | Run gates at start and end of each round |
| **Scope** | Default `pytest` excludes `@pytest.mark.integration` |

## Quality gates

| Command | Scope |
|---------|-------|
| `harness/scripts/lint_src.py` | `{{SRC_DIR}}/` (ruff + pyright) |
| `pytest` | Unit tests in `harness/tests/` |

On failure: do not advance the task; fix until green, then restart from gates (before). Details: [harness/index.md](harness/index.md).

---

## Harness artifacts

| File / directory | Key points |
|------------------|------------|
| **todo.md** | Register changes before making them |
| **PROGRESS.md** | Script writes mechanical sections; Main Agent hand-writes "Current state", "Known issues", "Next steps" |
| **DECISIONS.md** | Active constraints |
| **plans/** | Do not change `{{SRC_DIR}}/` before user confirmation |
| **code_review/** | Reviews on disk + index + open-findings |
| **code_simplifier/** | Pre-commit refinement on disk |

Path index: [harness/index.md](harness/index.md).
