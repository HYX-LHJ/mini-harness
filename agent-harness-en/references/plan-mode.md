# Plan mode — align on approach before major tasks

Same goal as Cursor **Plan** mode: help the user think it through, offer options, **then write code after the user decides**.  
Assume the collaborator is **less familiar with technical details than the Agent**: fewer terms, more analogies, option comparisons at a glance.

Hard constraints live in project `AGENTS.md`; this document is operational detail and doc templates.

---

## When to enter Plan (required)

If **any** of these apply, Plan first — **do not** change business code directories directly:

- New feature / new API / cross-module change (≥3 directories or affects external contract)
- Architecture or data model change, rollout strategy, performance/quota/security work
- Ambiguous requirements, multiple implementation paths, or user says "discuss first / draft a plan / brainstorm / plan this"
- Estimated effort > 1 person-day, or Agent cannot safely deliver in one round

**No Plan needed**: clear single-point bug fix, copy tweak, user gave step-by-step instructions with clear scope, pure harness/doc maintenance.

**Relation to Cursor Plan**: you may suggest switching to Cursor **Plan** mode; if still in **Agent** mode, obey "no business code until confirmed".

---

## Main Agent workflow

1. **Restate the goal in the user's language** (2–4 sentences), list 1–3 open questions (prefer multiple choice).
2. **Dispatch Subagent if needed** (`explore`) to understand current state; translate findings into user-friendly bullets.
3. **Write the plan** → `harness/plans/YYYY-MM-DD-topic.md` (template: `harness/plans/_template.md`).
4. **Conversation summary**: goal, options A/B, **recommendation + why**, ask user to pick.
5. **Hard stop**: wait for explicit confirmation. Before confirmation, only edit `harness/plans/`, `todo.md` (Plan sub-items), `DECISIONS.md` (architecture trade-offs).
6. **After confirmation**: add implementation `task:` to `todo.md` → enter regular round (gates, tdd, implement).

---

## How to talk to the user

- **Conclusion first, details second**; use "I recommend" and "You only need to decide" to reduce pressure.
- Explain jargon in plain language the first time it appears.
- No fake options; if there is only one viable path, say so.
- Small tasks: just do them; large tasks: Plan.

---

## Relation to other artifacts

| Artifact | Difference |
|----------|------------|
| **plans/** | Pre-implementation options for the user |
| **DECISIONS.md** | Confirmed architecture constraints |
| **code_review/** | Post-implementation code review |
| **todo.md** | Executable checklist after Plan confirmation |

After the user confirms a Plan, add a summary to `DECISIONS.md` if it imposes long-term constraints.
