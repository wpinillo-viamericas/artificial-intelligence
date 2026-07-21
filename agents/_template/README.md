# Agent Template

Copy this folder to bootstrap a new role-specific agent:

```
cp -r agents/_template agents/<role_name>
```

Then fill in each file. The Solutions Architecture Agent (`agents/solution_architect`) is the reference implementation — mirror its structure.

## Checklist for a new agent

- [ ] **`config.yaml`** — set `agent.name`, `role`, `version`; wire `prompt.compose`, `context_includes`, and `schemas`.
- [ ] **`prompt.md`** — define the role, what it must do, its boundaries (stay in lane), and its output contract. Composed on top of `shared/prompts/base_agent.md`.
- [ ] **`schemas/input.schema.json`** — usually the **handoff packet** this role receives from an upstream agent (e.g. the Solution Architect's handoff for this role).
- [ ] **`schemas/output.schema.json`** — this role's structured deliverable. Reuse `shared/schemas/enums.json` via `$ref`.
- [ ] **`examples/`** — at least one worked input → output pair.
- [ ] **`tests/cases.md`** — golden cases + evaluation rubric.
- [ ] **`README.md`** — the contract and how to run it.
- [ ] Update the status table in the root `README.md` and mark the phase in `docs/roadmap.md`.

## Principles to honor

See [`docs/agent_design_principles.md`](../../docs/agent_design_principles.md). Most important: one role/one job, structured I/O as the contract, never fabricate, handoff-first, risk as first-class, shared ground truth.
