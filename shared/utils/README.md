# Shared Utils

Reusable helper logic shared across agents. Kept language-agnostic in spec here; implement in the chosen runtime (Python or TypeScript) during Phase 1.

Intended helpers:

- **`prompt_composer`** — builds a final system prompt from: `shared/prompts/base_agent.md` + the agent's `prompt.md` + injected `shared/context/*` files listed in the agent's `config.yaml` (`context_includes`).
- **`schema_validator`** — validates an agent's output against its `schemas/output.schema.json` (resolving `$ref`s into `shared/schemas/enums.json`). Fails loudly so bad output never reaches a downstream agent.
- **`agent_runner`** — loads `config.yaml`, composes the prompt, calls the model (Claude API / Agent SDK) with structured-output enforcement, validates, and returns the structured result plus metadata.
- **`handoff_router`** — extracts `handoffs[]` from an agent output and routes each packet to the target downstream agent's input schema (used from Phase 2 onward).

Design notes:
- Utils never hardcode org facts — those live in `shared/context`.
- Utils are dependency-light and independently testable.
- Keep the runtime concern here so agent definitions (`prompt.md`, `config.yaml`, `schemas/`) stay portable.
