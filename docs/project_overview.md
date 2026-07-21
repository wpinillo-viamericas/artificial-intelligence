# Project Overview

## Purpose

Create a **scalable foundation for role-specific AI agents** inside the Data & AI area, starting with a **Solutions Architecture Agent**. Each agent accelerates the structured, repeatable thinking of one role while leaving judgment and accountability with the human in that role.

## The problem we are solving

Requests reach the Data & AI area in many shapes: a business sponsor asking for a dashboard, a product team wanting event tracking, a compliance-driven data quality initiative, an ML use case, and so on. Today, turning each of these into a well-scoped, technically sound, governed solution depends heavily on individual expertise and produces inconsistent artifacts. This slows delivery and creates gaps (missing data ownership, unclear success metrics, unmanaged risk).

The Solution Architect sits at the center of this translation problem. Supporting that role first produces **standardized upstream artifacts** that every downstream role can rely on.

## What the Solutions Architecture Agent does

Given a business, analytics, data, or AI initiative request, the agent:

1. **Intakes** the request and normalizes it into a structured form.
2. **Clarifies** objective, stakeholders, systems, expected outcomes, and constraints — surfacing what is missing rather than inventing it.
3. **Translates** the request into a structured **Solution Architecture Brief**.
4. **Identifies** required data sources, integrations, pipelines, analytics layers, governance needs, and delivery dependencies.
5. **Highlights risks**: missing ownership, unclear data sources, data quality gaps, security/compliance exposure, scalability limits, and unclear success metrics.
6. **Produces standardized outputs** with explicit **handoff packets** for downstream roles (Data Engineering, Digital Analytics, Data Governance, Data Visualization, Data Science, Project Management, Value Assurance).

Crucially, the first agent does **not** try to do every role's job. It produces a high-quality architecture brief and clear, scoped handoffs. Depth belongs to the downstream role-specific agents.

## How it fits together

> **Rendered diagram:** [`docs/diagrams/agent_operating_model.md`](diagrams/agent_operating_model.md) — a regenerable, Viamericas-themed operating-model diagram (edit [`brand_palette.json`](diagrams/brand_palette.json) / the template and run `python docs/diagrams/render.py`). The ASCII below is a text fallback of the same flow.

```
                 Business / technical request
                            │
                            ▼
              ┌───────────────────────────────┐
              │  Solutions Architecture Agent  │
              │   (Solution Architect role)    │
              └───────────────────────────────┘
                            │
        Structured Solution Architecture Brief
                            │
     ┌──────────┬───────────┼───────────┬───────────┐
     ▼          ▼           ▼           ▼           ▼
  Data Eng   Governance  Analytics   Data Viz   Data Science  ...
   handoff    handoff     handoff     handoff     handoff
     │          │           │           │           │
     ▼          ▼           ▼           ▼           ▼
 (future role-specific agents consume these handoffs)
```

Shared knowledge (org structure, operating model, common enums/schemas, base prompt blocks) lives in `/shared` so every agent reasons from the same ground truth.

## Non-goals (for v0.1)

- Not a chatbot for general Q&A.
- Not a replacement for the Solution Architect's decision authority.
- Not an implementation engine — it designs and hands off; it does not build pipelines, models, or dashboards.
- Not a system of record — it produces artifacts that are stored/tracked in the team's existing tools.

## Success criteria for the first agent

- A vague one-paragraph request produces a brief with (a) a clear objective, (b) an explicit list of open questions, and (c) at least the required data/governance/delivery components identified.
- Every brief includes a risk register with severity and an owner-or-gap flag.
- Every brief includes at least one downstream handoff packet in the standard schema.
- Output validates against [`agents/solution_architect/schemas/output.schema.json`](../agents/solution_architect/schemas/output.schema.json).

## Related documents

- [`docs/agent_design_principles.md`](agent_design_principles.md)
- [`docs/roadmap.md`](roadmap.md)
- [`shared/context/org_structure.md`](../shared/context/org_structure.md)
- [`shared/context/data_ai_operating_model.md`](../shared/context/data_ai_operating_model.md)
