# Governance, Security, and Risk

> Document 6 of 9 — see [research_overview.md](research_overview.md) for the index; citations `[S#]` in [research_sources.md](research_sources.md).
>
> Framing fact: automated, code-embedded governance **accelerates** delivery rather than slowing it — clear, automated guardrails move pilots to production in weeks instead of quarters [S8] **[Extracted]**. Governance here is designed as infrastructure, not inspection.

## Security requirements

| Requirement | Detail | Evidence |
|---|---|---|
| Least privilege per agent and per tool | Agents and orchestrators get the minimum scopes their registered tools need; permissions reviewed on change (counters permission creep [S13]) | [S5] **[Verified]** |
| Identity-aware security trimming | The agent must never return data the *requesting user* cannot access — enforced in every agent, across every knowledge store (catalog, Confluence, etc.) | [S5] **[Verified]** |
| Guardrails at four checkpoints | Content/safety checks at user input, tool call, tool response, final output | [S5] **[Verified]** |
| Layered guardrail mechanisms | LLM classifiers, rules-based filters (regex/blocklists), moderation, PII filters, output validation — layered, and a **complement to, never a substitute for**, authN/authZ | [S1] **[Verified]** |
| Per-tool risk ratings | Every registered tool rated low/medium/high from read-vs-write, reversibility, permissions, impact; medium/high triggers pause or human escalation | [S1] **[Verified]** |
| Systems-level containment | Reliability and security come from design constraints — read-only modes, sandboxed verification, wrapper APIs, RBAC mirroring user permissions — not from model quality | [S9] **[Verified]** |
| Secrets management | API keys and integration credentials in a secrets manager, never in repo/prompts; per-environment secrets | **[Recommendation]** (standard practice; specific patterns not covered by surviving claims) |
| Session/state isolation | Explicit persistent storage with validated per-user isolation — in-memory session loss and cross-user leakage are documented production failures | [S21] **[Extracted]** |

The SA Agent's risk profile is favorable — internal, read-mostly, producing human-reviewed documents — the lowest-risk deployment class (52% of production agents serve internal employees; internal-first is the deliberate risk-mitigation strategy) [S9] **[Verified]**. Controls above still apply from day one; they just bite harder when write-tools arrive **[Inference]**.

## Privacy and compliance

- **PII filters** in the guardrail stack [S1] **[Verified]**; intake may contain customer/business-sensitive detail — classify and handle brief content per existing data-classification policy **[Recommendation]**.
- **No architecture content to uncontrolled external services** — e.g., render diagrams on self-hosted infrastructure, not public renderers (kroki.io caveat) [S24] **[Extracted]**. Model API data-handling terms are an **[Open decision]** input (enterprise agreement, retention, region).
- **Risk-tiered compliance controls**: low-risk internal use → fast-track approval and minimal logging; moderate → standard guardrails and audit trails; high-risk (PII/financial/regulated) → enhanced logging, HITL, isolated environments [S8] **[Extracted]**. Viamericas operates in a regulated (remittance/financial) domain: expect the regulated-enterprise pattern — approval/review controls as hard requirements (42% of regulated enterprises adding them vs 16% unregulated) [S17] **[Extracted]** **[Inference]**.

## Access control model

**[Recommendation]**, from [S1][S5][S8]: users authenticate to the intake surface; the agent runs with a service identity whose retrieval is trimmed by the *requesting user's* permissions; tools carry their own scoped credentials from the registry entry; write-capable tools (later) additionally require the named human approver. Role-based: requesters submit; the mapped role (Solution Architect) reviews/approves; the platform owner administers registries; the Head of Data & Analytics approves new agents and risk-tier changes.

## Auditability and traceability

Every run must answer: *who asked, what did the agent see, what did it produce, who approved it, under which versions?*

- Trace of every prompt, response, tool call in a structured timeline [S18] **[Extracted]**; audit trails are an explicit enterprise requirement [S5] **[Verified]**.
- Output metadata: agent version, prompt version, model ID, input reference, timestamps (existing principle #9), plus reviewer identity/decision **[Recommendation]**.
- Registries as the accountability spine: **agent registry** (owner, purpose, risk tier, evaluation status), **tool registry** (scopes, data access, approval authority), **prompt registry** (versioning, lineage, rollback) [S8] **[Extracted]**; a central agent catalog is part of minimum viable governance [S13] **[Extracted]**.
- Source traceability in outputs: briefs/ADRs should reference which retrieved documents grounded which claims — semantic traceability between artifacts is a named research gap and a control against unsourced recommendations [S12] **[Extracted]**.

## Human-in-the-loop controls

The two mandatory triggers [S1] **[Verified]**: (1) **failure thresholds exceeded** — validator cap hit, repeated schema failures, low judge scores → escalate with trace; (2) **high-risk or irreversible actions** — any medium/high-risk tool call pauses for explicit approval.

Additional posture for this agent: 100% human review of outputs during pilot (74% of production agents rely primarily on human evaluation [S9] **[Verified]**); checkpoints and stopping conditions rather than open-ended autonomy [S2] **[Verified]**; approval-gated writes to systems of record indefinitely (existing principle #10). Guard against reviewer fatigue: keep pilot volume low, use rubrics, track draft-vs-approved edit distance **[Inference]**.

## Prompt, schema, and version governance

- Prompts, schemas, configs, and eval cases are **versioned repo artifacts** changed via PR review; breaking output-schema changes bump major versions (existing principle #9).
- Prompt registry semantics: lineage, rollback policy, change control — "version and govern prompts like code" [S8] **[Extracted]**.
- No prompt/schema change merges without green golden-case regression ([development_best_practices.md](development_best_practices.md)) [S4].
- Policy-as-code: centralized guardrail/policy logic packaged as an installable versioned library → org-wide consistency, versioned updates, git audit trail [S8] **[Extracted]**.
- Model version pinning per agent config, with planned (not silent) upgrades validated against evals; prototype with the most capable model, then downshift where accuracy holds [S1] **[Extracted]**.

## Governance maturity and tiering

Two convergent maturity ladders anchor staging:

- **Microsoft (levels 100→500)**: from no AI-specific governance to predictive, continuously adaptive governance. **Level-100 prerequisites before broad adoption:** who can create/publish agents; approved data sources; access controls; environment separation; an accountable owner per agent; basic logging; feedback channels; incident-response procedures [S6] **[Extracted]**. Level 300 adds explicit classification by purpose/criticality/autonomy, a central registry, audit logging, zoned environments, and CoE/AI-Council oversight [S6].
- **AAGMM (levels 1→5, 12 domains)**: **Level 3 — formal policies, central agent catalog, RBAC, HITL — is the minimum viable governance standard**; reactive incident-driven governance provides almost no security benefit over none [S13] **[Extracted, simulation-based]**.
- **Tier controls by agent risk/criticality — uniform controls are an anti-pattern** (over-restricting low-risk agents drives shadow AI; under-governing critical ones creates gaps) [S6] **[Extracted]**.

**[Recommendation]** Target: Microsoft Level-100 controls at MVP launch, Level-300/AAGMM-Level-3 equivalents (registry, classification, formal approval workflow) before the second agent ships. Council function: given team size, the Head of Data & Analytics initially acts as the AI-Council/CoE with real decision rights — a council without a mandate drives governance bypass [S6] **[Extracted]**.

## Risk register

| # | Risk | L | S | Mitigations | Owner (proposed) |
|---|---|---|---|---|---|
| R1 | Wrong/incomplete architecture recommendation accepted (blind trust → architectural degradation [S12]) | M | H | Mandatory architect approval; options+tradeoffs format; required assumptions/open-questions; source traceability | Solution Architect |
| R2 | Hallucinated org facts (systems, owners, platforms) | M | H | Injected shared ground truth only; `unknown`/`not_provided` enums; never-fabricate rule; retrieval grounding | Solution Architect |
| R3 | Data leakage via retrieval or external services | L–M | H | Security trimming [S5]; approved-source allowlist; PII filters [S1]; self-hosted rendering [S24] | Platform owner |
| R4 | Weak evals → silent quality drift (the field's most-cited gap [S12]) | H (if unmitigated) | H | 20–50 golden cases before launch [S4]; CI regression; judge+human layered QA [S9] | Eval owner |
| R5 | Inconsistent output formats breaking handoffs | M | M | Schema-enforced outputs [S25]; deterministic validation; consistency linter [S23] | Platform owner |
| R6 | Premature multi-agent complexity (41–86.7% failure rates [S10]; 15× cost [S3]) | M | H | Written trigger criteria; orchestrator-worker only; delegation contracts [S3] | Head of D&A |
| R7 | Agent sprawl at scale (duplication, shadow/orphaned agents, permission creep [S13]) | M (grows) | M→H | Registry-required-to-run; one-role-one-agent; tiered governance [S6]; periodic registry review | Head of D&A |
| R8 | Framework/vendor lock-in amid quarterly stack churn [S17] | M | M | Thin custom core; prompts/schemas/evals as framework-independent repo data | Platform owner |
| R9 | Over-automation / reviewer rubber-stamping | M | M | Augment-not-automate posture [S9]; low pilot volume; rubric review; edit-distance tracking | Solution Architect |
| R10 | Prompt-governance failure (untested changes, no rollback) | M | M | PR-gated prompt changes; prompt registry with rollback [S8]; eval gate | Platform owner |
| R11 | Session/state leakage across users | L | H | Persistent isolated state store; isolation tests before prod [S21] | Platform owner |
| R12 | Cost runaway (agents ≈4× chat tokens; multi-agent ≈15× [S3]) | M | L–M | Per-run token metering; budget alerts; model downshifting where evals hold [S1] | Platform owner |

L = likelihood, S = severity. Owners are proposals pending the ownership decision in [implementation_prerequisites.md](implementation_prerequisites.md).
