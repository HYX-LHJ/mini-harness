# Subagent artifacts — hard constraints

The round **must not wrap up** until these steps are done (commit round: no `git commit` without reports).

## code-review-expert

1. **Dispatch**: Main Agent starts Subagent via **Task**, with this round's diff and `code-review-expert` Skill.
2. **Body**: Subagent outputs structured review (severity P0–P3; verdict APPROVE / REQUEST_CHANGES / COMMENT).
3. **Write to disk** (Main Agent, **required**):
   - `harness/code_review/YYYY-MM-DD_topic-summary.md`
   - Add a row at top of [code_review/index.md](../../templates/code-review-index.md)
   - Open **P0/P1** → [open-findings.md](../../templates/open-findings.md)
4. **Forbidden**: chat-only review; no report while checking todo / writing PROGRESS "review complete".

### Severity

| Level | Meaning |
|-------|---------|
| P0 | Security/data loss; blocks merge |
| P1 | Logic error or significant architecture issue |
| P2 | Maintainability / extensibility |
| P3 | Style and minor optimization |

## code-simplifier

1. **Dispatch**: Task + `code-simplifier` Skill, scoped to business-code diff pending commit.
2. **Execute**: Subagent simplifies code in-repo (preserve behavior), summarize changes.
3. **Write to disk** (Main Agent, **required**):
   - `harness/code_simplifier/YYYY-MM-DD_topic-summary.md`
   - Add a row at top of `code_simplifier/index.md`
   - If no meaningful simplification, state "No changes" and why
4. **Follow-up**: re-run gates after refinement; commits with business code need code-review-expert again (second pass).

## Main Agent vs Subagent boundary

| Who | Does what |
|-----|-----------|
| Subagent | Read diff, write review/refinement **body**, optionally edit code (simplifier) |
| Main Agent | Dispatch, collect output, **write to disk**, update index/open-findings, summarize for user |

Main Agent **must not** produce the full review report body instead of the Subagent.
