# Data & AI Agents — Internal MCP Server

An internal [Model Context Protocol](https://modelcontextprotocol.io) server that
exposes **this repo's structured substrate** — schemas, shared context, artifact
validation, handoff extraction, the governance registry, and diagram rendering —
as MCP tools and resources. It makes the reference architecture's **Tooling Layer**
concrete and reusable across every agent and IDE surface (Claude Code, Claude
Desktop, etc.).

This is the deliberate first MCP server: it needs **no external vendor terms**
(unlike a catalog or Jira integration) and every future agent reuses it, matching
the "capabilities used by ≥2 agents are shared services" rule. It also serves as
the low-risk **spike answering open decision D9** (MCP vs native APIs).

## What it exposes

### Tools

| Tool | Purpose | Risk |
|---|---|---|
| `validate_artifact(agent, artifact, kind="output")` | Validate an artifact against an agent's JSON Schema **plus** cross-reference / Definition-of-Done consistency checks. Returns `{ok, errors[], warnings[]}` — errors are hard schema failures, warnings are advisory. | read-only |
| `get_schema(agent, kind="output")` | Return an agent's input/output JSON Schema as a parsed object. | read-only |
| `list_schemas()` | List agents + which schemas they have, plus shared context docs and enums. | read-only |
| `get_shared_context(name)` | Return a ground-truth doc (`org_structure`, `data_ai_operating_model`). Grounding / RAG-lite. | read-only |
| `extract_handoffs(brief)` | Extract scoped handoff packets from a Solution Architecture Brief — the handoff contract a downstream agent's input consumes. | read-only |
| `list_agents()` | Discovered agents + the agent/tool/prompt governance registry (decision D7). | read-only |
| `render_diagram()` | Regenerate the operating-model diagram from palette + template (wraps `docs/diagrams/render.py`). | medium (writes generated files) |

### Resources

| URI template | Content |
|---|---|
| `schema://{agent}/{kind}` | Raw JSON Schema text, e.g. `schema://solution_architect/output`. |
| `context://{name}` | Shared-context markdown, e.g. `context://org_structure`. |

## Layout

```
shared/mcp/
  repo.py          # repo layout + agent/context discovery (stdlib only)
  validation.py    # schema + consistency validation, handoff extraction (jsonschema)
  registry.json    # agent/tool/prompt governance registry seed (D7)
  server.py        # thin FastMCP layer wiring the core to MCP tools/resources
  pyproject.toml
  tests/           # test_repo.py, test_validation.py (no MCP SDK needed)
```

**Design note:** `repo.py` and `validation.py` depend only on stdlib +
`jsonschema`/`referencing` and are importable/testable **without** the MCP SDK —
keeping the runtime concern in `server.py` so the logic stays portable (the same
principle as `shared/utils`). `validation.validate_artifact` is the concrete
implementation of the `schema_validator` helper described there.

## Install & run

```bash
# from the repo root
pip install "mcp[cli]" jsonschema      # or: pip install -e shared/mcp
python -m shared.mcp.server            # starts the stdio server
```

Run the tests (SDK not required):

```bash
pip install pytest
python -m pytest shared/mcp/tests -q
```

### Register with an MCP client

Point any MCP client at the module over stdio. Example client config:

```json
{
  "mcpServers": {
    "data-ai-agents": {
      "command": "python",
      "args": ["-m", "shared.mcp.server"],
      "cwd": "C:/Users/Wilson.Pinillo/Documents/artificial-intelligence"
    }
  }
}
```

For Claude Code:

```bash
claude mcp add data-ai-agents -- python -m shared.mcp.server
```

## Consistency checks (the `warnings` tier)

Beyond schema validity, `validate_artifact` runs cheap deterministic checks that
mirror the operating model's "what good looks like" for a brief:

- `recommended_option.option_name` must match a `solution_options[].name`.
- At least one stakeholder marked `is_owner=true` (or flag the gap).
- Non-measurable success metrics should have a corresponding open question.
- No duplicate handoff `to_role` entries.
- Delivery dependencies present but no handoffs → downstream can't start.

These are **warnings, not errors**: they inform the human reviewer / agent without
blocking, since the schema is the hard contract.

## Roadmap alignment

- **Now (Phase 0/1):** this server — repo-native, no external dependencies.
- **Phase 2:** a read-only **Data Catalog MCP** (dataset lookup, ownership,
  lineage) once the platform stack (decision D3) is confirmed — the first
  *external* server.
- **Phase 3:** approval-gated write tools (Confluence draft, Jira backlog) added
  as medium/high-risk registered tools, each passing the registry + risk-rating
  process, never ad-hoc wiring.

New agents get validation, schema, and handoff tooling for free — no per-agent
duplication.
