# 🔌 Installation

mini-harness ships as a **host plugin** for Claude Code, Cursor, and Codex.

| Step | You get |
|------|---------|
| Install plugin | Skills + session hooks |
| Repo `install` | Persistent `harness/` state |

---

## One-click plugin

| Host | Action |
|------|--------|
| **Claude Code** | `/plugin marketplace add HYX-LHJ/mini-harness` → `/plugin install mini-harness@mini-harness` |
| **Cursor** | Dashboard → Plugins → Import `https://github.com/HYX-LHJ/mini-harness` → install **mini-harness** |
| **Codex** | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness` → `codex plugin install mini-harness` |

Then activate in **your project**:

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

---

<details>
<summary>📖 Per-host details</summary>

### Claude Code

```text
/plugin marketplace add HYX-LHJ/mini-harness
/plugin install mini-harness@mini-harness
```

Local: `claude --plugin-dir /path/to/repo/mini-harness`

### Cursor

1. [Cursor Dashboard](https://cursor.com/dashboard) → **Plugins**
2. Import → `https://github.com/HYX-LHJ/mini-harness`
3. Install **mini-harness**

Local: `~/.cursor/plugins/local/mini-harness` → reload window

### Codex

```bash
codex plugin marketplace add github.com/HYX-LHJ/mini-harness
codex plugin install mini-harness
```

Trust hooks → **new session**

</details>

---

## Two layers

| | Content | Required? |
|--|---------|-----------|
| 1️⃣ Plugin | Table above | Recommended |
| 2️⃣ Activate | `mini_harness.py install` | **Yes** |

### Manifest locations

| Host | Marketplace | Manifest |
|------|-------------|----------|
| Claude Code | `.claude-plugin/marketplace.json` | `mini-harness/.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `mini-harness/.cursor-plugin/plugin.json` |
| Codex | `.agents/plugins/marketplace.json` | `mini-harness/.codex-plugin/plugin.json` |

---

## Clone + activate only (no plugin)

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd your-project
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

---

## Maintenance commands

```bash
python harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```

---

## ✅ Verify

1. **Plugin**: `using-harness` skill visible; Codex hooks trusted
2. **Repo**: `doctor` → `ok: true`; `harness/skills/using-harness/SKILL.md` exists

Python 3.10+ (use `py` on Windows). Installer uses stdlib only.

More → [host-support.md](../../mini-harness/skills/using-harness/references/host-support.md)
