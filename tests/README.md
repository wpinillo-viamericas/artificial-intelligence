# Cross-cutting Tests

Repo-level and integration tests that span more than one agent or the shared layer.

Per-agent golden cases live with the agent (e.g. `agents/solution_architect/tests/`). This folder is for:

- **Schema integrity** — every `*.schema.json` parses and all `$ref`s into `shared/schemas/enums.json` resolve.
- **Shared enum consistency** — role keys in `shared/schemas/enums.json` match `shared/context/org_structure.md`.
- **Handoff contract tests (Phase 2+)** — a Solution Architect handoff packet validates as the *input* of the corresponding downstream agent. This is what proves agents compose.
- **Prompt composition** — `shared/utils/prompt_composer` assembles the expected prompt for each agent from its `config.yaml`.

Implement these in the chosen runtime during Phase 1 (see `docs/roadmap.md`). Until then, this file documents intended coverage.
