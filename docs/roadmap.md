# Implementation Roadmap

> **Superseded (near-term) by [`docs/roadmap/agentic_ai_roadmap.md`](roadmap/agentic_ai_roadmap.md).** That document is the operative plan: it resolves the open decisions (D1–D10), organizes delivery around the six workstreams with evaluation gates, defines the SA Agent MVP backlog, sets the governance Level-100 launch checklist, and writes the multi-agent expansion triggers. This file is retained for its **downstream sequencing rationale** (SA → DE → Governance/Assurance → Delivery → PM/Orchestration), which the roadmap preserves as trigger-gated expansion beyond the SA pilot.

A staged plan for growing from a single Solutions Architecture Agent into a coordinated set of role-specific agents for the Data & AI area.

The guiding rule: **each new agent consumes the standardized output of the ones before it.** We expand along the natural flow of a request through the org.

---

## Phase 0 — Foundation (this milestone)

**Goal:** A clean, modular repo and a working first agent.

- [x] Repository structure (`/agents`, `/shared`, `/docs`, `/tests`).
- [x] Shared context: org structure + Data & AI operating model.
- [x] Design principles documented.
- [x] Solutions Architecture Agent v0.1: prompt, config, input/output schemas, example, tests.
- [ ] Wire the agent to a runtime (SDK/API call) — see "Runtime" below.

**Exit criteria:** A request runs through the Solution Architect agent and produces a schema-valid brief with handoff packets.

---

## Phase 1 — Harden the first agent

**Goal:** Make the Solution Architect agent reliable enough to use on real requests.

- Add 5–10 golden test cases spanning request types (dashboard, tracking, pipeline, ML, governance).
- Build a thin runner + output validator (`/shared/utils`) that checks output against the schema.
- Add an evaluation rubric run (does the brief catch the planted risks / gaps?).
- Collect real requests, review outputs with the Solution Architect, tune the prompt.

**Exit criteria:** Solution Architect signs off that briefs are useful and safe to hand downstream.

---

## Phase 2 — First downstream consumer: Data Engineering Agent

**Why next:** The Data Engineer reports under the Solution Architect and is the most direct consumer of the architecture brief's `data_engineering` handoff.

- Copy `/agents/_template` → `/agents/data_engineer`.
- Input schema = the Solution Architect's **Data Engineering handoff packet**.
- Output: pipeline design outline, data contract draft, transformation/orchestration notes, ingestion source checklist.
- Prove the **handoff contract** end-to-end: SA output feeds DE input with no manual reshaping.

**Exit criteria:** A brief's engineering handoff flows into the DE agent and yields a usable pipeline outline.

---

## Phase 3 — Governance & Assurance rails

**Why next:** These roles gate quality and compliance and should be in the loop early.

- **Data Governance Agent** (Data Governance Specialist): policy checks, ownership/stewardship mapping, metadata & lineage requirements, compliance flags. Consumes the brief's `governance` handoff. Governance Analysts (temporary contract, x3) are the human executors this agent supports.
- **Data Assurance Agent** (Data Assurance Specialist): QA rule generation, data validation checklists, anomaly-detection logic, test-case creation. Consumes the brief's `data_quality` handoff.
- **Value Assurance Agent** (Value Assurance Specialist): validates that the proposed solution maps to expected business value and success metrics. Consumes the brief's `success_metrics` and `business_context`.

**Exit criteria:** A brief can be checked for governance and value alignment by agents before build starts.

---

## Phase 4 — Delivery-facing agents

- **Digital Analytics Agent** (Digital Analytics Specialist): GA4 event schema generation, tagging/data-layer docs, funnel mapping, tracking QA, analytics governance. Consumes the `digital_analytics` handoff.
- **Data Visualization Agent** (Data Visualization Specialist): dashboard requirements, KPI mapping, visualization QA, stakeholder reporting briefs. Consumes the `visualization` handoff.
- **Data Science Agent** (Data Scientist): model framing, feature discovery, experiment design, model documentation, evaluation workflows. Consumes the `data_science` handoff.

**Exit criteria:** The three main delivery outputs (analytics, viz, models) have agent support driven by the architecture brief.

---

## Phase 5 — Coordination & orchestration

- **Project Management Agent** (Project Manager): delivery plan, RAID log, dependency/timeline extraction, status summaries, backlog structuring. Consumes the brief's `delivery_dependencies` and `risks`, plus downstream handoffs.
- **Orchestration layer:** route a request through the relevant agents automatically (SA → DE/Governance/Analytics/… → PM), aggregating outputs into a single initiative package.
- Optionally introduce a **Head of Data & Analytics** view: a portfolio-level summary across initiatives for prioritization and governance.

**Exit criteria:** A single request can be fanned out across role agents and reassembled into an initiative package with a delivery plan.

---

## Runtime (cuts across all phases)

Kept intentionally out of the agent definitions so agents stay portable:

- Target implementation: Anthropic **Claude API / Agent SDK** using the latest capable models (default to the current Opus/Sonnet tier for architecture reasoning; a faster tier for mechanical agents).
- A small runner in `/shared/utils` that: loads an agent's `config.yaml`, composes its prompt from `/shared/prompts` + role prompt + injected `/shared/context`, calls the model, and validates output against the agent's output schema.
- Structured output enforced via schema / tool-use so downstream consumption is reliable.

---

## Sequencing rationale

1. **Solution Architect first** — it is the translation bottleneck and produces the artifacts everyone else needs.
2. **Data Engineering next** — closest reporting line and most direct consumer; proves the handoff contract works.
3. **Governance/Assurance** — put quality and compliance rails in before scaling delivery.
4. **Delivery agents** — analytics, viz, science expand capacity where work volume is highest.
5. **Project Management + orchestration** — tie it together once individual agents are trustworthy.

Each phase is shippable on its own; we do not need later phases to get value from earlier ones.
