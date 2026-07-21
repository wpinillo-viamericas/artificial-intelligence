# Agentic AI for the Data & AI Area — Research Overview

> **Package index.** This is document 1 of 9 in the research package that precedes roadmap definition.
>
> 1. **research_overview.md** (this document) — executive summary, key findings, direction, risks, decisions
> 2. [reference_architecture.md](reference_architecture.md) — target architecture and layers
> 3. [agent_operating_model.md](agent_operating_model.md) — mapping agents to the Data & AI org
> 4. [solutions_architecture_agent_research.md](solutions_architecture_agent_research.md) — first-agent scope, I/O, templates, MVP
> 5. [technology_options.md](technology_options.md) — framework and technology comparison
> 6. [governance_security_and_risk.md](governance_security_and_risk.md) — security, HITL, prompt governance, risk register
> 7. [development_best_practices.md](development_best_practices.md) — repo, prompts, schemas, testing, CI/CD, observability
> 8. [implementation_prerequisites.md](implementation_prerequisites.md) — decisions, platforms, standards, and inputs the roadmap needs
> 9. [research_sources.md](research_sources.md) — sources, methodology, evidence tiers
>
> Citations `[S#]` resolve in [research_sources.md](research_sources.md), which also defines the evidence tiers used here: **[Verified]** (survived 3-vote adversarial verification), **[Extracted]** (single fetched source, quoted verbatim), **[Inference]** (our application of evidence to this org), **[Assumption]**, **[Open decision]**.

## Executive summary

The verified evidence converges on one strategy: **start with a single, tool-equipped, schema-first Solutions Architecture Agent built as a structured workflow with mandatory human review — and earn the right to expand, one trigger at a time.**

OpenAI, Anthropic, and Microsoft independently recommend maximizing one agent's capabilities at the lowest complexity level that reliably works before splitting into multiple agents [S1][S2][S5] **[Verified]**. The largest empirical study of production agents confirms this is how successful teams actually ship: 68% of deployed agents execute ≤10 steps before human intervention, 80% of case-study systems use predefined structured workflows rather than open-ended autonomy, and 85% are custom implementations calling model APIs directly rather than using heavy frameworks [S9] **[Verified]**. Multi-agent systems pay off only on parallelizable, high-value work, and cost ~15× the tokens of a chat interaction [S3] **[Verified]** — and open-source multi-agent systems fail at rates of 41–86.7%, mostly from specification and coordination defects, not model weakness [S10] **[Extracted]**.

The Solutions Architecture use case itself is well-founded. It passes OpenAI's three-part gating test for agent-worthiness (nuanced judgment, non-codifiable rules, unstructured inputs) [S1] **[Verified]**; requirements-to-architecture is the single most-studied GenAI application in software architecture research (40% of studies) [S12] **[Extracted]**; and a 2026 blind study found an orchestrated, human-supervised pipeline outperformed single-prompt LLMs at generating architecture decision records — with the largest gap in completeness [S11] **[Verified, preliminary]**.

The existing repository (schema-first agents, one role per agent, handoff packets, human-in-the-loop by default, Claude API runtime) is **already aligned with the strongest evidence**. The research does not call for a redesign; it calls for hardening what exists (evaluation harness, guardrails, tool access, registries, observability) before scaling to more roles.

## Key findings

Ordered by decision relevance. Full detail lives in the linked documents.

1. **The use case is agent-worthy — many neighboring workflows are not.** OpenAI's gating test (complex judgment / unmaintainable rules / unstructured data) admits the Solutions Architecture Agent but would reject deterministic work like rule-based data-quality checks, which should remain conventional automation [S1] **[Verified]**. → [agent_operating_model.md](agent_operating_model.md)

2. **Single-agent-first is the unanimous vendor recommendation and the production norm.** Split into multiple agents only on documented triggers: instruction-following failures, tool overload/confusion, or parallelizable work exceeding one context window [S1][S2][S5][S9] **[Verified]**. → [reference_architecture.md](reference_architecture.md)

3. **"Workflow, not free-running agent" is the right internal shape.** Anthropic distinguishes workflows (predefined code paths) from agents (model-directed control) and recommends workflows for predictable tasks [S2] **[Verified]**. The SA Agent's intake → retrieve → generate → validate pipeline is predictable; AgenticAKM demonstrates exactly this decomposition with bounded (≤3-iteration) validator loops beating single prompts [S11] **[Verified, preliminary]**.

4. **When multi-agent expansion is eventually justified, use a central orchestrator, not peer handoffs.** All four vendor taxonomies steer enterprise process automation toward centralized orchestration (OpenAI "manager", Anthropic "orchestrator-workers", AWS "workflow agents", Microsoft's pattern table with explicit failure modes: handoff → infinite loops; magentic → stalls on ambiguity) [S1][S2][S5][S7] **[Verified]**. → [reference_architecture.md](reference_architecture.md)

5. **Multi-agent economics are unforgiving.** ~90% gains appear only on breadth-first parallelizable tasks; token spend explains 80% of the performance variance; multi-agent ≈15× chat cost; single agents match multi-agent under equal token budgets [S3][S14][S15] **[Verified]**. The SA pipeline is largely sequential/shared-context — a single-agent fit; a later parallel research/assessment phase is where subagents would pay.

6. **Delegation contracts are the #1 multi-agent failure surface.** Vague orchestrator instructions cause duplicated work and gaps; each delegation needs an explicit objective, output format, tool/source guidance, and boundaries [S3] **[Verified]**. MAST attributes 41.8% of multi-agent failures to specification/design defects [S10] **[Extracted]**. The repo's handoff-packet schema is the right artifact to evolve into these contracts **[Inference]**.

7. **Enterprise controls are convergent and required from the MVP, scaled to risk.** Layered guardrails; per-tool low/medium/high risk ratings; two mandatory HITL triggers (failure thresholds exceeded; high-risk/irreversible actions); least-privilege with per-agent identity-aware security trimming (an agent must never return data its requesting user can't access); audit trails; content checks at input, tool call, tool response, and output [S1][S5] **[Verified]**. The SA Agent's profile is favorable — read-mostly, producing human-reviewed documents — but identity-aware retrieval and audit logging are day-one requirements **[Inference]**. → [governance_security_and_risk.md](governance_security_and_risk.md)

8. **Human evaluation is the production QA norm; start small and early.** 74% of deployed agents rely primarily on human evaluation; 75% of case-study teams ship without formal benchmarks; LLM-as-judge is used as a pre-screen paired with human review [S9] **[Verified]**. Anthropic: start with 20–50 eval tasks drawn from real failures; grade outcomes, not tool-call paths; use pass^k for consistency-critical outputs [S4] **[Extracted]**. → [development_best_practices.md](development_best_practices.md)

9. **Stack churn is real — design for modularity, not framework lock-in.** Only ~5% of surveyed organizations have agents in production; 70% of regulated enterprises rebuild their agent stack every ≤3 months; observability/evals are the weakest and most-invested layer [S17] **[Extracted]**. Custom-lightweight over heavy framework is both the evidence-backed and repo-consistent choice [S2][S9] **[Verified]**. → [technology_options.md](technology_options.md)

10. **Registries and tiered governance prevent the failure mode that kills agent ecosystems: sprawl.** Agent, tool, and prompt registries with owner, risk tier, scopes, and rollback; governance tiered by agent criticality (uniform controls are an explicit Microsoft anti-pattern); a governance level with formal policies + central catalog + RBAC + HITL is the minimum before scaling [S6][S8][S13] **[Extracted]**. → [governance_security_and_risk.md](governance_security_and_risk.md)

## Recommended strategic direction

**[Recommendation]** — synthesized from the findings above; rationale and alternatives in the linked docs.

1. **Confirm the current repo direction.** One role-scoped, schema-first agent; structured workflow internals (intake → clarify → retrieve → generate → validate → human review); human approval on every output. No redesign needed — harden.
2. **Build the SA Agent as a bounded workflow on direct model APIs** (Anthropic Claude API / Agent SDK per existing `config.yaml`), with schema-enforced outputs via tool-use, a validator step with a bounded refinement loop, and an ask-first intake stage [S2][S11][S23][S25].
3. **Stand up the shared substrate before the second agent, not after:** tool registry, prompt/schema versioning, evaluation harness (20–50 golden tasks), tracing/observability, agent registry with owner and risk tier [S1][S4][S8][S13].
4. **Defer multi-agent orchestration until a documented trigger fires** (instruction failures, tool overload, parallel work exceeding context). When it fires, adopt orchestrator-worker with explicit delegation contracts — evolve the existing handoff schemas into those contracts [S1][S3][S5].
5. **Keep deterministic work deterministic.** Do not wrap rule-based checks (schema validation, lint-style governance checks) in LLM calls; run them as code, optionally CI-integrated (fitness-function style) [S1][S22].
6. **Adopt recognized documentation standards for outputs:** ADRs (MADR/Nygard-style), arc42-informed brief structure, C4 diagrams as text (Mermaid/Structurizr DSL/PlantUML) so diagrams are versionable and regenerable [S22][S23][S24].

## Major risks

Top-line register; the full risk register with mitigations is in [governance_security_and_risk.md](governance_security_and_risk.md).

| Risk | Evidence anchor | Severity |
|---|---|---|
| Plausible-but-wrong architecture recommendations accepted without scrutiny ("architectural degradation from blind trust") | [S12] warns explicitly; mitigated by mandatory architect sign-off + assumptions/open-questions surfacing | High |
| Weak evaluation: shipping prompt/schema changes without regression evidence — the field's most-cited gap | [S12] (rigorous testing "typically missing"), [S4], [S17] | High |
| Data leakage through retrieval: agent surfaces catalog/Confluence content the requesting user can't access | [S5] security trimming requirement | High |
| Agent sprawl as the ecosystem grows: duplicated capabilities, shadow/orphaned agents, permission creep | [S13] taxonomy; [S6] tiered governance | Medium→High at scale |
| Premature multi-agent complexity: 41–86.7% failure rates, 15× cost, fragile coordination | [S10][S3][S16] | High if triggered early |
| Framework lock-in amid quarterly stack churn | [S17] | Medium |
| Over-automation of judgment roles; correct posture is augment/advise, with humans as final verifiers | [S9] (92.5% of agents serve humans; internal-first), [S12] (85% assistive) | Medium |
| Inconsistent output formats breaking downstream handoffs | Mitigated by schema-first + validation; [S25] | Medium |

## Major decisions needed before implementation

Summarized here; full decision list with options and defaults in [implementation_prerequisites.md](implementation_prerequisites.md).

1. **Runtime & hosting** — where the agent actually runs (thin custom runner on Claude API per current config; hosted where?), and environment separation (dev/test/prod). **[Open decision]**
2. **Knowledge & retrieval scope for MVP** — which sources the agent may read (data catalog? Confluence? prior briefs?) and how identity-aware access is enforced. **[Open decision]**
3. **Intake channel** — where requests arrive (form, Jira ticket, Slack/Teams, chat UI) and where outputs land (Confluence page, Jira epics, repo files). **[Open decision]**
4. **Output standards adoption** — confirm ADR template (MADR vs Nygard), whether the brief aligns to arc42 sections, and the diagram-as-code format. **[Open decision]**
5. **Evaluation ownership & rubric** — who curates the 20–50 golden cases, who signs off outputs during pilot, and what the pass bar is. **[Open decision]**
6. **Governance minimum** — adopt registries (agent/tool/prompt) and risk-tiering now vs at second agent; who chairs approval (Head of Data & Analytics as accountable owner?). **[Open decision]**
7. **Multi-agent trigger definition** — write down, in advance, the observable conditions that justify splitting the agent. **[Open decision]**
