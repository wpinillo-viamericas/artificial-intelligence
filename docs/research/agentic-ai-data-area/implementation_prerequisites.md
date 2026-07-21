# Implementation Prerequisites — Inputs to the Roadmap Phase

> Document 8 of 9 — see [research_overview.md](research_overview.md) for the index; citations `[S#]` in [research_sources.md](research_sources.md).
>
> This document does **not** define the roadmap. It enumerates the decisions, platforms, standards, processes, sample data, and evaluation criteria the roadmap phase will consume, plus the maturity frame and workstream/dependency map the roadmap should be organized around.

## Adoption maturity model for the Data & AI area

**[Recommendation]** — synthesis of the Microsoft adoption maturity model [S6] and AAGMM [S13] **[Extracted]**, adapted to this org. Use it to name where we are, what each level requires, and what is deliberately postponed.

| Level | Name | Capabilities | Dominant risks | Governance required |
|---|---|---|---|---|
| 0 | Manual workflows | Humans + ad-hoc LLM chat use | Shadow AI; inconsistent quality | Usage policy; approved-tools list |
| 1 | Prompt templates | Shared, versioned prompts for recurring tasks | Prompt drift; no measurement | Prompts in git; owner per template |
| 2 | Role-based copilots | Advisory assistants per role; no tools; human executes everything | Blind trust in fluent output [S12]; no traceability | Output-review norms; source citation; basic logging |
| 3 | **Tool-enabled agents** ← target for SA Agent MVP | Single schema-first agent per validated use case; retrieval + typed tools; bounded workflow; 100% human review | Data leakage via tools; weak evals; silent drift | Microsoft Level-100 set [S6]: owners, approved sources, env separation, logging, incident procedures + eval gate in CI + registries started |
| 4 | Multi-agent workflows | Orchestrator-worker over role agents; delegation contracts; pipelined handoffs | Coordination failures (41–86.7% in immature systems [S10]); 15× cost [S3]; role confusion | AAGMM Level-3 minimum [S13]: formal policies, central catalog, RBAC, HITL; delegation-contract schemas; per-agent cost metering |
| 5 | Governed enterprise ecosystem | Portfolio of governed agents; tiered controls; predictive governance; cross-initiative memory | Sprawl (duplication, shadow/orphaned agents, permission creep [S13]); maintenance load | Microsoft 300–500 [S6]: classification by criticality/autonomy, zoned environments, CoE/AI-Council, continuous compliance |

Rule from the evidence: **do not skip levels, and gate each promotion on the previous level's exit criteria** — incremental single-agent-first expansion is the verified vendor consensus [S1][S2][S5] **[Verified]**, and reactive (incident-driven) governance adds almost nothing [S13] **[Extracted]**.

## Required decisions (blocking roadmap definition)

| # | Decision | Options / default leaning | Informed by |
|---|---|---|---|
| D1 | Runtime & hosting: where the runner executes (local/CI job, container service, serverless), and dev/test/prod separation | Default: thin Python runner in a container; env separation from day one [S6] | [technology_options.md](technology_options.md) |
| D2 | Model provider terms: enterprise agreement, data retention, region for the Claude API | Must precede any real request data entering the agent | [governance_security_and_risk.md](governance_security_and_risk.md) |
| D3 | MVP retrieval corpus: exactly which sources are approved (shared context, standards docs, prior briefs? Confluence spaces? catalog metadata?) and how identity trimming is enforced [S5] | Start narrowest that still grounds briefs | [reference_architecture.md](reference_architecture.md) |
| D4 | Intake channel + output surface for the pilot | Default: lightweight form or chat + markdown outputs in repo/Confluence draft | [solutions_architecture_agent_research.md](solutions_architecture_agent_research.md) |
| D5 | Output standards: ADR template (MADR-simple default), arc42 section mapping, diagram format (Mermaid default → Structurizr later) | Defaults per [S22][S23][S24] | same |
| D6 | Evaluation ownership: who curates golden cases, who is the calibration reviewer, what the pilot pass bar is (approval-rate / rubric threshold) | Default: Solution Architect owns cases; Head of D&A sets bar | [development_best_practices.md](development_best_practices.md) |
| D7 | Governance minimum at launch: adopt agent/tool/prompt registries + risk tiering now (recommended) vs at second agent | Recommended: now — Level-100 set is cheap and pays immediately [S6][S8] | [governance_security_and_risk.md](governance_security_and_risk.md) |
| D8 | Multi-agent trigger criteria, written in advance (instruction-following failure rate, tool-confusion evidence, context exhaustion) [S1][S5] | Draft thresholds during pilot | [reference_architecture.md](reference_architecture.md) |
| D9 | Integration transport for enterprise tools when they arrive: MCP servers vs native APIs | Needs a spike — patterns not verified by this research | [technology_options.md](technology_options.md) |
| D10 | Budget guardrails: token/cost ceiling per run and per month; alerting thresholds [S3] | Set before pilot | [governance_security_and_risk.md](governance_security_and_risk.md) |

## Required platforms and infrastructure

- Model API access (Anthropic) with enterprise terms (D2); secrets manager for keys/credentials; container or job runtime (D1) with dev/test/prod separation [S6].
- Git hosting + CI (schema checks, golden-case regression, consistency linter) — [development_best_practices.md](development_best_practices.md).
- Trace/observability store (structured logs at minimum; a Langfuse-class tool preferred) [S17][S18].
- Persistent, per-user-isolated session/state storage (validated isolation before prod) [S21].
- Later: index/vector store for the retrieval corpus; MCP or API gateway for enterprise integrations (D9).

## Required integrations (sequenced)

1. **MVP:** none beyond model API + local corpus. This is deliberate — successful first deployments are constrained and measurable [S17] **[Extracted]**.
2. **Phase 2:** Confluence/catalog **read** (identity-trimmed [S5]); Jira read for intake context.
3. **Phase 3:** approval-gated **writes** (Confluence draft publishing, Jira backlog creation) as medium/high-risk registered tools [S1].
4. Slack/Teams intake, M365/Google Workspace, BI tools: only when a specific agent capability requires them — each addition passes the tool-registry + risk-rating process, not ad-hoc wiring.

## Required standards (to ratify before build)

- Output artifact standards: MADR ADRs, arc42-informed brief, C4-as-text diagrams (D5) [S22][S23][S24].
- Schema conventions: Pydantic-first, generated JSON Schema, shared enums, semver on schemas [S25].
- Prompt conventions: composition order, context-injection blocks, tool-description style [S1][S2].
- Registry schemas: agent/tool/prompt entries with owner, risk tier, scopes, eval status, rollback [S8].
- Review rubric for briefs (completeness, correctness, risk coverage, handoff quality) — doubles as the judge rubric [S3][S4].

## Required governance processes

- Agent lifecycle: propose (gating test [S1]) → registry entry + owner → build → eval gate → pilot with 100% review → promote/retire. Registry entry precedes production, always (anti-shadow-agent control [S13]).
- Change management: PR-gated prompt/schema/config changes with regression evidence; model upgrades treated as changes [S4][S8].
- HITL procedures: the two mandatory triggers (failure thresholds; high-risk actions) with named escalation paths [S1] **[Verified]**.
- Incident response for agent failures + user feedback channel (Level-100 requirements [S6]).
- Quarterly registry review: orphaned agents, permission creep, duplicate capabilities [S13].

## Required sample data and documents (pilot inputs)

**[Recommendation]** Collect before build:

- 10–20 **real historical requests** to the Solution Architect (raw form: emails, tickets, meeting notes) spanning request types — dashboard, tracking/analytics, pipeline, ML, governance — to become golden-case inputs [S4].
- 3–5 **exemplar briefs/designs** the Solution Architect considers good — the target quality bar and few-shot/reference material.
- The **platform/standards corpus** for retrieval: current platform inventory, naming/design standards, governance policies (also fixes hallucinated-org-facts risk).
- 2–3 requests with **known planted gaps/risks** to test the agent's detection behavior (existing tests/cases.md approach, extended).

## Required evaluation criteria (pilot exit bar)

To be finalized in D6; evidence-based skeleton:

- Golden-case suite (≥20) green in CI; zero schema-invalid outputs [S4][S25].
- Judge rubric score ≥ threshold with judge calibrated against the architect's scoring [S3][S4].
- **pass^k consistency** on repeated runs of the same request (target set in D6) [S4].
- Architect sign-off: briefs are useful and safe to hand downstream (existing roadmap Phase-1 exit criterion) — the primary criterion, per the human-evaluation production norm [S9] **[Verified]**.
- Health metrics trending well during pilot: approval rate, edit distance, downstream rework, cost per brief.

## Workstreams and dependencies for the roadmap phase

The roadmap should be organized around six workstreams **[Recommendation]**:

```
WS1 Foundation platform (runner, schema enforcement, registries, secrets, envs)
      └─► WS2 SA Agent build (intake→clarify→retrieve→generate→validate→review)
                └─► WS4 Pilot & hardening (real requests, 100% review, tuning)
WS3 Evaluation & observability (golden cases, rubric, judge, tracing)  ──► gates WS2/WS4
WS5 Governance & security (guardrails, trimming, audit, HITL procedures) ──► gates WS4
WS6 Expansion readiness (handoff-contract validation with DE role, trigger
     monitoring, second-agent gating) — starts only after WS4 exit criteria
```

Hard dependencies: WS2 cannot pilot without WS3's golden cases and WS5's Level-100 controls; WS6 cannot start until the architect sign-off in WS4. WS1/WS3/WS5 can largely run in parallel with early WS2. The sequencing rationale already in `docs/roadmap.md` (SA → DE → governance/assurance → delivery → PM/orchestration) is consistent with the evidence and should be preserved, with each phase gated by written exit criteria [S1][S2][S5].
