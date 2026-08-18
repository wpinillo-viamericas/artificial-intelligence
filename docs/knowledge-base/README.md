# Viamericas AI Knowledge Base

Curated knowledge supporting Viamericas' AI initiatives, organized in two layers:

## 1. Event snapshots (immutable)

One folder per event (`<event>-<year>/`), holding photos of slides plus companion notes transcribing them. These record **what was said at a point in time** and are never edited after filing — corrections and updates belong in the reference layer.

- [aws-summit-2026/](./aws-summit-2026/README.md) — AWS Summit Bogotá 2026 (July 30): Amazon Bedrock AgentCore, agents in production.

## 2. Reference layer (living, re-verified)

Topic-based deep-dive notes that verify and expand the event claims against official documentation, sample code, and hands-on findings. Each note lists its sources with access dates and ends with a `Last verified:` line — re-check notes whose date has gone stale before relying on them.

- [agentcore-reference/](./agentcore-reference/README.md) — Bedrock AgentCore: runtime, gateway, memory, identity, observability, RAG, harness/SDK, MCP tooling, and the hands-on learning path.

## 3. Company governance and strategy (extracted)

Markdown extracts of internal policy and strategy documents so agents and developers can consume them as context. The formatted originals (`.docx`/`.pptx`) are gitignored and live in SharePoint / local folders — see the folder README for provenance and re-extraction notes.

- [politicas-y-estrategia-ia/](./politicas-y-estrategia-ia/README.md) — AI Acceptable Use and Data Protection Policy, Viamericas AI Strategy, use-case discovery and training-adoption decks.

## Conventions

- Event snapshot: `YYYY-MM-DD_<category>_<kebab-topic>.jpg` + companion `.md` (see the event README for the note format).
- Reference note: one file per topic, kebab-case; header links back to the related event note(s); facts that can't be verified go under "Open questions", never stated as fact; `Last verified: <date>` footer.
- English throughout; source-language quotes preserved where transcribed.
