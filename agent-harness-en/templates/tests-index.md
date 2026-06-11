# tests — unit tests

- Entry: repo root [pytest.ini](../../pytest.ini) → this directory
- Default gates: `pytest` excludes `@pytest.mark.integration` cases
- **Any change to `{{SRC_DIR}}/` requires tests** (no exceptions); **immediately** start [AGENTS.md](../../AGENTS.md) **tdd** Skill after todo registration, then change `{{SRC_DIR}}/`
- Integration tests: add `pytest -m integration …` notes in this file (not default gates)

Shared fixtures: [conftest.py](conftest.py) (create as needed).
