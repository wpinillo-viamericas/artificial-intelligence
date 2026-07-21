# Solutions Architecture Agent — Research

> Document 4 of 9 — see [research_overview.md](research_overview.md) for the index; citations `[S#]` in [research_sources.md](research_sources.md).
>
> This document researches the *first* agent. A v0.1 scaffold already exists in `agents/solution_architect/` (prompt, config, input/output schemas, example, tests); findings below are framed as confirm / extend / change against it.

## Why this agent, validated

- **Passes the agent-worthiness gating test** — translating ambiguous business/analytics/data/AI requests into structured architecture involves nuanced judgment, resists codified rules, and consumes unstructured input [S1] **[Verified]**.
- **Requirements-to-architecture is the most-studied GenAI application in software architecture** (40% of reviewed studies) — the core translation job is exactly where LLMs are being applied [S12] **[Extracted]**.
- **An orchestrated, human-supervised pipeline beats single prompts at this job**: AgenticAKM's extraction→retrieval→generation→validation pipeline outscored single-prompt LLMs on all metrics (3.8–3.9 vs 3.3/5, blind study, 29 repos), with the largest gap in *completeness*; naive single prompts fail because architectural knowledge is distributed and exceeds effective context [S11] **[Verified, preliminary — single workshop-scale study]**.
- **Caution:** ADR/C4 generation specifically is thinly evidenced (one study each in the systematic review), and rigorous testing of GenAI architecture outputs is "typically missing" — this agent operates in a promising but under-validated area and needs its own evaluation harness from day one [S12] **[Extracted]**.

## Recommended scope (MVP)

**[Recommendation]** One bounded workflow, one deliverable family:

> **In:** a business/analytics/data/AI request (structured intake + free text + optional attachments).
> **Out:** a schema-valid **Solution Architecture Brief** with per-role handoff packets, plus ADRs for key decisions and a context/container diagram as text — always routed to the human Solution Architect for review.

Internal shape (workflow, not free-running agent [S2] **[Verified]**):

```
intake → clarify (ask-first) → retrieve (approved corpus) → generate (brief + ADRs + diagram)
      → validate (deterministic + LLM critique, ≤3 refinement iterations) → render → human review
```

The ≤3-iteration validator loop and human-architect supervision mirror AgenticAKM's validated design [S11]; the ask-first stage mirrors the arc42 toolkit ("no generation happens until you have answered") [S23] **[Extracted]**; maker-checker loops require acceptance criteria, an iteration cap, and human-escalation fallback [S5] **[Verified]**.

## Core capabilities

| Capability | MVP | Evidence / notes |
|---|---|---|
| Intake + requirements decomposition | ✅ | Existing input schema; extend with request-source metadata |
| Clarifying-question generation | ✅ | Ask-first pattern [S23]; questions directed at named roles (existing `open_questions.directed_to`) |
| Retrieval over approved corpus (org context, standards, prior briefs/ADRs) | ✅ (small corpus) | Distributed-knowledge finding [S11]; identity-trimmed [S5] **[Verified]** |
| Solution options + recommendation with rationale | ✅ | Existing schema (`solution_options`, `recommended_option`) |
| Risk assessment (category, severity, likelihood, owner/gap) | ✅ | Existing schema; risk-as-first-class principle |
| Assumptions & open questions surfacing | ✅ | Existing principle #3 — the anti-hallucination control |
| ADR drafting | ✅ (new) | Well-defined structured target [S22]; see templates below |
| Handoff packets per downstream role | ✅ | Existing schema; future delegation contracts [S3] |
| Diagram generation (text-based C4 context/container) | ✅ minimal (Mermaid) | Diagrams-as-code so they're versionable/regenerable [S23][S24] **[Extracted]** |
| Success metrics / KPI definition | ✅ | Existing schema (`success_metrics`, `measurable` flag) |
| Backlog generation (epics/stories from handoffs) | ⏩ later | Requires Jira integration + PM-role alignment |
| Data contract drafting | ⏩ later | Belongs mostly to the DE agent's depth; SA emits contract *requirements* in the `data_engineering` handoff **[Inference]** |
| Governance checklist generation | ⏩ later | Depends on governance policy corpus being retrievable |
| Dependency mapping across initiatives | ⏩ later | Needs portfolio memory (multiple briefs) |
| Writing directly to Jira/Confluence | ⏩ later, approval-gated | Write tools are medium/high-risk → HITL pause [S1] **[Verified]** |

## Inputs

Confirmed/extended from the existing input schema **[Recommendation]**:

- Requester identity and role; business sponsor if known (identity also drives security trimming [S5]).
- Request narrative (unstructured), request type hint, urgency/priority.
- Known systems, data sources, constraints (platforms, compliance, budget/timeline).
- Expected outcomes / success criteria as stated by the business.
- Attachments/links (prior docs, tickets) — MVP: pasted text; later: fetched via tools.
- Everything optional except identity + narrative: missing information is the agent's job to surface, not a validation error **[Inference from design principle #3]**.

## Outputs

The **structured JSON is the source of truth; prose/markdown is a rendering** (existing principle #2, corroborated by schema-first guidance [S25] **[Extracted]**). Output set:

1. **Solution Architecture Brief** — existing `output.schema.json` is well-aligned with the evidence; keep.
2. **ADRs (new)** — one per significant decision, embedded in the brief and renderable standalone. Immutable: amend or supersede, never edit [S22] **[Extracted]**.
3. **Diagram (new)** — C4 context/container as Mermaid (MVP) with the schema storing the source text; Structurizr DSL is the more rigorous later option [S24].
4. **Handoff packets** — existing; each self-contained enough for the receiving role/agent to start.
5. **Run metadata** — agent version, prompt version, model, timestamps, input ref, reviewer decision (audit trail, [governance_security_and_risk.md](governance_security_and_risk.md)).

## Required templates

| Artifact | Recommended template | Why |
|---|---|---|
| ADR | **MADR** (Markdown Any Decision Records), simple variant to start | Emphasizes options with pros/cons — matching the brief's existing `solution_options` structure; Nygard's template is the simpler fallback; both widely recognized [S22] **[Extracted]** |
| ADR quality rules | One decision per record; explicit rationale; immutable/supersede semantics; timestamps | Encodable as generation + validation rules [S22] |
| Brief structure | Keep the repo's brief; map sections to **arc42** headings where natural (goals/constraints/quality/risks/decisions) rather than adopting all 12 sections | arc42 is the recognized what-and-how standard; full adoption is overkill for an intake-stage brief **[Recommendation]**. Note arc42's one hard sequencing rule: quality goals precede other architecture work [S23] **[Extracted]** — the brief's `objective`/`success_metrics` play this role |
| Diagrams | **C4 model**, context + container levels, as text (Mermaid MVP → Structurizr DSL/PlantUML later) | Hierarchical, developer-friendly, docs-as-code and CI-exportable [S22][S24] **[Extracted]**. Privacy note: render diagrams locally or on self-hosted services, not public renderers like kroki.io [S24] |
| Technical Debt Record | Optional later artifact type | Distinct templated artifact alongside ADRs in mature docs-as-code setups [S24] |

## Required schemas

- **Keep:** input schema; output brief schema; shared enums (`request_type`, `risk_category`, `severity`, `likelihood`, `downstream_role`, `confidence`, `known_state`).
- **Add:** `adr` fragment (title/status/context/decision/consequences/options-considered, `supersedes` ref); `diagram` fragment (type: c4_context|c4_container, format: mermaid|structurizr|plantuml, source text); `clarification` round-trip schema (questions asked ↔ answers received) so intake is auditable.
- **Practice:** define schemas once in code (Pydantic), generate JSON Schema, enforce via Claude tool-based structured output, validate on return — prompt-and-parse is fragile in production [S25] **[Extracted]**. Details in [development_best_practices.md](development_best_practices.md).

## Required integrations

| Integration | MVP | Later | Notes |
|---|---|---|---|
| Model API (Anthropic Claude) | ✅ direct API, tool-use-enforced schema | Agent SDK if runner outgrows a thin script | Matches existing `config.yaml`; [technology_options.md](technology_options.md) |
| Approved-corpus retrieval | ✅ local/indexed docs | Data catalog, Confluence (read, identity-trimmed [S5]) | **[Open decision]** corpus scope |
| Intake channel | ✅ one (form/CLI/chat) | Jira/Slack/Teams intake | **[Open decision]** |
| Output surface | ✅ repo/markdown + reviewer | Confluence publish, Jira backlog creation (approval-gated writes [S1]) | Writes are medium/high-risk tools |
| Tracing/observability | ✅ from day one | — | Weakest layer industry-wide; top investment priority [S17] |
| Integration-pattern caveat | — | — | Concrete Jira/Confluence/M365 wiring patterns were **not** adversarially verified by this research; run a technical spike before committing ([implementation_prerequisites.md](implementation_prerequisites.md)) |

## MVP vs later phases

**MVP (validate usefulness before breadth):** single agent; ask-first intake in one channel; small retrieval corpus; brief + ADRs + Mermaid C4 context diagram; deterministic + LLM validation with 3-iteration cap; human review of 100% of outputs; 20–50 golden cases [S4]; full trace + audit logging; agent/tool/prompt registry entries.

**Phase-2 candidates (after architect sign-off that briefs are useful):** Jira/Confluence read integration; backlog generation (approval-gated writes); larger corpus incl. catalog metadata; Structurizr DSL diagrams + consistency linting in CI [S23][S24]; LLM-judge pre-screen routing low scores to humans [S9]; brief-to-brief memory (prior-art retrieval across initiatives).

**Explicitly deferred:** multi-agent decomposition into separate extraction/retrieval/generation/validation *agents* (the AgenticAKM shape [S11]) — adopt only if the single workflow hits its documented limits (instruction failures, tool overload, context exhaustion) [S1][S5] **[Verified]**; autonomous publishing; fine-tuning [S9]; parallel subagents [S16].

## Risks and controls (agent-specific)

| Risk | Control | Evidence |
|---|---|---|
| Plausible-but-wrong recommendations → architectural degradation from blind trust | Mandatory architect review; options-with-tradeoffs rather than single answers; assumptions/open-questions as required schema fields; confidence marking | [S12] **[Extracted]**; existing principles #3, #10 |
| Incomplete briefs (the biggest quality gap single prompts showed) | Retrieval stage + validator completeness checks + rubric-scored review | [S11] **[Verified]** |
| Hallucinated org facts (systems, owners, platforms) | Ground truth injected from `shared/context` only; `known_state`/`not_provided` enums; never fabricate principle | Existing design; [S12] |
| Inconsistent outputs breaking downstream consumption | Schema-enforced structured output + deterministic validation before return | [S25] **[Extracted]** |
| Data leakage via retrieval | Identity-aware security trimming per store; approved-source allowlist | [S5] **[Verified]** |
| Silent quality drift after prompt changes | Golden-case regression in CI; no prompt merge without green evals | [S4][S12] |
| Cross-artifact inconsistency (ADR ↔ brief ↔ diagram) | Deterministic consistency linter (IDs/names/risks referenced across artifacts) in CI — proven pattern | [S23] **[Extracted]** |
| Reviewer rubber-stamping (HITL fatigue) | Keep volume low in pilot; rubric-based review; track edit-distance between draft and approved version as a health metric | **[Inference]**; pass^k thinking [S4] |
