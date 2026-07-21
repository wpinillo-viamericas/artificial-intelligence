# Agentic AI Implementation Roadmap — Data & AI Area

> **Status:** Draft for approval. **Owner:** Head of Data & Analytics (accountable). **Author:** Data & AI systems architecture.
> **Supersedes:** [`docs/roadmap.md`](../roadmap.md) as the operative plan. The older document's *sequencing rationale* (SA → DE → Governance/Assurance → Delivery → PM/Orchestration) is preserved and re-expressed here as trigger-gated expansion; its phase list is retained downstream of the SA pilot.
> **Grounded in:** the research package in [`docs/research/agentic-ai-data-area/`](../research/agentic-ai-data-area/) — start with [research_overview.md](../research/agentic-ai-data-area/research_overview.md) and [implementation_prerequisites.md](../research/agentic-ai-data-area/implementation_prerequisites.md). Citations `[S#]` resolve in [research_sources.md](../research/agentic-ai-data-area/research_sources.md).

---

## 0. Operating constraints (non-negotiable, from the verified evidence)

These bound every phase below. They are restated up front because they are the difference between the evidence-backed path and the failure modes it documents.

1. **Single agent first.** Build and prove one role-scoped agent — the Solutions Architecture (SA) Agent — before any second agent. Multi-agent expansion happens only when a **written trigger** fires (§6) [S1][S2][S5][S9] **[Verified]**.
2. **Workflow-shaped internals, not a free-running agent.** The SA Agent is a bounded, predefined pipeline: `intake → clarify (ask-first) → retrieve → generate → validate (≤3 loops) → render → human review` [S2][S11] **[Verified]**.
3. **100% human review during pilot.** Every brief/ADR/diagram is reviewed, edited, or rejected by the human Solution Architect. Nothing auto-publishes to a system of record [S9][S12] **[Verified]**.
4. **No production agent code is written until this roadmap is approved.** Approval of this document is the entry gate to WS1/WS2 build work. Until then, work is limited to schema/spec drafting and decision ratification.
5. **Deterministic work stays deterministic.** Schema checks, enum conformance, cross-artifact consistency linting run as code, never as LLM calls [S1][S22] **[Verified]**.
6. **Do not skip maturity levels.** Each promotion is gated on the prior level's exit criteria [S1][S6][S13] **[Verified/Extracted]**.

**Where we are on the maturity ladder** (from [implementation_prerequisites.md](../research/agentic-ai-data-area/implementation_prerequisites.md)): the repo sits at **Level 2 → 3**. The scaffold (schema-first agent, one role per agent, handoff packets, HITL-by-default) is Level-2-complete. This roadmap drives the promotion to **Level 3 (Tool-enabled agents)** and defines — but defers — the gate to Level 4 (multi-agent).

---

## 1. Decision register — D1–D10 resolved

Each open decision from [implementation_prerequisites.md](../research/agentic-ai-data-area/implementation_prerequisites.md) is resolved with a **recommended default** and a **named owner**. Decisions marked *Ratify* need a yes/no at roadmap approval; decisions marked *Assign* are delegated to an owner to close by the stated milestone.

| # | Decision | Resolution (recommended default) | Owner | Close by | Status |
|---|---|---|---|---|---|
| **D1** | Runtime & hosting; env separation | **Thin Python runner** (`shared/utils/agent_runner`) calling the Anthropic Claude API directly, packaged as a **container**; **dev/test/prod separated from day one** with per-env secrets. No orchestration framework in MVP [S2][S9]. | Platform owner | WS1 start | Ratify |
| **D2** | Model-provider terms (enterprise agreement, retention, region) | **Secure an Anthropic enterprise agreement with zero data-retention and an approved region before any real request data enters the agent.** Until signed, only synthetic/anonymized inputs are permitted. **Hard gate before pilot (Phase 2).** | Head of D&A + Procurement/Legal | Before Phase 2 | Assign — **blocking** |
| **D3** | MVP retrieval corpus + identity trimming | **Narrowest grounding that still works:** `shared/context/*` org files + a curated **platform/standards corpus** + 3–5 exemplar briefs/ADRs, held **locally and indexed**. No external stores (Confluence/catalog) in MVP. Identity-aware trimming is **designed into the retrieval interface now** but only enforced when external stores arrive in Phase 3 [S5][S11]. | Solution Architect (curates) + Platform owner (interface) | WS1/WS2 | Ratify |
| **D4** | Intake channel + output surface | **In:** one channel — a lightweight structured **form / CLI** producing JSON that matches `input.schema.json` (free-text `request_text` + optional context). **Out:** markdown + JSON **drafts written to a repo `drafts/` folder**, routed to the Solution Architect. No Slack/Jira/Confluence intake in MVP [S17]. | Solution Architect + Platform owner | WS2 | Ratify |
| **D5** | Output standards | **ADR = MADR (simple variant); brief mapped to arc42 headings where natural** (quality goals precede design); **diagrams = C4 context + container as Mermaid** (Structurizr DSL later). Render diagrams **self-hosted/local, never public renderers** (kroki caveat) [S22][S23][S24]. | Solution Architect | WS2 | Ratify |
| **D6** | Evaluation ownership + pilot pass bar | **Solution Architect owns and curates the golden cases and is the calibration reviewer; Platform owner owns eval infrastructure; Head of D&A sets and signs the pass bar.** Recommended default bars in §3 (Gate G2/G3) — architect sign-off is the primary criterion [S3][S4][S9]. | Head of D&A (bar) + Solution Architect (cases) | WS3 | Ratify |
| **D7** | Governance minimum at launch | **Adopt agent/tool/prompt registries + risk-tiering NOW, at MVP** (not deferred to the second agent). The Level-100 set is cheap and pays immediately [S6][S8]. Registry entry is a precondition for running. | Platform owner + Head of D&A | WS1 | Ratify |
| **D8** | Multi-agent trigger criteria | **Written in advance in §6.** Draft thresholds are set now; calibrated against observed pilot data before any expansion decision [S1][S5]. | Head of D&A | §6 (now); recalibrate end of Phase 2 | Resolved (draft) |
| **D9** | Integration transport (MCP vs native APIs) | **Deferred to a time-boxed spike in Phase 3**, not MVP. Default leaning: **MCP servers** for registry-friendly reuse of Jira/Confluence/catalog, decided by spike outcome. Not blocking the MVP [S1] **[Inference — not verified]**. | Platform owner | Phase 3 | Assign — non-blocking |
| **D10** | Budget guardrails | **Set before pilot:** per-run token ceiling (**default 60k output tokens/run**, hard-fail above), per-request cost log, **monthly cap with alerts at 50/80/100%**. Model pinned in `config.yaml`; downshift where evals hold [S1][S3]. | Platform owner | Before Phase 2 | Ratify |

**Cross-cutting ownership** (from [agent_operating_model.md](../research/agentic-ai-data-area/agent_operating_model.md)): the **Head of Data & Analytics** acts as the AI-Council/CoE with real decision rights (approves new agents, risk-tier changes, high-risk tools, the pilot pass bar). The **Platform owner** role is a de-facto duty held **jointly by the Data Engineer + Solution Architect** initially — not a new hire. The **Solution Architect** is the accountable owner of SA Agent outputs and golden cases.

---

## 2. Workstreams and dependency map

Delivery is organized around the six workstreams from the research. WS1/WS3/WS5 run largely in parallel with early WS2; WS4 (pilot) cannot start until WS3 and WS5 gate it; WS6 cannot start until WS4's architect sign-off.

```
WS1 Foundation platform  ─────────────────────────────►  WS2 SA Agent build  ──►  WS4 Pilot & hardening
    (runner, schema enforcement,        (intake→clarify→retrieve→          (real requests, 100%
     registries, secrets, envs)          generate→validate→render→review)   review, tuning)
                                                     ▲   ▲                        ▲
WS3 Evaluation & observability ──────────────────────┘   │  ── gates ──────────────┤
    (golden cases, rubric, judge, tracing)               │                         │
                                                          │                         │
WS5 Governance & security ────────────────────────────────┘  ── gates ────────────┘
    (guardrails, trimming, audit, HITL procedures, Level-100)
                                                                                     │
WS6 Expansion readiness  ◄───────────────────── starts only after WS4 exit ─────────┘
    (handoff-contract validation with DE role, trigger monitoring, second-agent gating)
```

**Hard dependencies** (from [implementation_prerequisites.md](../research/agentic-ai-data-area/implementation_prerequisites.md)):
- WS2 **cannot pilot** without WS3's golden cases and WS5's Level-100 controls.
- WS6 **cannot start** until the architect sign-off produced in WS4.
- The **shared substrate (WS1/WS3/WS5) is stood up before the second agent, not after** [S1][S4][S8][S13].

| WS | Scope | Depends on | Primary owner |
|---|---|---|---|
| **WS1 Foundation platform** | Runner, prompt composer, schema validator, registries (agent/tool/prompt), secrets, dev/test/prod envs, container | — | Platform owner |
| **WS2 SA Agent build** | Ask-first intake, retrieval, generation, validator loop, rendering, new schema fragments (ADR/diagram/clarification) | WS1 | Solution Architect + Platform owner |
| **WS3 Evaluation & observability** | Golden-case suite (≥20), rubric, LLM-judge pre-screen, trace capture, token/cost metering, failure taxonomy | WS1 (light) | Platform owner (infra) + Solution Architect (cases) |
| **WS4 Pilot & hardening** | Real requests through the agent, 100% human review, prompt/schema tuning, health-metric collection | WS2, WS3, WS5, D2, D10 | Solution Architect |
| **WS5 Governance & security** | Guardrail checkpoints, identity-trimming interface, audit log, HITL procedures, Level-100 checklist, risk register operationalized | WS1 | Platform owner + Head of D&A |
| **WS6 Expansion readiness** | Handoff-contract validation (DE role, human-relayed), trigger monitoring, second-agent gating test | WS4 exit | Head of D&A |

---

## 3. Phases, deliverables, and evaluation gates

Phases replace the near-term of `docs/roadmap.md`. Each has explicit **entry** and **exit** criteria; exits are enforced by the **evaluation gates** defined at the end of this section. Phase 0 is largely complete; the plan's active work is Phases 1–4.

### Evaluation gates (referenced by every phase)

| Gate | Name | Check | Enforced |
|---|---|---|---|
| **G0** | Schema validity | All examples + golden outputs validate against `output.schema.json`; enums resolve; no extra fields [S25] | CI, every PR |
| **G1** | Deterministic checks | Enum conformance + **cross-artifact consistency linter** (IDs/names/risks referenced consistently across brief↔ADR↔diagram) pass [S23] | CI, every PR |
| **G2** | Golden-case + judge | **≥20 golden cases green**; single rubric-scoring LLM judge (0.0–1.0 + pass/fail) **≥ 0.80 mean** and calibrated to the architect's scores; **pass^k consistency ≥ target** (default pass^3 ≥ 0.70; final value set under D6) [S3][S4] | CI on prompt/schema/config/model change |
| **G3** | Architect sign-off + Level-100 | Solution Architect signs that briefs are **useful and safe to hand downstream** (primary criterion [S9]); **Level-100 checklist complete** (§5); zero schema-invalid outputs | Release gate (human) |
| **G4** | Pilot health | Approval rate, draft-vs-approved **edit distance**, open-questions-per-brief, downstream rework, cost/brief all trending acceptably; no unresolved high-severity incident | Continuous during Phase 2 |

Nondeterminism rule: integration tests use rubric/judge scoring, **never exact-match** on generated prose [S5].

---

### Phase 0 — Foundation scaffold *(this milestone — largely complete)*

**Goal:** clean modular repo + first-agent v0.1 scaffold.

- [x] Repo structure (`/agents`, `/shared`, `/docs`, `/tests`).
- [x] Shared context (org structure + operating model); design principles.
- [x] SA Agent v0.1: prompt, config, input/output schemas, worked example, test cases.
- [ ] **Roadmap approval (this document).** ← entry gate for all build work.

**Exit:** this roadmap and D1/D3/D4/D5/D6/D7/D10 are ratified; D2 assigned; a request can conceptually run through the agent to a schema-valid brief.

---

### Phase 1 — Platform hardening + SA Agent MVP build (WS1 + WS2 + WS3 + WS5 in parallel)

**Goal:** a reliable, observable, governed SA Agent that produces schema-valid briefs with ADRs and a C4 diagram, exercised against a golden-case suite — **but not yet on real request data**.

**Entry:** Phase 0 exit met (roadmap approved).

**Deliverables** (detailed backlog in §4):
- **WS1:** thin Python runner (`agent_runner`), `prompt_composer`, `schema_validator`; agent/tool/prompt **registries** seeded; secrets manager; dev/test/prod envs; container image.
- **WS2:** new schema fragments (`adr`, `diagram`, `clarification`) in `/shared/schemas`; ask-first intake stage; local retrieval over the D3 corpus; generation of brief + MADR ADRs + Mermaid C4 diagram; **validator loop (≤3 iterations)**; markdown/JSON renderer.
- **WS3:** golden-case suite (≥20) from historical requests; rubric + LLM-judge; **trace capture** (every prompt/response/tool call); token/cost metering; MAST-style failure tagging.
- **WS5:** guardrail checkpoints at the four points (input/tool-call/tool-response/output); audit log; identity-trimming **interface** stubbed; HITL procedures documented; Level-100 checklist started.

**Evaluation gates:** G0 + G1 wired into CI and green; G2 achievable on synthetic golden cases.

**Exit:** the agent runs end-to-end in the **test** environment on the golden-case suite; G0, G1, G2 pass in CI; trace + audit records are produced for every run; all three registries have the SA Agent + its tools + its prompt entered with owner and risk tier.

---

### Phase 2 — Pilot & hardening (WS4)

**Goal:** prove the briefs are **useful and safe on real requests**, under 100% human review.

**Entry:** Phase 1 exit met; **D2 signed** (enterprise model terms); D10 budget guardrails live; Level-100 checklist complete (§5).

**Deliverables:**
- 10–20 **real historical requests** collected (anonymized where needed) spanning request types; run through the agent.
- **100% human review** by the Solution Architect (review rubric = judge rubric); edits captured to measure edit distance.
- Prompt/schema tuning via PR, each change gated by G2 (no merge without green evals).
- Health-metric dashboard (G4 metrics); incident log; feedback channel.

**Evaluation gates:** G3 (architect sign-off + Level-100) and G4 (pilot health) are the phase's exit gates.

**Exit:** **Solution Architect signs off** that briefs are useful and safe to hand downstream; G4 metrics trending well over a sustained set of real requests; no open high-severity risk from the register (§ risk linkage). This sign-off is the **only** entry key to WS6.

---

### Phase 3 — SA Agent Phase-2 capabilities *(post-sign-off, still single-agent)*

**Goal:** widen the single agent's reach without adding a second agent — earn integration and write capabilities behind approval gates.

**Entry:** Phase 2 exit (architect sign-off) met.

**Deliverables** (each new tool passes the tool-registry + risk-rating process, not ad-hoc wiring):
- **D9 spike:** time-boxed evaluation of MCP servers vs native APIs for Jira/Confluence/catalog; decision recorded as a platform ADR.
- **Read integrations:** Confluence/catalog **read**, identity-trimmed [S5]; Jira read for intake context. (Integration transport per D9 outcome.)
- **Approval-gated writes:** Confluence draft publishing, Jira backlog creation as **medium/high-risk registered tools** → HITL pause + explicit approval on every call [S1].
- **Corpus growth:** larger retrieval corpus incl. catalog metadata; Structurizr DSL diagrams + consistency linting in CI.
- **Judge pre-screen routing:** LLM-judge routes low-scoring drafts to humans first (still never judge-only) [S9].

**Evaluation gates:** G0–G2 continuously; every write tool adds an HITL approval point (Approval Point 3) and an audit entry; identity-trimming now **enforced** (not just stubbed) with isolation tests before prod [S5][S21].

**Exit:** integrations live behind their risk tiers with green regressions; write actions demonstrably require and log human approval; corpus expansion has not regressed G2.

---

### Phase 4 — Expansion readiness & second-agent gating (WS6)

**Goal:** decide, on evidence, whether to promote to Level 4 (multi-agent) — and if so, do it correctly.

**Entry:** Phase 2 sign-off met; trigger monitoring (§6) has run through the pilot and Phase 3.

**Deliverables:**
- **Handoff-contract validation with the DE role:** stand up the **Data Engineering Agent** whose *input schema = the SA brief's `data_engineering` handoff packet*, proving the contract end-to-end with a **human relay** (no orchestrator, no agent-to-agent calls) [agent_operating_model.md].
- **Trigger evaluation:** measure the §6 metrics; produce a written go/no-go on multi-agent expansion.
- **Governance uplift** *(only if expanding):* AAGMM Level-3 / Microsoft Level-300 equivalents — formal approval workflow, central classification, RBAC, per-agent cost metering, delegation-contract schemas evolved from handoff packets [S6][S13].

**Evaluation gate:** expansion proceeds **only if a §6 trigger has fired and is documented**; otherwise the org stays single-agent and continues hardening. Orchestration, when justified, is **manager/orchestrator-worker with explicit delegation contracts — never peer handoffs** [S1][S2][S5][S7].

**Exit:** either (a) a written, evidence-backed decision to remain single-agent, or (b) a triggered, governed plan to add the second agent with delegation contracts and Level-3 governance in place.

> Beyond Phase 4, the sequencing from [`docs/roadmap.md`](../roadmap.md) holds: **DE → Governance/Assurance → Delivery (Analytics/Viz/Science) → PM + orchestration**, each phase-gated by written exit criteria. That order is preserved and not repeated here.

---

## 4. SA Agent MVP backlog

Concrete, buildable work items for Phases 1–2. Grouped by epic; each item names the artifact it touches. This is the definition of "done" for the MVP.

### Epic A — Schema additions (`/shared/schemas`)

The output brief schema (`agents/solution_architect/schemas/output.schema.json`) and shared enums (`shared/schemas/enums.json`) are kept as-is and **extended** with three new cross-agent fragments. Schemas are defined once (Pydantic), JSON Schema generated, enforced via Claude tool-based structured output, validated on return [S25].

- **A1 — `adr` fragment** (`shared/schemas/adr.schema.json`): MADR-simple shape — `id`, `title`, `status` (`proposed|accepted|superseded`), `context`, `decision`, `consequences`, `options_considered[]` (name/pros/cons), `supersedes` (ref), `timestamp`. Rules: **one decision per record; immutable — amend or supersede, never edit** [S22]. Embedded in the brief and renderable standalone.
- **A2 — `diagram` fragment** (`shared/schemas/diagram.schema.json`): `type` (`c4_context|c4_container`), `format` (`mermaid|structurizr|plantuml`), `source` (diagram-as-code text), `title`. MVP emits Mermaid C4 context + container [S24].
- **A3 — `clarification` round-trip** (`shared/schemas/clarification.schema.json`): `questions_asked[]` (`id`, `text`, `directed_to`, `blocking`) ↔ `answers_received[]` (`question_id`, `answer`, `answered_by`) — makes the ask-first intake **auditable**.
- **A4 — Wire fragments into the brief:** add `adrs[]`, `diagrams[]`, and a `clarification` block to `output.schema.json`; add any new enums (e.g., `adr_status`) to `enums.json`. Breaking changes bump the agent major version [S8].
- **A5 — Source traceability:** add optional `sources[]` refs on claims/recommendations so briefs cite which retrieved doc grounded them (control against unsourced recommendations [S12]).

### Epic B — Ask-first intake flow

- **B1 — Clarify stage:** after intake, the agent generates **clarifying questions directed at named roles** (reuse `open_questions.directed_to`) and **blocks generation until answered or explicitly logged** as `assumptions`/`open_questions` — the arc42 "no generation until answered" rule [S23].
- **B2 — Intake surface (D4):** structured form/CLI producing `input.schema.json`-valid JSON; only `request_text` + requester identity required; everything else optional (missing info is the agent's job to surface, not a validation error).
- **B3 — Clarification persistence:** store the A3 round-trip against the run for audit; carry answers back into generation context.

### Epic C — Validator loop

- **C1 — Deterministic validators (code, not LLM):** schema validity, enum conformance, required-field presence, **cross-artifact consistency linter** (recommended option matches a listed option; handoff roles are valid enums; ADR/diagram/brief reference the same component IDs/names) [S23][S25].
- **C2 — LLM critique pass:** rubric-based self-critique against the review rubric (completeness, ownership honesty, no-fabrication, risk specificity, actionable handoffs).
- **C3 — Bounded refinement loop:** deterministic + critique feed a **≤3-iteration** maker-checker loop with explicit acceptance criteria; on cap-exceeded, **escalate to human with the trace attached** (Approval Point 4) [S5][S11].

### Epic D — Golden-case suite & evaluation

- **D1e — Seed ≥20 golden cases** from the 10–20 real historical requests + the existing 5 in `tests/cases.md`, spanning all `request_type` values and every downstream handoff role [S4].
- **D2e — Planted-gap cases:** 2–3 requests with **known planted gaps/risks** to test detection behavior (extend the existing Case-2 pattern).
- **D3e — Rubric + judge:** encode the `tests/cases.md` rubric as a **single rubric-scoring judge** (0.0–1.0 + pass/fail); calibrate against the architect's scores; grade **outcomes, not tool-call paths** [S3][S4].
- **D4e — pass^k harness:** repeat-run the same request to measure **pass^k** consistency (default pass^3 ≥ 0.70) — briefs are consistency-critical [S4].
- **D5e — CI wiring:** golden-case regression runs on any prompt/schema/config/model change; **no merge on regression** [S4].

### Epic E — Registries (`/registry`)

- **E1 — `agents.yaml`:** SA Agent entry — owner (Solution Architect), purpose, **risk tier (low–moderate)**, scopes, eval status, version. **Registry entry precedes running in prod — the anti-shadow-agent control** [S8][S13].
- **E2 — `tools.yaml`:** each tool (retrieval, diagram render) with scopes, data access, **risk rating (low/medium/high)**, approval authority. Keep tools **few and orthogonal** [S1].
- **E3 — prompt registry:** prompt/schema versions with lineage + rollback policy — "version and govern prompts like code" [S8].

### Epic F — Tracing & observability

- **F1 — Trace capture:** every prompt, response, and tool call in a structured timeline (Langfuse-class tool or structured logs) [S17][S18].
- **F2 — Run metadata / audit spine:** stamp agent version, prompt version, model ID, input ref, timestamps, and **reviewer identity + decision** on every output [governance_security_and_risk.md].
- **F3 — Token/cost metering:** per-run and per-agent; enforce D10 ceilings; alert on iteration-cap hits, schema-failure spikes, budget breaches [S1][S3].
- **F4 — Failure tagging:** MAST 14-mode/3-category taxonomy applied to failed runs so recurring classes surface [S10].

---

## 5. Governance Level-100 launch checklist (Phase 2 entry criteria)

Microsoft **Level-100** controls are the minimum before broad/real-data adoption and are the **launch criteria for the pilot** [S6]. All must be **complete** before Phase 2 begins. (Automated, code-embedded governance *accelerates* delivery — treat as infrastructure, not inspection [S8].)

- [ ] **Who can create/publish agents** is defined; publishing requires a registry entry (E1) and Head-of-D&A approval.
- [ ] **Approved data sources** allowlisted (D3 corpus); no source outside the allowlist is retrievable.
- [ ] **Access controls:** users authenticate to the intake surface; the agent runs under a service identity; retrieval trimmed by the requesting user's permissions (interface in place; enforced now for any external store).
- [ ] **Environment separation** (dev/test/prod) live with per-env secrets (D1).
- [ ] **Accountable owner per agent** recorded (Solution Architect for the SA Agent) (E1).
- [ ] **Basic logging** = trace capture + audit spine operational (F1/F2).
- [ ] **Feedback channel** for users of the agent exists.
- [ ] **Incident-response procedure** for agent failures documented, with named escalation paths.
- [ ] **HITL procedures** documented for the two mandatory triggers — failure thresholds and high-risk actions [S1].
- [ ] **Model-provider terms (D2)** signed; region/retention compliant.
- [ ] **Budget guardrails (D10)** live with alerting.
- [ ] **Registries (E1–E3)** populated for the SA Agent, its tools, and its prompt.

**Human approval points enforced from launch** (from [reference_architecture.md](../research/agentic-ai-data-area/reference_architecture.md)): (1) intake confirmation — generation blocked until questions answered or logged; (2) **output review — always**, Solution Architect approves/edits/rejects; (3) high-risk tool action — pause + confirm (activates in Phase 3); (4) failure-threshold escalation — validator cap / low judge score / repeated schema failures route to human with trace; (5) change approval — PR + green evals.

> Before the **second agent** ships, uplift to **AAGMM Level-3 / Microsoft Level-300**: formal approval workflow, central classification by criticality/autonomy, RBAC, per-agent cost metering, delegation-contract schemas [S6][S13]. This is Phase-4 scope, not launch scope.

---

## 6. Multi-agent expansion trigger criteria (written in advance — D8)

Per the unanimous vendor guidance, the org stays single-agent until **one or more of the following observable conditions is documented** [S1][S2][S5][S9]. These are drafted now and **recalibrated against real pilot data at the end of Phase 2**. Expansion is a decision by the Head of D&A on this evidence — not a default.

| Trigger | Observable condition (default threshold) | Data source |
|---|---|---|
| **T1 — Instruction-following failure** | The single agent cannot reliably follow its instructions for a distinct sub-job: **≥ 20% of runs** in a request class fail the rubric on the *same* failure mode across ≥ 2 prompt-tuning iterations, and the failures cluster in one role's depth (e.g., data-contract detail) | Golden-case + pilot judge scores; MAST failure tags (F4) |
| **T2 — Tool overload / confusion** | Tool selection errors driven by **similarity/overlap** (not raw count): the agent mis-selects among overlapping tools in **≥ 10% of tool-using runs**, and consolidating descriptions has not fixed it. (Count alone is not a trigger — some agents handle 15+ orthogonal tools fine.) [S1] | Trace analysis (F1); tool-call error rate |
| **T3 — Parallelizable work exceeding one context window** | A single initiative genuinely requires **independent** sub-tasks whose combined context exceeds the model's effective window, *and* the sub-tasks are breadth-first parallelizable (not sequential/shared-context) — the only shape where multi-agent's ~15× token cost pays [S3][S14] | Context-length metering; token/cost meter (F3) |
| **T4 — Sustained handoff-contract proof** | The Phase-4 DE handoff relay works reliably **and** demand exists for ≥ 2 downstream roles to consume SA output routinely — i.e., the *value* case for pipelining is demonstrated, not assumed | WS6 handoff-validation results |

**If a trigger fires, the expansion rules are fixed in advance:**
- Adopt **manager / orchestrator-worker with agents-as-tools** — **never peer handoffs** (documented failure modes: infinite loops, unpredictable routing) [S1][S2][S5][S7].
- Every delegation uses an **explicit task contract** (objective, output format, tool/source guidance, boundaries) evolved from today's handoff-packet schemas — vague delegation is the #1 multi-agent failure surface (41.8% of failures are specification defects) [S3][S10].
- Do **not** share mutable state between concurrent agents; prefer context compression over parallel context windows [S5][S16].
- Governance must reach **AAGMM Level-3 / MS Level-300** first (§5).

**If no trigger fires:** the correct action is to keep hardening the single agent and widening its reach (Phase 3), not to add agents. Premature multi-agent complexity carries 41–86.7% failure rates and ~15× cost [S10][S3].

---

## 7. Ownership summary (RACI-lite)

| Concern | Accountable | Responsible | Consulted |
|---|---|---|---|
| Roadmap approval; new-agent / risk-tier / high-risk-tool approval; pilot pass bar (D6) | **Head of D&A** | Head of D&A | Solution Architect, Platform owner |
| Model-provider terms (D2) | Head of D&A | Procurement/Legal | Platform owner |
| SA Agent outputs, prompt, golden cases (D3 curation, D5, D6 cases) | **Solution Architect** | Solution Architect | Domain experts |
| Runner, registries, CI, observability, secrets, envs (D1, D7, D10, WS1/WS3-infra/WS5) | **Platform owner** (DE + SA jointly) | Platform owner | Head of D&A |
| Eval infrastructure (D6 infra) | Platform owner | Platform owner | Solution Architect (task contribution) |
| Integration spike + transport (D9) | Platform owner | Platform owner | Head of D&A |
| Multi-agent expansion decision (D8/§6) | **Head of D&A** | Head of D&A | Solution Architect, Platform owner |

Risk owners for R1–R12 are as assigned in [governance_security_and_risk.md](../research/agentic-ai-data-area/governance_security_and_risk.md#risk-register) and are operationalized in WS5.

---

## 8. What this roadmap deliberately postpones

Restated so scope creep is visible (from [reference_architecture.md](../research/agentic-ai-data-area/reference_architecture.md)):

- Orchestrator + multi-agent workflows — until a §6 trigger fires.
- Cross-agent shared long-term / organizational memory — beyond per-request retrieval + session state.
- Autonomous writes into systems of record — Jira/Confluence writes stay draft-or-approved-only, **indefinitely**.
- Fine-tuning — prompting on off-the-shelf models is the norm [S9].
- Parallel subagents — single-threaded with context compression preferred [S16].
- Any framework adoption before the single agent has proven itself against evals [S2][S9].

---

*This document is the operative roadmap. Changes to it are PR-reviewed like any other governed artifact. Platform decisions (runner, registries, transport) are recorded as ADRs in this repo — the platform eats its own cooking.*
