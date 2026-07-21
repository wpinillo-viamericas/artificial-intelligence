# 14 — Risks, Open Questions, and Decisions

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — index and evidence-tier
> legend there. Citations `[S#]` resolve in [references.md](references.md).
>
> Consolidates the risk register, the maturity frame, the unresolved decisions, the honestly-labeled
> open questions, and the **handoff to the roadmap phase**. Security controls are detailed in
> [08](08-security-privacy-and-compliance.md); governance in
> [10](10-observability-and-governance.md).

## Adoption maturity model (where we are, what each level requires)

**[Recommendation]** — synthesis of Microsoft's model [S6] and AAGMM [S13], adapted to this org.
**Do not skip levels; gate each promotion on the prior level's exit criteria** [S1][S2][S5].

| Level | Name | Capabilities | Governance required |
|---|---|---|---|
| 0 | Manual | Humans + ad-hoc LLM chat | Usage policy; approved-tools list |
| 1 | Prompt templates | Shared, versioned prompts | Prompts in git; owner per template |
| 2 | Role copilots | Advisory, no tools; human executes | Output-review norms; citations; basic logging |
| 3 | **Tool-enabled agents ← SA Agent MVP target** | One schema-first agent per validated use case; retrieval + typed tools; bounded workflow; 100% human review | Microsoft Level-100 (owners, approved sources, env separation, logging, incident procedures) + eval gate in CI + registries started |
| 4 | Multi-agent workflows | Orchestrator-worker; delegation contracts; pipelined handoffs | AAGMM Level-3 (formal policies, central catalog, RBAC, HITL); delegation-contract schemas; per-agent cost metering |
| 5 | Governed ecosystem | Portfolio; tiered controls; cross-initiative memory | Microsoft 300–500 (classification, zoned envs, CoE/AI-Council, continuous compliance) |

## Risk register

Likelihood (L) / Severity (S): Low / Med / High. Residual = after the listed controls.
**Part A — identification:**

| # | Risk | Scenario | L | S | Business impact |
|---|---|---|---|---|---|
| R1 | Wrong/incomplete architecture accepted (blind trust) | Architect approves a fluent-but-wrong brief; design degrades downstream [S12] | M | H | Rework, delivery delay, bad architecture in production |
| R2 | Hallucinated org facts | Agent invents a system/owner/platform not in ground truth | M | H | Misleading briefs; loss of trust |
| R3 | Data leakage via retrieval | Retrieval surfaces catalog/Confluence content the requester can't access [S5] | L-M | H | PII/KYC exposure; compliance breach |
| R4 | Weak evals → silent quality drift | Prompt/model change ships without regression evidence [S12] | H (if unmitigated) | H | Undetected degradation; erodes adoption |
| R5 | Inconsistent outputs break handoffs | Schema drift or free-text output stalls downstream roles | M | M | Handoff friction; manual rework |
| R6 | Premature multi-agent complexity | Orchestration adopted with no trigger; 41–86.7% failure, ~15× cost [S10][S3] | M | H | Wasted spend; fragile system |
| R7 | Agent sprawl at scale | Duplicate/shadow/orphaned agents; permission creep [S13] | M (grows) | M-H | Maintenance load; security gaps |
| R8 | Framework/vendor lock-in | Heavy framework chosen; stack churns in months [S17] | M | M | Costly migration |
| R9 | Over-automation / rubber-stamping | Reviewer fatigue → approvals without scrutiny | M | M | Wrong outputs slip through |
| R10 | Prompt-governance failure | Untested prompt change, no rollback [S8] | M | M | Regression; no recovery path |
| R11 | Session/state leakage across users | Weak isolation leaks one user's data to another [S21] | L | H | PII exposure; compliance breach |
| R12 | Cost runaway | Runaway loops or vector-store idle floor [S3][S87] | M | L-M | Budget overrun |
| R13 | **Prompt injection (direct & indirect)** | Malicious instructions in an ingested ticket/page/KYC upload hijack the agent [S53][S54] | M | H | Tool abuse, exfiltration, bad output |
| R14 | **Retrieval/data poisoning** | Poisoned corpus/KB entries steer recommendations [S53] | L-M | H | Systematically wrong, trusted output |
| R15 | **Excessive tool agency / scope creep** | Over-broad tool scopes or a write path enabled without gating [S54] | L-M | H | Unauthorized writes to systems of record |
| R16 | **Regulatory / model-risk gap** | A higher-tier agent (Risk/CS) ships without model-risk review [S61] | L | H | Regulatory finding; enforcement risk |
| R17 | **Supply-chain (unofficial MCP/tool)** | Community MCP server or dependency introduces malicious behavior [S53 LLM03] | L | H | Compromise; data exposure |

**Part B — response:**

| # | Preventive control | Detective control | Owner | Residual | Decision required |
|---|---|---|---|---|---|
| R1 | Mandatory architect approval; options+tradeoffs; required assumptions/open-questions; source traceability | Approval-rate & edit-distance metrics; spot audits | Solution Architect | Low-Med | D6 (eval bar) |
| R2 | Inject `shared/context` only; `unknown`/`not_provided` enums; never-fabricate rule; retrieval grounding | Hallucinated-fact eval case = 0 tolerance | Solution Architect | Low | D3 (corpus) |
| R3 | Identity-trimmed / ACL-filtered retrieval [S39]; approved-source allowlist; PII filters | Access-audit review; retrieval logs | Platform owner | Low | D3, D2 |
| R4 | 20–50 golden cases before launch; CI regression; judge+human QA | pass^k tracking; regression alerts | Eval owner | Med | D6 |
| R5 | Schema-enforced output; deterministic validation; consistency linter | Schema-invalid rate = 0 | Platform owner | Low | — |
| R6 | Written trigger criteria (below); orchestrator-worker only; delegation contracts | Trigger-metric monitoring | Head of D&A | Low | **D8** |
| R7 | Registry-required-to-run; one-role-one-agent; tiered governance | Quarterly registry review | Head of D&A | Med | D7 |
| R8 | Thin custom core; prompts/schemas/evals as repo data | Periodic stack-cost review | Platform owner | Low-Med | D1 |
| R9 | Augment-not-automate posture; low pilot volume; rubric review | Edit-distance trend | Solution Architect | Med | D6 |
| R10 | PR-gated prompt changes; prompt registry with rollback; eval gate | Change audit in git | Platform owner | Low | D7 |
| R11 | Persistent isolated state store; isolation tests before prod | Cross-user leakage tests | Platform owner | Low | D1 |
| R12 | Per-run token metering; budget alerts; scale-to-zero store; model downshift | Cost-per-task dashboard | Platform owner | Low | **D10** |
| R13 | Treat retrieved content as untrusted; input guardrail; no auto-act on ingested content; least-privilege tools | Injection red-team set; anomaly alerts | Platform owner + Security | Med | D2, security review |
| R14 | Approved-source allowlist; source-authority ranking; ingestion review | Poisoning red-team; source-diff monitoring | Data owner | Low-Med | D3 |
| R15 | Read-only default; narrow scopes; propose-then-commit; risk-rated tools | Tool-call audit; scope review | Platform owner | Low | D9, D7 |
| R16 | Higher-tier agents pass model-risk review before build; always-human-approval list [08] | Compliance sign-off gate | Head of D&A + Compliance | Low | new decision (see below) |
| R17 | Vet/avoid unofficial MCP servers; pin & review deps; official vendor servers only | Dependency scanning | Platform owner | Low | D9 |

## Multi-agent expansion triggers (resolving D8, to ratify)

Write these down *in advance*; adopt an orchestrator only when one fires [S1][S5] **[Verified]**:

- **T1 — instruction-following failure:** the single agent's instructions become unmanageable or it
  drifts across roles despite prompt tuning.
- **T2 — tool overload/confusion:** tool-selection accuracy degrades from too many overlapping tools
  (overload is driven by similarity, not count [S1]).
- **T3 — parallelizable work exceeds one context window:** genuinely independent subtasks that don't
  fit sequentially (and justify ~15× token cost [S3]).
- **T4 — context exhaustion:** a single request's necessary context no longer fits with acceptable
  quality.

## Open questions (labeled — nothing invented)

These cannot be confirmed from the repo or public research; the roadmap phase must resolve them.
None are answered here.

| Ref | Open question | Type |
|---|---|---|
| Q1 | Current cloud & data architecture actually in use (vs the brief's candidate list) | [Assumption] |
| Q2 | Existing IAM / identity patterns (SSO, directory, how requester identity reaches the agent) | [Open decision] |
| Q3 | Data residency / region requirements | [Open decision] |
| Q4 | Approved AI model providers & enterprise terms (D2 — Bedrock? Anthropic direct? ZDR?) | [Open decision] |
| Q5 | Internal security standards & data-classification levels (operating-model TODOs) | [Open decision] |
| Q6 | Jira / Confluence / GitHub permission models & whether MCP servers are sanctioned | [Open decision] |
| Q7 | Production deployment process & CI available to the Data & AI area | [Open decision] |
| Q8 | Exact Data & AI headcount, seniority, and who can hold platform/governance duties | [Assumption] |
| Q9 | Ownership of agent development & governance (confirm Head of D&A as accountable owner) | [Open decision] |
| Q10 | Budget & usage constraints (per-run/per-month ceilings — D10) | [Open decision] |
| Q11 | Source-of-truth / authoritative sources for channel attribution & master data | [Open decision] |
| Q12 | Whether higher-tier agents (Risk, Customer-Service) require formal model-risk review, and who owns it | [Open decision] |

## Decisions required before implementation (D1–D10 + additions)

| # | Decision | Default leaning | Doc |
|---|---|---|---|
| D1 | Runtime & hosting; dev/test/prod separation | Thin Python runner in a container; env separation day one; consider AgentCore Runtime | [05](05-platform-and-framework-comparison.md) |
| D2 | Model-provider terms (agreement, retention, region, ZDR) | Resolve before real data enters the agent | [08](08-security-privacy-and-compliance.md) |
| D3 | MVP retrieval corpus + identity-trimming enforcement | Narrowest set that still grounds briefs; ACL-filtered | [06](06-knowledge-and-retrieval-architecture.md) |
| D4 | Intake channel + output surface | Lightweight form/chat + markdown in repo/Confluence draft | [04](04-solutions-architecture-agent.md) |
| D5 | Output standards (ADR/arc42/diagram format) | MADR-simple; arc42 section mapping; Mermaid → Structurizr later | [04](04-solutions-architecture-agent.md) |
| D6 | Eval ownership, golden-case curation, pilot pass bar | SA owns cases; Head of D&A sets bar; pass^k target | [09](09-evaluation-and-testing.md) |
| D7 | Governance minimum at launch (registries + tiering now vs later) | **Now** — Level-100 is cheap and pays immediately | [10](10-observability-and-governance.md) |
| D8 | Multi-agent trigger criteria (T1–T4) | Ratify the triggers above; draft thresholds during pilot | [02](02-agentic-ai-operating-model.md) |
| D9 | Integration transport (MCP vs native) | MCP-first where official server exists; native otherwise | [07](07-data-and-integration-architecture.md) |
| D10 | Budget guardrails (token/cost ceilings, alerts) | Set before pilot; track cost-per-successful-task | [11](11-cost-and-scalability.md) |
| D11 (new) | Model-risk / compliance gate for higher-tier agents | Require review before any Risk/CS/PII-touching agent | [08](08-security-privacy-and-compliance.md) |
| D12 (new) | Observability stack (AWS-native vs +LLM-native tool) | CloudWatch GenAI + Langfuse/Phoenix via OTel | [10](10-observability-and-governance.md) |

---

# Inputs Required for the Agentic AI Implementation Roadmap

*This is the handoff to the next (roadmap) phase. It summarizes what the research establishes and
what the roadmap must still decide. **Do not treat the open items as resolved.***

### What the research establishes (build on these)

1. **Direction:** one **schema-first Solutions Architecture Agent** built as a **bounded workflow**
   (`intake → clarify → retrieve → generate → validate → render → human review`) with **mandatory
   human review**, on a **custom-lightweight core** over the Claude API, expanding only on written
   triggers [S1][S2][S9][S11].
2. **Architecture:** the **layered platform** in [03](03-target-architecture.md); centralize any
   capability ≥2 agents use; keep prompts/schemas/tools/evals as framework-independent repo data.
3. **Platform path:** custom-light MVP → optional **AgentCore Runtime** host (managed state/identity/
   observability, GovCloud) and **LangGraph** only if operational/orchestration burden materializes;
   **MCP-first** integrations [S26][S30][S32].
4. **Retrieval:** managed RAG, **hybrid + rerank**, **ACL-filtered via Verified Permissions**,
   recency + source-authority ranking, inline citations; **skip GraphRAG initially** [S35][S38][S39].
5. **Security:** four-checkpoint guardrails, identity-trimmed retrieval, agent-as-NHI with JIT creds,
   Bedrock/Anthropic data-handling terms, and a firm **always-human-approval list** — the SA Agent
   publishes and approves nothing [S1][S5][S57][S62].
6. **Evaluation:** 20–50 golden cases now; deterministic→judge→human graders; **pass^k**;
   Bedrock Evaluations + Ragas + Langfuse/Phoenix; phased rollout [S4][S63][S69].
7. **Governance:** Microsoft **Level-100** at launch → **Level-300/AAGMM-3** before agent #2;
   central registry (seeded); minimum artifact set; risk-tiered controls [S6][S13].
8. **Portfolio evidence:** Data Engineering + Documentation + Intake/Triage are the strongest early
   follow-ons; Data Reconciliation / DQ / Tracking-QA runtimes should be **deterministic, not
   agents**; Risk/Customer-Service agents are high-value but gated by sensitivity & model risk.
9. **Measurement from inception:** every agent has business KPIs, technical SLIs, eval criteria, and
   retirement conditions ([09](09-evaluation-and-testing.md), [12](12-development-lifecycle.md)).

### What the roadmap must still resolve (unresolved decisions & open questions)

- **Decisions D1–D12** above — especially D2 (model terms), D3 (corpus + trimming), D7 (governance
  now), D8 (triggers), D10 (budget), D11 (model-risk gate).
- **Open questions Q1–Q12** — cloud/data reality, IAM & identity flow, data residency, permission
  models, deployment/CI, headcount/ownership, source-of-truth, model-risk ownership. **Confirm with
  the business; do not assume.**
- **Sample-data collection** (D6 inputs) before build: 10–20 real requests, 3–5 exemplar briefs,
  standards corpus, 2–3 planted-gap requests.
- **Workstream organization** (from the prior prerequisites work): WS1 Foundation platform → WS2 SA
  Agent build → WS4 Pilot & hardening; WS3 Evaluation/observability and WS5 Governance/security gate
  the pilot; WS6 Expansion readiness starts only after architect sign-off.
- **The final implementation sequence, dates, and per-agent backlog** — explicitly *not* set here;
  they are the roadmap phase's output, and must begin with the Solutions Architecture Agent.
