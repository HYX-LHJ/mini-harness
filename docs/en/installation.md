# Installation

mini-harness ships as a **host plugin** for Claude Code, Cursor, and Codex. Plugin install loads skills and session hooks; **repo activation** (`mini_harness.py install`) scaffolds `harness/` in your project.

## One-click plugin install

| Host | Steps |
|------|-------|
| **Claude Code** | `/plugin marketplace add HYX-LHJ/mini-harness` then `/plugin install mini-harness@mini-harness` |
| **Cursor** | Dashboard → Settings → Plugins → **Import Marketplace** → `https://github.com/HYX-LHJ/mini-harness` → install **mini-harness** |
| **Codex** | `codex plugin marketplace add github.com/HYX-LHJ/mini-harness` then `codex plugin install mini-harness` |

After installing the plugin, activate harness in your project:

```bash
python mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

Or ask the agent: *"Initialize mini-harness in this repository."*

<details>
<summary>Per-host details</summary>

### Claude Code

```text
/plugin marketplace add HYX-LHJ/mini-harness
/plugin install mini-harness@mini-harness
```

CLI equivalent:

```bash
claude plugin marketplace add HYX-LHJ/mini-harness
claude plugin install mini-harness@mini-harness
```

Local dev: `claude --plugin-dir /path/to/repo/mini-harness`

### Cursor

1. [Cursor Dashboard](https://cursor.com/dashboard) → **Settings** → **Plugins**
2. **Import Marketplace** → paste `https://github.com/HYX-LHJ/mini-harness`
3. Install **mini-harness** from the marketplace panel

Local dev: copy or symlink `mini-harness/` to `~/.cursor/plugins/local/mini-harness`, then reload the window.

### Codex

```bash
codex plugin marketplace add github.com/HYX-LHJ/mini-harness
codex plugin install mini-harness
```

Review and trust bundled hooks when prompted; start a **new session**.

</details>

---

## Two layers

| Step | What | Required |
|------|------|----------|
| 1. Plugin | Install via table above | Recommended (skills + hooks) |
| 2. Activate | `mini_harness.py install` in target repo | **Yes** for harness files |

### Manifest locations

| Host | Marketplace (repo root) | Plugin manifest |
|------|-------------------------|-----------------|
| Claude Code | `.claude-plugin/marketplace.json` | `mini-harness/.claude-plugin/plugin.json` |
| Cursor | `.cursor-plugin/marketplace.json` | `mini-harness/.cursor-plugin/plugin.json` |
| Codex | `.agents/plugins/marketplace.json` | `mini-harness/.codex-plugin/plugin.json` |

### Method 2 — Git clone + activate only

If you skip the host plugin:

```bash
git clone https://github.com/HYX-LHJ/mini-harness.git
cd your-project
python /path/to/mini-harness/mini-harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py doctor --root .
```

### Maintenance (activated repo)

```bash
python harness/scripts/mini_harness.py install --root .
python harness/scripts/mini_harness.py update --root .
python harness/scripts/mini_harness.py doctor --root .
python harness/scripts/mini_harness.py uninstall --root .
```

### Verify

1. Plugin: `skills/using-harness/SKILL.md` visible in host; session-start hook trusted (Codex) — workflow usable without repo `install`
2. Repo (after `install`): `doctor` → `ok: true`, empty `warnings`; `harness/skills/using-harness/SKILL.md` exists

### Runtime requirements

Python 3.10+ (`python` or `py` on Windows). Installer uses stdlib only.

See also: [host-support.md](../../mini-harness/skills/using-harness/references/host-support.md)
