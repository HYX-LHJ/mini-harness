# Installation

mini-harness is a **portable plugin** with shared skills, host manifests, and session-start hooks. Plugin install and repo activation are **two separate steps**.

### Two steps

| Step | What | Required |
|------|------|----------|
| 1. Plugin | Install host plugin (optional reminders) | No — repo activation is enough |
| 2. Activate | `mini_harness.py install` in target repo | **Yes** |

### Supported hosts

| Host | Manifest | Hooks |
|------|----------|-------|
| [Cursor](https://cursor.com/) | `.cursor-plugin/plugin.json` | `hooks/cursor/hooks.json` |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `.claude-plugin/plugin.json` | `hooks/claude/hooks.json` |
| [Codex](https://github.com/openai/codex) | `.codex-plugin/plugin.json` | `hooks/codex/hooks.json` |

Hooks remind agents to read `AGENTS.md`; the playbook is the persistent workflow entry.

### Method 1 — Git clone + activate (recommended)

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd your-project
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

**Windows (PowerShell):**

```powershell
python mini-harness\scripts\mini_harness.py install --root .
python harness\scripts\mini_harness.py doctor --root .
```

### Method 2 — Vendor plugin into your repo

Commit the plugin so the team shares one version:

```text
your-repo/
├── mini-harness/          # plugin source (or submodule)
├── AGENTS.md              # after install
├── harness/               # after install
└── tests/
```

Team members run `python harness/scripts/mini_harness.py install --root .` after pull.

### Method 3 — Host plugin (optional)

<a id="cursor"></a>

#### Cursor

Local test — copy or symlink:

```text
~/.cursor/plugins/local/mini-harness  →  /path/to/mini-harness
```

Restart Cursor or reload the window.

<a id="claude-code"></a>

#### Claude Code

```bash
claude --plugin-dir /path/to/mini-harness
```

Publish via Claude Code plugin marketplace for team distribution.

<a id="codex"></a>

#### Codex

Install `mini-harness` from the Codex marketplace. **Review and trust** bundled hooks before execution. Start a **new session** after install.

### Maintenance commands (activated repo)

```bash
python harness/scripts/mini_harness.py install --root .   # sync templates & skills
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```

### Verify

1. `doctor` → `ok: true`, empty `warnings`
2. `AGENTS.md` at repo root
3. `harness/skills/mini-harness/SKILL.md` exists
4. New agent session: *"Read AGENTS.md and harness state files"*

### Runtime requirements

- Python 3.10+ callable as `python` (or `py` on Windows)
- No third-party deps for the installer itself
- Target repo language/framework is not prescribed

### Maintainer note

Edit **`mini-harness/` only** (authoritative source), then re-run `install` on target repos. See [mini-harness/skills/mini-harness/SKILL.md](../../mini-harness/skills/mini-harness/SKILL.md).
