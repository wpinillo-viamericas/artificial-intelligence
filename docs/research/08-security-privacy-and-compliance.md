# 08 — Security, Privacy, and Compliance

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — index and evidence-tier
> legend there. Citations `[S#]` resolve in [references.md](references.md).
>
> Controls for an agentic system in a **US money-transfer / remittance (regulated financial
> services)** environment handling PII/KYC. Governance *process* and artifacts are in
> [10](10-observability-and-governance.md); the risk register is in
> [14](14-risks-open-questions-and-decisions.md).
>
> **Compliance caveat.** Regulatory statements below are factual and high-level; **confirm scope and
> applicability with Compliance/Legal** — do not treat this document as legal advice.

## Framing

Automated, code-embedded governance **accelerates** delivery rather than slowing it — clear,
automated guardrails move pilots to production in weeks instead of quarters [S8] **[Extracted]**.
Security here is infrastructure, not inspection. The SA Agent's profile is favorable (internal,
read-mostly, human-reviewed documents — the lowest-risk deployment class [S9]), but customer,
transaction, KYC, compliance, and risk data are **sensitive by default** (research principle #9), so
the controls below apply from day one and bite harder when write-tools arrive.

## Threat model (what we defend against)

Grounded in the **OWASP Top 10 for LLM Applications (2025)** [S53] and OWASP's **Agentic AI Threats
& Mitigations (Feb 2025)** + **Top 10 for Agentic Applications (Dec 2025)** [S54], with adversary
techniques from **MITRE ATLAS** [S56]:

| Threat | How it manifests here | Primary controls |
|---|---|---|
| **Prompt injection** (direct & indirect) — OWASP LLM01 | Malicious instructions hidden in an ingested ticket, Confluence page, or KYC upload hijack the agent | Treat all retrieved content as untrusted data, not instructions; input guardrail; never auto-act on externally-ingested content [S53][S54] |
| **Retrieval / data poisoning** — LLM04 | Poisoned or false entries in the corpus/KB steer recommendations | Approved-source allowlist; source-authority ranking [S40]; ingestion review; supply-chain checks |
| **Sensitive-info disclosure** — LLM02 | Brief or retrieval surfaces PII/KYC or another user's data | Identity-trimmed retrieval [S5][S39]; PII filters; output validation |
| **Improper output handling** — LLM05 | Unvalidated output written to a system of record | Schema-enforced output; deterministic validation; approval-gated writes |
| **Excessive agency** — LLM06 | Over-broad tools/permissions or autonomy without approval | Least-privilege scoped tools; risk-rated tools; mandatory HITL on writes [S1] |
| **Tool misuse / exfiltration** — Agentic | Injected instruction drives a scoped tool (DB query, API) to leak/move data | Read-only default; narrow scopes; egress control; audit every tool call [S54][S50] |
| **Identity & privilege abuse** — Agentic | Long-lived/broad agent credentials abused | Agent as governed non-human identity; time-bounded/JIT creds [S62] |
| **Cross-user / cross-tenant exposure** — LLM02/LLM08 | Shared memory/embeddings or weak session isolation leak one customer's PII to another | Per-user session isolation [S21]; ACL-tagged chunks [S39]; isolation tests before prod |
| **System-prompt leakage** — LLM07 | Prompt/tool internals exposed | Don't put secrets in prompts; output guardrail |
| **Unbounded consumption** — LLM10 | Cost/DoS via runaway loops | Iteration caps; token budgets/quotas [S3] ([11](11-cost-and-scalability.md)) |

## Guardrails and access control

- **Guardrails at four checkpoints** — user input, tool call, tool response, final output — layered
  (LLM classifiers, rules/regex/blocklists, moderation, **PII filters**, output validation), as a
  **complement to, never a substitute for, authN/authZ** [S1][S5] **[Verified]**.
- **Least privilege** per agent and per tool; permissions reviewed on change (counters permission
  creep) [S5][S13].
- **Identity-aware security trimming:** the agent must never return data the *requesting user*
  cannot access, enforced across every knowledge store [S5] **[Verified]** — realized via ACL-tagged
  retrieval / Verified Permissions [S39][S36].
- **Agent identity:** treat each agent as a governed **non-human identity** with a dedicated
  identity, a narrow tool allowlist, and **time-bounded / just-in-time credentials** that expire with
  the task; tokens carry minimal scope (e.g., "read-only on the approved corpus") [S62] **[Extracted]**.
- **RBAC/ABAC:** requesters submit; the mapped role reviews/approves; platform owner administers
  registries; Head of D&A approves agents and risk-tier changes; attribute-based filters (dept,
  sensitivity) drive retrieval ACLs [S36].
- **Secrets management:** API keys and integration credentials in a secrets manager, per
  environment, never in repo/prompts.
- **Encryption:** in transit and at rest for corpus, state, logs, and outputs (GLBA Safeguards
  expectation [S59]).
- **Session/state isolation:** explicit persistent storage with validated per-user isolation —
  in-memory loss and cross-user leakage are documented production failures [S21].

## Model-provider data handling

- **Amazon Bedrock:** does not store prompts/outputs after the request, does not share data with
  model providers, and does not use inputs/outputs to train models; each provider runs in an isolated
  deployment account [S57] **[Extracted]**.
- **Anthropic (commercial terms, incl. API/Bedrock/Vertex):** does not train on customer
  inputs/outputs without permission; standard API log retention reduced to 7 days (2025-09-14);
  **Zero Data Retention (ZDR)** and HIPAA-ready arrangements available on approval [S58] **[Extracted]**.
- **[Open decision D2]:** confirm the enterprise agreement, retention, region, and whether ZDR is
  required *before* any real request data enters the agent.
- **No architecture/PII content to uncontrolled external services** — render diagrams on self-hosted
  infrastructure, not public renderers [S24].

## Financial-services compliance context **[Extracted — high-level; confirm applicability]**

- **GLBA / FTC Safeguards Rule:** written information security program with a Qualified Individual,
  encryption in transit/at rest, MFA, access controls with periodic least-privilege review, and
  testing; breach notification for events affecting 500+ consumers effective **2024-05-13** [S59].
- **BSA/AML & KYC:** MSBs/money transmitters register with FinCEN, hold state licenses, run AML
  programs, perform CIP/CDD, screen OFAC, and file SARs/CTRs; Travel Rule and funds-transfer
  recordkeeping apply [S60].
- **Model risk (SR 11-7):** the Fed/OCC framework governs model development, validation, and
  governance; institutions apply it by analogy to AI/LLM systems [S61]. *(A reported 2026 formal
  extension to AI/agentic systems is **unverified** against a primary letter — confirm.)*
- **PCI-DSS** where card/PAN data is in scope; **SOC 2** as the common vendor/control attestation.

**Implication [Inference]:** expect the regulated-enterprise pattern — approval/review controls as
*hard requirements* (42% of regulated firms are adding them vs 16% unregulated [S17]). The SA Agent
never touches the KYC/AML decision or money-movement path; agents that would must clear the
always-human-approval list below and likely a model-risk review.

## Actions that must ALWAYS require human approval

Non-delegable regardless of agent confidence, for any Data & AI agent in this environment [S1][S54]:

- Executing/releasing a **money transfer, payout, refund, or hold-release**, or changing payment
  limits/beneficiaries.
- **KYC/AML decisions:** approving/clearing onboarding; overriding a sanctions/OFAC or watchlist hit;
  closing/dismissing a case.
- **Filing or suppressing a SAR/CTR** or any regulatory report.
- **Disclosing or exporting PII/KYC externally**, or bulk export/deletion of customer records.
- **Account actions:** freeze/unfreeze; credential/MFA reset; changing entitlements.
- Modifying AML rules, thresholds, risk scores, or **the agent's own permissions/tools/system prompt**.
- **Any write to a system of record** (Jira/Confluence/Salesforce) — propose-then-commit [S51].
- Any action the agent flags as low-confidence or that was triggered by externally-ingested
  (untrusted) content.

For the SA Agent specifically, the binding rule is simpler: **it publishes nothing and approves
nothing** — the Solution Architect signs off every output.

## Auditability, retention, incident response, red-teaming

- **Immutable, tamper-evident audit trail:** every run answers *who asked, what did the agent see,
  what did it produce, who approved it, under which versions* — logging every tool call, permission
  granted, data accessed, and outcome [S5][S62]. See [10](10-observability-and-governance.md).
- **Retention & data minimization** aligned to GLBA/BSA recordkeeping [S59][S60]; define retention
  for prompts, traces, outputs, and corpus copies (**[Open decision]**).
- **Incident response** for agent failures + a user-feedback channel are Level-100 prerequisites
  [S6].
- **Red-teaming / adversarial testing** mapped to OWASP LLM Top 10 and MITRE ATLAS (prompt
  injection, exfiltration, tool abuse, poisoning) before and continuously after deployment
  [S56][S53]; feeds the adversarial test set in [09](09-evaluation-and-testing.md).

## Decision matrix — deployment models (security lens)

| Model | Data exposure | Control | Fit |
|---|---|---|---|
| **AWS-hosted, Bedrock/AgentCore, VPC/PrivateLink, GovCloud-eligible** | Lowest (data stays in tenant; no provider training) [S57] | ● (IAM, inherited compliance) | ✅ **recommended** for regulated FS [S26][S28] |
| Anthropic API direct, with ZDR + enterprise terms | Low (ZDR) [S58] | ◐ (you build hardening) | ✅ MVP-viable with D2 resolved |
| Third-party SaaS agent platform (data leaves tenant) | Higher | ◐ | ⚠️ only with DPA + compliance review |
| Public/consumer LLM tools for real data | High | ○ | ❌ prohibited for PII/KYC |

**Recommended:** keep inference and data inside the AWS tenant (Bedrock/AgentCore) or use the
Anthropic API under ZDR/enterprise terms; never route PII/KYC through consumer tools.
