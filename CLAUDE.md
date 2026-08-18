# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A modular foundation for role-specific AI agents supporting Viamericas' Data & AI area. It is mostly **structured markdown, JSON Schemas, and prompts**, plus two Python components: an internal MCP server (`shared/mcp/`) and a diagram generator (`docs/diagrams/render.py`). The first live agent is `agents/solution_architect/`; the rest of the portfolio is planned in `docs/roadmap.md`.

## Commands

```bash
# Run all tests (pytest testpaths configured in shared/mcp/pyproject.toml)
python -m pytest shared/mcp/tests -q

# Run a single test file / test
python -m pytest shared/mcp/tests/test_validation.py -q
python -m pytest shared/mcp/tests/test_repo.py::<test_name> -q

# Regenerate all diagrams (after editing a .mmd.tpl or brand_palette.json)
python docs/diagrams/render.py

# Run the internal MCP server (stdio, from repo root)
python -m shared.mcp.server

# Dependencies
pip install "mcp[cli]" jsonschema pytest   # or: pip install -e shared/mcp
```

## Architecture

**One role, one agent.** Each agent lives in `agents/<role_name>/` with a fixed anatomy: `prompt.md`, `config.yaml` (model, params, schema paths, version), `schemas/input|output.schema.json`, `examples/`, `tests/cases.md`. New agents are bootstrapped by copying `agents/_template/`. Full rules: `docs/agent_design_principles.md`.

**Structured I/O is the contract.** JSON Schema outputs are the source of truth; prose is a rendering. Agents produce **handoff packets** addressed to downstream roles — this is how agents compose. Missing information is marked `unknown`/`not_provided` and surfaced in `open_questions`/`assumptions`, never fabricated.

**Shared ground truth lives once.** Org facts, enums, and prompt building blocks live in `shared/context/`, `shared/schemas/enums.json`, and `shared/prompts/` and are referenced from agents — never copied or hardcoded into an agent's prompt.

**MCP server layering** (`shared/mcp/`): `repo.py` (discovery) and `validation.py` (schema + consistency checks, handoff extraction) depend only on stdlib + `jsonschema` and are testable **without** the MCP SDK. `server.py` is a thin FastMCP wrapper — keep runtime/MCP concerns there only. Validation returns `errors` (hard schema failures) vs `warnings` (advisory consistency checks); the schema is the hard contract.

**Diagrams are generated** (`docs/diagrams/`): edit only `brand_palette.json` (colors) or `*.mmd.tpl` (structure), then re-run `render.py`. Never hand-edit the generated `.mmd`/`.md`/`.svg`/`.png` files. To add a diagram: create `<name>.mmd.tpl` using `{{token}}` placeholders and add a row to the `DIAGRAMS` list in `render.py`. Every `{{token}}` must exist in the palette's `colors` or render errors loudly.

## Knowledge base conventions (`docs/knowledge-base/`)

- **Event snapshots** (`<event>-<year>/`) are immutable once filed — corrections go in the reference layer, not the snapshot. Naming: `YYYY-MM-DD_<category>_<kebab-topic>.jpg` + companion `.md`.
- **Reference notes** (`agentcore-reference/`) are living docs: one kebab-case file per topic, sources with access dates, unverifiable claims under "Open questions", and a `Last verified: <date>` footer — re-verify stale notes before relying on them.
- English throughout. Formatted policy originals (`.docx`/`.pptx`) are gitignored; only markdown extracts are committed (`politicas-y-estrategia-ia/`).
