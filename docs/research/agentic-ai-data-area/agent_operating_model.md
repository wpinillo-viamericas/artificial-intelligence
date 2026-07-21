# Agent Operating Model — Mapping Agents to the Data & AI Organization

> Document 3 of 9 — see [research_overview.md](research_overview.md) for the index; citations `[S#]` in [research_sources.md](research_sources.md).
>
> **Evidence caveat:** no adversarially-verified claims directly addressed agent-to-role mapping for this specific org. This document applies verified general principles (gating test, automate/augment posture, sprawl prevention, orchestration patterns) to the org structure in `shared/context/org_structure.md`. Role-mapping conclusions are **[Inference]** unless tagged otherwise.

## Principles that govern the mapping

1. **Gate every proposed agent through OpenAI's three-part test** — complex/nuanced decision-making, difficult-to-maintain rules, heavy reliance on unstructured data; otherwise build deterministic automation instead [S1] **[Verified]**. This single test prevents most sprawl before it starts.
2. **Augment, don't automate, judgment roles.** 92.5% of production agents serve human users; humans act as final verifiers; even external-facing systems augment domain experts rather than replace them [S9] **[Verified]**. In GenAI-for-architecture research specifically, 85% of systems are assistive/human-in-the-loop [S12] **[Extracted]**.
3. **One agent's output is the next agent's (and next role's) input.** Structured handoff packets are the collaboration contract — and the future delegation contracts if an orchestrator is added [S3] **[Verified — delegation specification]**.
4. **Prevent duplication structurally, not by policy memo.** The five sprawl failure modes — functional duplication, shadow agents, orphaned agents, permission creep, unmonitored delegation [S13] **[Extracted]** — are countered by: a central agent registry with owners [S6][S8], shared services instead of per-agent copies, and the one-role-one-agent boundary rule.
5. **Add an agent only when the previous one is trusted.** Incremental expansion is the vendor-recommended path [S1][S2][S5] **[Verified]**; the existing roadmap's phase gating ("exit criteria" per phase) matches this.

## Role-by-role mapping

Posture legend — **Augment**: agent drafts, human owns and approves. **Advise**: agent answers questions/reviews artifacts, produces no primary deliverables. **Automate (partial)**: agent executes bounded, verifiable steps with spot-check review. Nothing in this org merits full automation at current maturity **[Inference]** (consistent with [S9][S12]).

| Role | Agent (eventually) | Posture | Gating-test fit | Notes |
|---|---|---|---|---|
| Solution Architect | **Solutions Architecture Agent** (first) | Augment | Strong — ambiguous unstructured requests, nuanced trade-offs [S1] | Translation bottleneck of the org; produces the artifacts every downstream role consumes. See [solutions_architecture_agent_research.md](solutions_architecture_agent_research.md) |
| Data Engineer | Data Engineering Agent (phase 2) | Augment | Strong for pipeline design/data-contract drafting; weak for mechanical codegen tasks that tooling already does | First consumer of the SA brief's `data_engineering` handoff; proves the handoff contract end-to-end |
| Data Governance Specialist (+ 3 contract Analysts) | Data Governance Agent | Augment (Specialist) / Automate-partial (Analyst tasks) | Mixed — policy interpretation is nuanced; metadata cleanup and cataloging are rule-bound | The temporary-contract Analyst workload (documentation, cataloging, stewardship ops) is the org's best candidate for *partial automation with review*, precisely because it is structured and high-volume — matching the "constrained, high-volume, measurable" profile of successful first deployments [S17] **[Extracted]** |
| Data Assurance Specialist | Data Assurance Agent | Augment for QA-rule *generation*; the checks themselves stay deterministic | Partial — generating validation logic is judgment; running checks is not [S1] | Anti-pattern to avoid: an LLM agent "checking data quality" at runtime. Generate rules once; execute as code |
| Value Assurance Specialist | Value Assurance Agent | Advise → Augment later | Moderate — value/metric alignment review is judgment over unstructured briefs | Consumes `success_metrics` + `business_context`; natural LLM-critique role |
| Data Visualization Specialist | Data Visualization Agent | Augment | Moderate | Dashboard requirements, KPI mapping from the `visualization` handoff |
| Digital Analytics Specialist | Digital Analytics Agent | Augment; Automate-partial for schema generation | Moderate–strong (event taxonomy from unstructured requirements) | GA4 event schemas, tagging docs — highly schematizable outputs |
| Data Scientist | Data Science Agent | Augment | Strong for experiment framing/model documentation | Model framing, experiment design from the `data_science` handoff |
| Project Manager | Project Management Agent | Augment; Automate-partial for status synthesis | Moderate — RAID/dependency extraction from structured briefs is semi-mechanical | Aggregates *other agents'* structured outputs; benefits most from the ecosystem existing first — correctly sequenced last in the current roadmap |
| Head of Data & Analytics | No dedicated agent; portfolio *view* over registry + outputs | Advise | Weak for an "agent"; strong for reporting | A dashboard over agent outputs/registry, not an LLM agent **[Recommendation]** |

**Which roles get no agent at all:** none are excluded permanently, but every one of the above must re-pass the gating test with a concrete workflow before build — several will resolve to deterministic tooling plus a thin advisory copilot rather than a full agent **[Recommendation]**.

## Boundaries between agents

- **One role, one agent, one job** (existing principle #1) — an agent reaching into another role's depth produces a *handoff*, not a deeper answer. This is the structural fix for role confusion across agents **[Inference]**, and it mirrors why monolithic do-everything agents fail: unwieldy instructions, role drift, and no independent per-domain updates [S8] **[Extracted]**.
- **Boundaries are enforced by schema, not prompt willpower:** each agent's output schema only contains its role's artifacts plus typed handoffs (`downstream_role` enum). Adding agents without meaningful specialization is an explicit Microsoft antipattern [S5] **[Verified]**.
- **Tools are shared; reasoning is not.** Two agents may use the same retrieval or Jira tool from the registry; they must not both "draft data contracts" — capability overlap is resolved by moving the capability to whichever agent's role owns it and handing off.

## Collaboration patterns between agents

Phased, matching the verified escalation path:

1. **Now (single agent):** the SA Agent emits handoff packets addressed to *human* roles. Collaboration is document-mediated; no agent-to-agent calls.
2. **Phase 2+ (pipelined agents):** downstream agent's input schema = upstream agent's handoff schema, still human-triggered ("human-in-the-loop relay"). This proves contracts without orchestration complexity.
3. **Later (orchestrated):** a central orchestrator routes an initiative through relevant agents and reassembles an initiative package — **manager/orchestrator-worker pattern, agents-as-tools; not peer handoffs, not group chat** [S1][S2][S5][S7] **[Verified]**. If any group-chat/debate step is ever used (e.g., design review), cap at ≤3 agents with maker-checker acceptance criteria, an iteration cap, and human fallback [S5] **[Verified]**.
4. Delegations at stage 3 use explicit task contracts (objective, output format, tools/sources, boundaries) — evolved from today's handoff packets [S3] **[Verified]**. Do not share mutable state between concurrent agents [S5] **[Verified]**.

Parallel fan-out (multiple agents on one initiative concurrently) is justified only for genuinely independent subtasks — the parallelizable-vs-sequential criterion [S3][S14] **[Verified]** — and carries ~15× token economics [S3] **[Verified]**.

## Ownership and governance model

**[Recommendation]**, grounded in [S6][S8][S13][S4]:

| Concern | Owner |
|---|---|
| Accountable owner per agent (required at governance Level 100 [S6]) | The human in the mapped role (e.g., Solution Architect owns the SA Agent's outputs and golden cases) |
| Platform/shared services, registries, CI, observability | One designated engineering owner (initially Data Engineer + Solution Architect jointly; a de-facto "agent platform" duty, not a new hire) |
| Eval infrastructure centralized; eval *tasks* contributed by domain experts | Mirrors Anthropic's most effective org model: dedicated eval infra ownership + domain-expert task contribution [S4] **[Extracted]** |
| Approval authority for new agents, risk-tier changes, high-risk tools | Head of Data & Analytics (acting AI-Council function; a council without real decision rights drives governance bypass [S6] **[Extracted]**) |
| Agent registry hygiene (no shadow/orphaned agents) | Platform owner; registry entry is a precondition for running in prod [S8][S13] |

Governance intensity is **tiered by agent risk/criticality** — uniform controls are an anti-pattern that either drives shadow AI or under-governs critical agents [S6] **[Extracted]**. The SA Agent (internal, read-mostly, human-reviewed documents) sits in the low-to-moderate tier; future agents that write to systems of record tier higher. Full model in [governance_security_and_risk.md](governance_security_and_risk.md).
