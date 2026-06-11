# Plan mode — align on approach before major tasks

Same goal as Cursor **Plan** mode: help the user think it through, offer options, **then write code after the user decides**.  
Assume the collaborator is **less familiar with technical details than the Agent**: fewer terms, more analogies, option comparisons at a glance.

Hard constraints: root [AGENTS.md](../../AGENTS.md); this document is operational detail and doc templates.

---

## When to enter Plan (required)

If **any** of these apply, Plan first — **do not** change `{{SRC_DIR}}/` directly:

- New feature / new API / cross-module change (≥3 directories or affects external contract)
- Architecture or data model change, rollout strategy, performance/quota/security work
- Ambiguous requirements, multiple implementation paths, or user says "discuss first / draft a plan / plan this"
- Estimated effort > 1 person-day, or Agent cannot safely deliver in one round

**No Plan needed**: clear single-point bug fix, copy tweak, user gave step-by-step instructions with clear scope, pure harness/doc maintenance.

---

## Main Agent workflow

1. **Restate the goal in the user's language** (2–4 sentences), list 1–3 open questions.
2. **Dispatch Subagent if needed** (`explore`) to understand current state.
3. **Write the plan** → `harness/plans/YYYY-MM-DD-topic.md` (template: [../plans/_template.md](../plans/_template.md)).
4. **Conversation summary**: goal, options A/B, **recommendation + why**.
5. **Hard stop**: wait for explicit confirmation.
6. **After confirmation**: add `task:` to `todo.md` → regular round.

---

## Plan document template (copy to use)

```markdown
# Plan: <one-line title>

**Date**: YYYY-MM-DD  
**Status**: draft | awaiting user confirmation | confirmed (option X)

## What we're solving

…

## Options

| | Option A | Option B |
|---|----------|----------|
| One-liner | | |
| Pros | | |
| Cons | | |

## Recommendation

**Recommend option X**, because: …

## Your decision

Please reply: pick A / B / need changes …
```

---

## Relation to other artifacts

| Artifact | Difference |
|----------|------------|
| **plans/** | Pre-implementation plans |
| **DECISIONS.md** | Confirmed architecture constraints |
| **code_review/** | Post-implementation review |
| **todo.md** | Checklist after confirmation |
