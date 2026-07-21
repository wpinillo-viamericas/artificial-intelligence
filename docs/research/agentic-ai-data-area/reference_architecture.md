# Reference Architecture for Agentic AI in the Data & AI Area

> Document 2 of 9 — see [research_overview.md](research_overview.md) for the package index and [research_sources.md](research_sources.md) for citations `[S#]` and evidence tiers ([Verified] / [Extracted] / [Inference] / [Recommendation] / [Open decision]).

## Design stance

**[Recommendation]** The target architecture is a **layered platform with exactly one production agent at first**, built so each additional agent reuses the shared layers instead of duplicating them. This follows the strongest verified guidance:

- Use the lowest complexity level that reliably meets requirements; a single agent with tools is often the right enterprise default [S1][S5] **[Verified]**.
- Prefer *workflows* (predefined code paths) over free-running *agents* for predictable tasks [S2] **[Verified]**.
- Production agents overwhelmingly run bounded (≤10 step), structured, custom-built pipelines [S9] **[Verified]**.
- When multi-agent is eventually justified, use a central orchestrator over role specialists — never peer handoffs for process automation [S1][S2][S5][S7] **[Verified]**.

## Target architecture (layers)

```
┌──────────────────────────────────────────────────────────────────────┐
│  EXPERIENCE LAYER                                                    │
│  Intake channels (form / Jira / Slack / chat UI) · Output surfaces   │
│  (Confluence, Jira, repo) · Human review & approval UI               │
├──────────────────────────────────────────────────────────────────────┤
│  AGENT LAYER (grows over time; starts with one)                      │
│  Solutions Architecture Agent  →  later: DE, Governance, Assurance…  │
│  Each agent = prompt + config + input/output schemas + tests         │
│  (Future) Orchestrator — added only when a documented trigger fires  │
├──────────────────────────────────────────────────────────────────────┤
│  SHARED SERVICES LAYER (build before agent #2)                       │
│  Agent runner · Prompt composition · Schema validation ·             │
│  Agent/Tool/Prompt registries · Shared context (org ground truth)    │
├──────────────────────────────────────────────────────────────────────┤
│  TOOLING LAYER                                                       │
│  Typed, registered tools: retrieval, catalog lookup, ticket/page     │
│  creation, diagram rendering — each with risk rating & scopes        │
├──────────────────────────────────────────────────────────────────────┤
│  MEMORY & RETRIEVAL LAYER                                            │
│  RAG over approved sources · prior briefs/ADRs · session state       │
│  (identity-aware: security-trimmed per requesting user)              │
├──────────────────────────────────────────────────────────────────────┤
│  EVALUATION & OBSERVABILITY LAYER                                    │
│  Golden-case evals · LLM-as-judge pre-screen · trace capture ·       │
│  token/cost metering · failure taxonomy tagging                      │
├──────────────────────────────────────────────────────────────────────┤
│  GOVERNANCE & SECURITY LAYER (cross-cutting)                         │
│  AuthN/Z & least privilege · guardrails at 4 checkpoints ·           │
│  audit log · version control · environment separation · approvals    │
└──────────────────────────────────────────────────────────────────────┘
```

## Layer-by-layer

### 1. Experience layer

Requests enter through an intake channel and outputs land where downstream roles already work. **[Open decision]** which channel ships first (see [implementation_prerequisites.md](implementation_prerequisites.md)). Two evidence-backed constraints:

- **Ask-first intake**: no generation until clarifying questions are answered or gaps are explicitly recorded as `open_questions`/`assumptions` — the pattern used by the arc42 toolkit ("no generation happens until you have answered") [S23] **[Extracted]** and already encoded in the repo's design principle #3.
- **Human review is part of the product, not an afterthought**: 92.5% of production agents serve human users, with humans as final verifiers; internal-first deployment is the standard risk posture [S9] **[Verified]**.

### 2. Agent layer

One folder per agent (existing `/agents` convention), each a **bounded workflow** internally:

```
intake → clarify → retrieve → generate → validate → render → human review
```

- The AgenticAKM study validates this exact decomposition for architecture outputs — extraction/retrieval/generation/validation stages with a bounded validator-driven refinement loop (≤3 iterations) and a supervising human architect [S11] **[Verified, preliminary]**.
- The validate stage should combine deterministic checks (schema validity, enum conformance, cross-reference consistency — cheap code, not LLM calls) with an LLM critique pass; maker-checker loops need explicit acceptance criteria, an iteration cap, and a fallback (escalate to human) [S5] **[Verified]**.
- **No orchestrator exists in the MVP.** It is added only when one of the documented triggers fires: instruction-following failures, tool overload/confusion, or parallelizable work exceeding a context window [S1][S5] **[Verified]**. When added, it follows the manager/orchestrator-worker pattern with agents-as-tools, not peer handoffs (handoff pattern's documented failure modes: infinite loops, unpredictable routing) [S1][S5] **[Verified]**.
- Delegation between orchestrator and workers uses **explicit task contracts** — objective, output format, tool/source guidance, boundaries — because vague delegation is the primary multi-agent failure mode [S3] **[Verified]**; 41.8% of multi-agent failures trace to specification defects [S10] **[Extracted]**. The repo's handoff-packet schemas are the natural seed for these contracts **[Inference]**.

### 3. Shared services layer

Everything more than one agent will need, centralized once:

| Service | Function | Evidence |
|---|---|---|
| Agent runner | Loads `config.yaml`, composes prompt (shared blocks + role prompt + injected context), calls model, validates output against schema, stamps metadata | Schema-first pipeline pattern [S25] **[Extracted]**; matches existing repo plan |
| Prompt composition | Shared base prompts + role prompts, versioned in git | Prompt registry with lineage/rollback [S8] **[Extracted]** |
| Registries (agent/tool/prompt) | Owner, purpose, risk tier, scopes, evaluation status, version | [S8] **[Extracted]**; central agent catalog is part of minimum viable governance [S13] **[Extracted]** |
| Shared context | Org structure, operating model, platform standards — injected, never hardcoded | Existing repo principle #6; instructions should derive from existing operating procedures [S1] **[Extracted]** |

**Centralize vs role-specific rule [Recommendation]:** capabilities used by ≥2 agents (retrieval, validation, rendering, registries, evals) are shared services; only role-specific reasoning (prompts, schemas, golden cases) lives in the agent folder. This is the direct answer to "what should be centralized versus role-specific" and the main defense against functional duplication — one of the five sprawl failure modes [S13] **[Extracted]**.

### 4. Tooling layer

- Tools are **typed, documented, registered, and reusable** across agents (many-to-many), preventing redundant definitions [S1] **[Verified — tool registry guidance]**.
- Each tool carries a **risk rating** (low/medium/high) from read/write access, reversibility, permissions, and impact; high-risk tools trigger pause/escalation [S1] **[Verified]**.
- Tool overload is driven by *similarity/overlap*, not raw count — some agents handle 15+ distinct tools while others fail with fewer than 10 overlapping ones [S1] **[Extracted]**. Keep tools few and orthogonal in the MVP.
- Tool design deserves prompt-level engineering attention (the "agent-computer interface"): Anthropic spent more time optimizing tools than prompts, and a single interface change (absolute paths) eliminated an error class [S2] **[Extracted]**. Improving tool descriptions measurably helps — a 40% task-time reduction in Anthropic's case [S3] **[Extracted]**.
- **[Open decision]** Tool transport: direct function calling vs MCP servers for enterprise integrations (Jira/Confluence/catalogs). MCP standardizes reuse across agents and IDE surfaces; direct calls are simpler for the first tool or two. Concrete integration patterns were *not* adversarially verified by this research — treat as an area for a spike ([implementation_prerequisites.md](implementation_prerequisites.md)).

### 5. Memory & retrieval layer

- **MVP: RAG over a small approved corpus** (org context, platform standards, prior briefs/ADRs, selected catalog metadata). Naive full-context stuffing fails: architectural knowledge exceeds single-prompt effective context, and long-context models still degrade (context rot / lost-in-the-middle) [S11] **[Verified]**.
- **Identity-aware, security-trimmed retrieval is non-negotiable**: the agent must never return data the requesting user cannot access, enforced per agent across every knowledge store [S5] **[Verified]**.
- Session state must live in explicit, persistent, isolated storage — a documented production failure mode is in-memory session loss and cross-user session leakage from misconfigured storage (Google ADK on Cloud Run) [S21] **[Extracted]**.
- Long-running work should prefer **context compression** (summarize history into key decisions/events) over spawning parallel context windows [S16] **[Extracted]**.
- Long-term "organizational memory" (accumulating reusable architecture knowledge across requests) is a later-maturity feature — defer past MVP **[Recommendation]**.

### 6. Evaluation & observability layer

Detailed practices in [development_best_practices.md](development_best_practices.md). Architectural requirements:

- **Trace capture of every prompt, response, and tool call** in a structured timeline — a production necessity, and the layer teams are least satisfied with and investing most in [S18][S17] **[Extracted]**.
- **Golden-case regression suite** (start at 20–50 tasks from real failures) wired into CI [S4] **[Extracted]**.
- **LLM-as-judge pre-screen paired with human review** — never judge-only [S9] **[Verified]**; a single rubric-scoring judge call (0.0–1.0 + pass/fail) outperformed panels of specialized judges [S3] **[Extracted]**.
- **Failure tagging** using a taxonomy (MAST's 14 modes / 3 categories is a ready-made rubric; its LLM-judge annotation pipeline hit 94% accuracy vs experts) [S10] **[Extracted]**.
- **Token/cost metering per run and per agent** — cost drives architecture decisions at every level (multi-agent ≈15× chat) [S3][S5] **[Verified]**.

### 7. Governance & security layer (cross-cutting)

Full treatment in [governance_security_and_risk.md](governance_security_and_risk.md). Architectural placement:

- **Guardrail checkpoints at four points**: user input, tool call, tool response, final output [S5] **[Verified]**; layered mechanisms (classifiers, rules/regex, moderation, PII filters, output validation) [S1] **[Verified]**.
- **Least privilege** per agent and per tool; guardrails complement — never replace — authN/authZ [S1][S5] **[Verified]**.
- **Audit log**: every run traceable to agent version, prompt version, input, model, and reviewer decision (repo principle #9, extended).
- **Environment separation** (dev/test/prod) and approved-data-source lists are Level-100 prerequisites — required *before* broad adoption, not at maturity [S6] **[Extracted]**.

## Human approval points

| # | Point | Trigger | Mechanism |
|---|---|---|---|
| 1 | Intake confirmation | Ambiguous/missing critical inputs | Clarifying questions; generation blocked until answered or logged as assumptions [S23] |
| 2 | Output review (always) | Every generated brief/ADR | Named human role (Solution Architect) approves, edits, or rejects; nothing auto-publishes to systems of record [S9][S12] |
| 3 | High-risk tool action | Any medium/high-risk tool call (writes: Jira ticket creation, page publishing) | Pause + explicit human confirmation [S1] **[Verified]** |
| 4 | Failure-threshold escalation | Validator loop exceeds iteration cap, low judge score, or repeated schema failures | Route to human with trace attached [S1][S5] **[Verified]** |
| 5 | Change approval | Prompt/schema/tool changes | PR review + regression evals green ([development_best_practices.md](development_best_practices.md)) |

The two **mandatory** HITL triggers per OpenAI — exceeded failure thresholds and high-risk/irreversible actions [S1] **[Verified]** — are points 3 and 4; points 1, 2, and 5 reflect the read-mostly, document-producing nature of this agent **[Inference]**.

## What this architecture deliberately postpones

- Orchestrator + multi-agent workflows (until a documented trigger fires) [S1][S5].
- Cross-agent shared long-term memory; anything beyond per-request retrieval + session state.
- Autonomous write actions into systems of record (Jira/Confluence writes stay draft-or-approved-only).
- Fine-tuning: 70% of production agents run prompting on off-the-shelf models [S9] **[Verified]**.
- Parallel subagents — fragile in 2025-era practice; single-threaded with context compression preferred [S16] **[Extracted]**.
