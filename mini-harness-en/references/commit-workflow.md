# Commit round and discipline

When the user says "commit", "push", etc. without specifying a branch, run this **after regular round wrap-up**.

## Order (do not skip or reorder)

1. Regular wrap-up complete (including code-review on disk, gates after)
2. **code-simplifier** (when delivery includes business code) → write to disk → gates
3. **Second code-review-expert** → write to disk; fix issues and re-run gates if needed
4. Git: `dev` → commit → push → merge `test` → push → back to `dev`
5. `sync_progress.py` + hand-write PROGRESS

Skip steps 2–3 when only harness/docs changed, no business code.

## Pre-commit checklist

```
- [ ] On dev branch (default dev)
- [ ] git status / diff: no secrets, no local integration scratch code
- [ ] lint + pytest all green
- [ ] src/ changes have matching test changes
- [ ] code_review / code_simplifier reports on disk
- [ ] todo checked off
```

## Non-fast-forward merge

Stop and explain to the user; do not `push --force` unless the user explicitly requests it and understands the consequences.

## Commit message

- 1–2 sentences explaining **why**, not a list of what
- Match recent `git log` style in the repo

## When to refresh PROGRESS

- Every round wrap-up
- **After commit and push**, refresh again so remote/HEAD matches the snapshot
