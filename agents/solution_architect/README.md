# Solutions Architecture Agent

Supports the **Solution Architect** role. Turns a business, analytics, data, or AI initiative request into a **structured Solution Architecture Brief** with scoped handoffs for downstream Data & AI roles.

This is the **first agent** in the repo and the reference implementation for the [design principles](../../docs/agent_design_principles.md).

## Contract

| | |
|---|---|
| **Input** | [`schemas/input.schema.json`](schemas/input.schema.json) — a request (`request_text` required; other context optional). |
| **Output** | [`schemas/output.schema.json`](schemas/output.schema.json) — a Solution Architecture Brief + handoff packets. |
| **Prompt** | [`prompt.md`](prompt.md), composed with [`shared/prompts/base_agent.md`](../../shared/prompts/base_agent.md). |
| **Config** | [`config.yaml`](config.yaml) — model, params, prompt composition, injected context, schema paths. |
| **Enums** | [`shared/schemas/enums.json`](../../shared/schemas/enums.json) — shared controlled vocabularies. |

## What it produces

A single JSON object (source of truth) containing:

- `request_summary`, `objective`, `request_type`
- `stakeholders` (with ownership state)
- `solution_options` + `recommended_option`
- `solution_components` (data sources, ingestion, models, analytics, integrations, governance, viz, ML, orchestration, infra)
- `success_metrics`
- `risks` (categorized, severity/likelihood, owner or gap)
- `open_questions`, `assumptions`
- `delivery_dependencies`
- `handoffs` — scoped packets for `data_engineering`, `digital_analytics`, `data_governance`, `data_visualization`, `data_science`, `data_assurance`, `value_assurance`, `project_management`

## What it does NOT do

It designs at the architecture level and hands off. It does **not** build pipelines, write transformations, design dashboards, define event schemas, engineer ML features, or author governance policies — those are downstream, captured as handoffs.

## Example

- Request: [`examples/request_ga4_funnel.json`](examples/request_ga4_funnel.json)
- Brief:   [`examples/output_ga4_funnel.json`](examples/output_ga4_funnel.json)

## Tests

See [`tests/cases.md`](tests/cases.md) — golden cases and the evaluation rubric.

## Running it (Phase 1 — runtime not yet wired)

Intended flow once `shared/utils/agent_runner` exists:

```
input.json ──▶ agent_runner (loads config.yaml)
                 │  composes prompt: base_agent.md + prompt.md + injected context
                 │  calls model (Claude API / Agent SDK) with structured-output enforcement
                 │  validates against output.schema.json
                 ▼
             brief.json (schema-valid) ──▶ handoff_router ──▶ downstream agents
```

Until then, the prompt + schemas + example are sufficient to run the agent manually against a model and validate the result by hand.

## Versioning

Current: **v0.1.0**. Breaking changes to `output.schema.json` bump the major version (downstream consumers depend on it).
