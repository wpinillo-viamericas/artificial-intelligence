# 00 — Executive Summary & Library Index

> **Agentic AI Research Library** for the Viamericas **Data & Artificial Intelligence** area.
> Research phase only — this library produces *evidence and decisions*, **not** an implementation
> roadmap and **not** working agents. It supersedes and expands the 2026-07-06 package now archived
> at [`agentic-ai-data-area/`](agentic-ai-data-area/README.md); the operative roadmap at
> `docs/roadmap/agentic_ai_roadmap.md` is unchanged.

## How to read this library

Every non-trivial claim carries an **evidence tier** and, where external, a `[S#]` citation
resolving in [references.md](references.md):

- **[Verified]** — survived 3-vote adversarial verification (Pass 1, 2026-07-06).
- **[Extracted]** — quoted from a single fetched source (incl. the mid-2026 Pass-2 refresh); "the
  source says X," not independently corroborated.
- **[Inference]** — our reasoned application to this org.
- **[Recommendation]** — our proposed course of action.
- **[Assumption]** / **[Open decision]** — explicitly unconfirmed; tracked in
  [14](14-risks-open-questions-and-decisions.md).

Established facts are kept visibly separate from recommendations, and Viamericas-environment
specifics are labeled `[Assumption]` — **nothing is invented**.

## Library index

| # | Document | Answers |
|---|---|---|
| 00 | **This document** | Direction, principles, platforms, risks, org implications, decisions, SA-Agent scope |
| 01 | [Company & operating context](01-company-and-operating-context.md) | Business, products, channels, priorities, the D&AI org & operating model |
| 02 | [Agentic AI operating model](02-agentic-ai-operating-model.md) | Ownership, RACI, HITL, approval/escalation, environments, orchestration matrix |
| 03 | [Target architecture](03-target-architecture.md) | Layered platform, agent patterns, memory/state, diagrams |
| 04 | [Solutions Architecture Agent](04-solutions-architecture-agent.md) | The first agent: users, JTBD, capability tiers, I/O, tools, review points |
| 05 | [Platform & framework comparison](05-platform-and-framework-comparison.md) | Bedrock/AgentCore/LangGraph/… 15-criteria matrix; build vs buy |
| 06 | [Knowledge & retrieval architecture](06-knowledge-and-retrieval-architecture.md) | Hybrid search, ACL-filtered RAG, freshness, GraphRAG decision |
| 07 | [Data & integration architecture](07-data-and-integration-architecture.md) | MCP-vs-native per system; auth, rate limits, idempotency, approval |
| 08 | [Security, privacy & compliance](08-security-privacy-and-compliance.md) | Threat model, guardrails, FS compliance, always-human-approval list |
| 09 | [Evaluation & testing](09-evaluation-and-testing.md) | Golden cases, judges, pass^k, SLIs, eval-platform matrix |
| 10 | [Observability & governance](10-observability-and-governance.md) | Tracing (OTel), governance artifacts, registry, risk tiering |
| 11 | [Cost & scalability](11-cost-and-scalability.md) | Cost drivers, caching, routing, the vector-store trap, showback |
| 12 | [Development lifecycle](12-development-lifecycle.md) | 12 stages with artifacts & approval gates |
| 13 | [Future agent portfolio](13-future-agent-portfolio.md) | Candidate agents scored (no final sequence) |
| 14 | [Risks, open questions & decisions](14-risks-open-questions-and-decisions.md) | Risk register, maturity model, D1–D12, Q1–Q12, **roadmap handoff** |
| — | [references.md](references.md) | Sources `[S1]–[S88]`, methodology, bias caveats |

## Recommended direction

The evidence converges on one strategy: **start with a single, tool-equipped, schema-first
Solutions Architecture Agent built as a bounded workflow with mandatory human review — and earn the
right to expand, one written trigger at a time.**

OpenAI, Anthropic, and Microsoft independently recommend maximizing one agent at the lowest
complexity that reliably works before splitting into multiple agents [S1][S2][S5] **[Verified]**. The
largest production study confirms this is how teams actually ship: 68% of agents run ≤10 steps, 80%
use structured workflows, 85% are custom implementations calling model APIs directly [S9]
**[Verified]**. Multi-agent systems cost ~15× the tokens and fail at 41–86.7% in immature setups
[S3][S10]. The Solutions Architecture use case is well-founded: it passes the agent-worthiness
gating test [S1], is the #1-studied GenAI architecture application [S12], and an orchestrated
human-supervised pipeline beat single prompts at it [S11].

**The existing repository is already aligned with the strongest evidence** (schema-first, one role
per agent, handoff packets, human-in-the-loop by default, Claude API runtime). The research calls
for *hardening* — evals, guardrails, retrieval, registry, observability — not a redesign.

## Major architectural principles

1. **Business value before autonomy** — build an agent only where it improves a measurable outcome.
2. **Deterministic where possible** — never put an LLM on a path that rules/SQL/APIs handle more
   reliably (attribution, reconciliation, data-quality checks).
3. **Human accountability** — agents prepare; humans approve architecture, compliance, and any
   system-of-record write. The SA Agent **publishes and approves nothing**.
4. **Grounded outputs** — every recommendation traces to an authoritative internal source or
   approved standard; assumptions and open questions are explicit.
5. **Least privilege** — identity-trimmed retrieval; scoped, risk-rated tools; agent as a governed
   non-human identity.
6. **Modular platform** — centralize retrieval, tools, memory, evals, observability, governance;
   keep prompts/schemas/evals as framework-independent repo data (stack churns quarterly [S17]).
7. **Incremental** — one agent, one channel, small corpus; expand only on documented triggers.
8. **Measurement from inception** — every agent has business KPIs, technical SLIs, eval criteria,
   and retirement conditions.

## Main platform options

For a regulated, AWS-hosted, low-volume internal agent (full matrix in
[05](05-platform-and-framework-comparison.md)):

- **MVP core:** custom-lightweight thin runner on the **Anthropic Claude API**, structured output via
  tool-use — the verified category choice and the current `config.yaml`.
- **Managed runtime (when operational burden grows):** **Amazon Bedrock AgentCore** (GA 2025-10;
  managed runtime/memory/gateway/identity/observability; GovCloud; MCP-native) — host the *same* thin
  agent with minimal change.
- **Orchestration (only on a trigger):** **LangGraph 1.0** for durable graph control.
- **Retrieval:** Bedrock Knowledge Bases → OpenSearch (hybrid) or scale-to-zero NextGen Serverless /
  S3 Vectors → rerank → **ACL-filtered via Verified Permissions**.
- **Integrations:** **MCP-first** where an official server exists (Atlassian GA 2026-02, GitHub GA
  2025-09, AWS), native REST otherwise.
- **Eval/observability:** Bedrock Evaluations + Ragas; CloudWatch GenAI + Langfuse/Phoenix over OTel
  `gen_ai.*` spans.

**Centralize** shared services; **build** the agent's reasoning/contracts/golden cases; **buy/reuse**
managed runtime, retrieval, observability, and eval tooling.

## Critical risks

Full register in [14](14-risks-open-questions-and-decisions.md). The ones that most shape decisions:

- **Plausible-but-wrong recommendations accepted on blind trust** (R1) — mitigated by mandatory
  architect sign-off, options-with-tradeoffs, and required assumptions/open-questions [S12].
- **Weak evaluation → silent quality drift** (R4) — the field's most-cited gap; 20–50 golden cases
  and a CI regression gate are day-one requirements [S4][S12].
- **Data leakage via retrieval / cross-user exposure** (R3, R11) — identity-trimmed, ACL-filtered
  retrieval and validated session isolation [S5][S39][S21].
- **Prompt injection & retrieval poisoning** (R13, R14) — treat retrieved content as untrusted;
  approved-source allowlist; red-team set [S53][S54].
- **Premature multi-agent complexity** (R6) and **framework lock-in** (R8) — stay single-agent on a
  thin, swappable core until a written trigger fires [S3][S10][S17].
- **Cost dominated by the vector-store idle floor** (R12), not tokens — use a scale-to-zero store
  [S87].

## Key organizational implications

- **Centralized platform + federated use-case ownership.** A *platform duty* (one or two engineers),
  not yet a platform team; each agent's outputs and golden cases owned by its mapped human role.
- **The Head of Data & Analytics is the accountable AI-Council with real decision rights** —
  approving agents, risk tiers, and high-risk tools.
- **Governance is infrastructure, not inspection:** Microsoft Level-100 controls at launch → Level-
  300 / AAGMM-3 before agent #2; a central registry (already seeded) gates production.
- New skills needed: eval/rubric authoring, tracing/observability, retrieval/ACL engineering, and
  agent governance — mostly *duties on existing roles* at current scale.

## Major decisions required before implementation

Twelve, detailed in [14](14-risks-open-questions-and-decisions.md): **D1** runtime/hosting & env
separation · **D2** model-provider terms (region/retention/ZDR) · **D3** MVP corpus + identity
trimming · **D4** intake/output surfaces · **D5** output standards (ADR/arc42/diagram) · **D6** eval
ownership & pass bar · **D7** governance minimum (adopt registries now) · **D8** multi-agent triggers
· **D9** integration transport (MCP-first) · **D10** budget guardrails · **D11** model-risk gate for
higher-tier agents · **D12** observability stack. Plus open questions **Q1–Q12** (cloud/data reality,
IAM, residency, permission models, deployment/CI, headcount/ownership, source-of-truth) that must be
**confirmed with the business, not assumed**.

## Recommended scope boundaries for the Solutions Architecture Agent

Detailed in [04](04-solutions-architecture-agent.md). In brief:

- **Does:** turn requests into schema-valid Solution Architecture Briefs with options, risks,
  dependencies, ADRs, a C4 diagram, and per-role handoffs — grounded, cited, and always
  human-reviewed. Reads (intermediate) Jira/Confluence/GitHub via MCP.
- **Does NOT:** design pipeline internals, write SQL, build dashboards, define event schemas, author
  ML features, or write governance-policy detail (it emits *requirements* for those); assume
  unconfirmed platforms; invent facts; **publish to or approve anything in a system of record**;
  approve production architecture.

## Handoff to the roadmap phase

The consolidated inputs the next phase must consume are in
**[14 → "Inputs Required for the Agentic AI Implementation Roadmap"](14-risks-open-questions-and-decisions.md#inputs-required-for-the-agentic-ai-implementation-roadmap)**.
That phase — not this one — produces the sequence, dates, and per-agent backlog, beginning with the
Solutions Architecture Agent.
