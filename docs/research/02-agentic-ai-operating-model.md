# 02 — Agentic AI Operating Model

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — see it for the index
> and evidence-tier legend. Citations `[S#]` resolve in [references.md](references.md).
>
> This document answers *who owns, runs, approves, and is accountable for* agents in the Data & AI
> area. Architecture patterns are in [03](03-target-architecture.md); the per-agent lifecycle is in
> [12](12-development-lifecycle.md); governance artifacts are in
> [10](10-observability-and-governance.md).

## Design stance

**[Recommendation]** Run a **centralized platform with federated use-case ownership**: one shared
agent platform (runtime, retrieval, tools, registries, evals, observability) owned centrally, and
each *agent's outputs and golden cases* owned by the human role it supports. This is the only model
that fits both the evidence and the org's size.

Why not the alternatives, for an area of ~10 roles with 3 of them on temporary contracts
([01](01-company-and-operating-context.md)):

- **Fully centralized (one team owns everything, including domain judgment)** underuses domain
  experts and recreates the monolithic-agent failure mode — unwieldy scope, role drift, no
  independent per-domain updates [S8] **[Extracted]**.
- **Fully federated (each role builds its own agent its own way)** guarantees the five sprawl
  failure modes — functional duplication, shadow agents, orphaned agents, permission creep,
  unmonitored delegation [S13] **[Extracted]** — and, given quarterly stack churn [S17], produces
  as many incompatible stacks as there are builders.

The verified middle path: **capabilities used by ≥2 agents are centralized shared services; only
role-specific reasoning (prompts, schemas, golden cases) lives with the role** [S5][S13]. This is
already the repo's structure (`/shared` vs `/agents/<role>`).

## Ownership and accountability (RACI-lite)

**[Recommendation]**, grounded in [S6][S8][S13][S4] and the org in
[`org_structure.md`](../../shared/context/org_structure.md):

| Concern | Accountable | Responsible | Consulted |
|---|---|---|---|
| An agent's output quality & golden cases | The mapped human role (e.g., Solution Architect) | Same role + AI engineer | Downstream roles |
| Shared platform (runner, registries, CI, observability, retrieval) | A designated platform owner (initially Data Engineer + Solution Architect jointly — a duty, not a new hire) | AI engineer(s) | Architecture, Software Dev |
| Eval **infrastructure** (harness, judge, CI gates) | Platform owner | AI engineer | — |
| Eval **tasks/rubric** (what "good" means) | Mapped human role (domain expert) | Same | Value Assurance |
| New-agent approval, risk-tier changes, high-risk tools | **Head of Data & Analytics** (acting AI-Council with real decision rights) | Platform owner | Security, Compliance, Risk |
| Security, privacy, compliance controls | Head of D&A + Compliance/Risk | Platform owner | Legal |
| Registry hygiene (no shadow/orphaned agents) | Platform owner | AI engineer | Head of D&A |

Two evidence-backed non-negotiables: **every production agent has one accountable human owner**
(a Level-100 prerequisite [S6]), and **the AI-Council function has real decision rights** — a
council without a mandate drives governance bypass [S6] **[Extracted]**. Anthropic's most effective
model — *central eval infrastructure + domain-expert-contributed tasks* [S4] — is exactly the split
above **[Extracted]**.

## Platform team vs domain-agent teams

At current scale there is **no separate platform team** — there is a *platform duty* held by one or
two engineers, plus domain roles who contribute prompts, schemas, and golden cases for their own
agent. Promote to a standing platform team only when the agent portfolio and its maintenance load
justify it (a Level-4→5 concern; see [12](12-development-lifecycle.md) and the maturity model in
[14](14-risks-open-questions-and-decisions.md)). Building a platform team before there is a platform
to run is premature complexity (research principle #10).

## Human-in-the-loop, approval, and escalation

Two **mandatory** HITL triggers apply to every agent from day one [S1] **[Verified]**:

1. **Failure-threshold exceeded** — validator loop hits its iteration cap, repeated schema
   failures, or a low judge score → **escalate to the mapped human with the full trace attached.**
2. **High-risk / irreversible action** — any medium/high-risk (typically write) tool call →
   **pause and require explicit human approval** (propose-then-commit; see
   [07](07-data-and-integration-architecture.md)) [S51].

Escalation ladder **[Recommendation]**: agent self-check → mapped human reviewer → platform owner
(technical failures) or Head of D&A (risk/policy decisions). For financial-services-sensitive
actions, the always-human-approval list in [08](08-security-privacy-and-compliance.md) governs and
**cannot be delegated to the agent** regardless of confidence.

Approval model for *changes* (not runs): prompt/schema/tool changes ship only via PR with green
regression evals ([09](09-evaluation-and-testing.md)); new agents and risk-tier changes are
approved by the Head of D&A against a registry entry ([10](10-observability-and-governance.md)).

## Agent lifecycle (summary)

Full detail with artifacts and gates in [12](12-development-lifecycle.md). The operating-model view:

```
propose (gating test) → register (owner + risk tier) → build → eval gate
   → security review → UAT (100% human review) → controlled deploy → monitor
   → continuous improvement → retire
```

**Registry entry precedes production, always** — the anti-shadow-agent control [S13] **[Extracted]**.
Promotion between stages is gated on the previous stage's exit criteria; do not skip stages [S1][S2][S5].

## Environment separation

**[Recommendation]** Four zones, a Level-100 governance prerequisite [S6] **[Extracted]**:

| Zone | Purpose | Data | Autonomy |
|---|---|---|---|
| Experimentation | Prompt/pattern spikes, notebooks | Synthetic / de-identified only | None (human-driven) |
| Development | Building the agent + tools | Synthetic + a few sanitized real cases | Sandboxed tools |
| Test / staging | Golden-case regression, sandboxed tools, isolation tests | Golden dataset (sanitized) | Sandboxed only |
| Production | Real requests, 100% human review in pilot | Real (identity-trimmed, [08](08-security-privacy-and-compliance.md)) | Read-mostly; writes approval-gated |

Real customer/KYC data never enters experimentation. AgentCore Runtime provides session isolation
and per-session sandboxing that maps cleanly onto these zones if adopted [S26]
([05](05-platform-and-framework-comparison.md)).

## Orchestration ownership: single agent now, orchestrator only on a trigger

The operating model is **document-mediated, single-agent** today: the SA Agent emits handoff packets
addressed to *human* roles; there are no agent-to-agent calls. This matches the verified production
norm (80% of case-study systems use structured workflows, not open-ended autonomy [S9]).

Add agent-to-agent orchestration **only when a documented trigger fires** — see the decision matrix
below and the written triggers in [14](14-risks-open-questions-and-decisions.md). When it does, use
a **central orchestrator (manager / orchestrator-worker, agents-as-tools)**, never peer handoffs for
process automation [S1][S2][S5][S7] **[Verified]**.

### Decision matrix — orchestration ownership models

Scoring: ✅ strong fit · ⚠️ conditional · ❌ poor fit, for *this org at current maturity*.

| Model | Coordination cost | Sprawl risk | Auditability | Fit now | When to use |
|---|---|---|---|---|---|
| **Single agent, document-mediated handoffs** | Lowest | Lowest | Highest | ✅ | **MVP and near term** — the current design [S9] |
| Pipelined agents (downstream input schema = upstream handoff), still human-triggered | Low | Low | High | ⚠️ | Phase 2 — proves handoff contracts without an orchestrator [S3] |
| Central orchestrator (manager / orchestrator-worker) | Medium | Medium (registry-controlled) | Medium-High | ⚠️ | Only on a documented trigger; the sanctioned multi-agent shape [S1][S5] |
| Peer handoff / group chat / debate | High | High | Low | ❌ | Avoid for process automation — documented failure modes: infinite loops, unpredictable routing, stalls [S5] |
| Fully autonomous agent swarm | Highest | Highest | Lowest | ❌ | Not appropriate for a regulated FS environment at any near-term maturity |

**Assumptions:** current portfolio = one agent; team is small; environment is regulated (writes
gated). **Recommended use:** stay in row 1; design handoff schemas so row 2 is a cheap step; treat
row 3 as trigger-gated future work; never adopt rows 4–5 without a redesign and a compelling,
measured case.

## What this operating model deliberately postpones

- A standing platform team (until maintenance load justifies it).
- Any agent-to-agent autonomy (until a trigger fires).
- Agents for roles that have not re-passed the gating test with a concrete workflow
  ([13](13-future-agent-portfolio.md)).
