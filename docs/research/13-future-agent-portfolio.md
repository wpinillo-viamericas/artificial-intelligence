# 13 — Future Agent Portfolio

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — index and evidence-tier
> legend there. Citations `[S#]` resolve in [references.md](references.md).
>
> Candidate agents *after* the Solutions Architecture Agent, with evidence to support
> prioritization. **This does not set the final implementation sequence** — that is the next
> (roadmap) phase's job. Role→agent mapping rationale is in
> [02](02-agentic-ai-operating-model.md); the operating model in
> [01](01-company-and-operating-context.md).

## How to read this

Two hard rules from the evidence gate every candidate:

1. **Re-pass the gating test with a concrete workflow before build** — nuanced judgment,
   non-codifiable rules, unstructured input; otherwise **build deterministic automation, not an
   agent** [S1] **[Verified]**. Several candidates below are *mostly deterministic* and are flagged
   as such — the agentic value is in *generating rules/docs*, not running checks at runtime.
2. **Augment, don't automate, judgment roles** — 92.5% of production agents serve humans as final
   verifiers [S9]; 85% of GenAI-for-architecture systems are assistive [S12].

Scoring (relative, **[Inference]** grounded in [S1][S9][S12] and the org in
[`org_structure.md`](../../shared/context/org_structure.md)): **Business value**, **Technical
complexity**, **Data sensitivity**, **Human oversight** on Low/Med/High; **Early/Later** suitability
is a readiness signal, not a commitment.

## Portfolio scoring matrix

| Candidate agent | Maps to role | Gating-test fit | Biz value | Tech complexity | Data sensitivity | Key integrations | Oversight | Depends on | Early/Later |
|---|---|---|---|---|---|---|---|---|---|
| **Solutions Architecture** (shipped first) | Solution Architect | Strong | High | Med | Low-Med | Corpus, Jira/Confluence/GitHub (read) | High | — | **Now** |
| **Data Engineering** | Data Engineer | Strong (pipeline/contract design); weak for mechanical codegen | High | Med | Med | GitHub, catalog, corpus | High | SA handoff contract | Early |
| **Documentation** | cross-role | Strong (unstructured→structured) | Med-High | Low | Low | Confluence/GitHub (read/draft) | Med | Corpus | Early |
| **Project Intake & Triage** | PM / Head of D&A | Strong (classify/route ambiguous requests) | Med-High | Low-Med | Low | Jira, intake channel | Med | SA Agent | Early |
| **Data Catalog / Data Governance (analyst tasks)** | Governance Specialist + Analysts | Mixed — policy = judgment; cataloging = rule-bound | High (temp-contract workload) | Med | Med-High | Catalog, corpus, Confluence | High | Catalog stack (D3) | Early-Mid |
| **Digital Analytics** | Digital Analytics Specialist | Moderate-strong (event taxonomy from unstructured reqs) | High | Med | Med (PII in analytics!) | GA4, GTM, corpus | High | Measurement standards | Mid |
| **Measurement Strategy** | Digital Analytics / Value Assurance | Strong (funnel/KPI/attribution design) | High | Med | Med | GA4, corpus | High | Analytics taxonomy | Mid |
| **BI Developer** | Data Visualization Specialist | Moderate (dashboard spec/KPI mapping) | Med-High | Med | Med | QuickSight/Tableau, corpus | High | Viz standards | Mid |
| **SQL Analysis** | Data Scientist / Analytics | Moderate (NL→SQL over governed models) | Med-High | Med-High | **High** (DB access) | SQL engines (read-only) | High | Governed data models, ACLs | Mid |
| **Experimentation** | Data Scientist | Strong (experiment/hypothesis design) | Med | Med | Med | Corpus, analytics | High | Data Science practice | Mid-Later |
| **Risk Analytics** | Risk / Data Scientist | Strong framing; **outputs advisory only** | High | High | **High** (fraud/KYC) | Transactional data (read), corpus | **Very High** | Model-risk review (SR 11-7) [S61] | Later |
| **Customer-Service Context** | Customer Service (business) | Strong (WhatsApp session summarization/context) | High | Med | **High** (customer PII) | WhatsApp logs, CRM | **Very High** | PII controls [08] | Later |
| **Tracking QA** | Digital Analytics | **Mostly deterministic** — agent *generates* checks | Med | Low-Med | Med | GA4/GTM, CI | Med | Tracking specs | Rule-gen only |
| **Data Quality** | Data Assurance | **Mostly deterministic** — agent *generates* rules; checks run as code | Med-High | Low-Med | Med | Data Lake, CI | Med | DQ framework | Rule-gen only |
| **Data Reconciliation** | Data Assurance / Engineering | **Deterministic** — do NOT put an LLM on the reconciliation hot path | High (biz priority #6) | Low | Med-High | Source systems, Data Lake | Low | Source-of-truth defs | Deterministic |
| **Dashboard QA** | Data Visualization | **Mostly deterministic** — agent generates QA checklists | Low-Med | Low | Low | BI tools | Low | Viz standards | Rule-gen only |
| **Value Assurance** | Value Assurance Specialist | Moderate (value/metric alignment review) | Med | Low-Med | Low | Corpus, briefs | Med | SA briefs | Later |

## What the matrix says (evidence for prioritization — not a sequence)

- **Highest early leverage after SA:** **Data Engineering** (first consumer of the SA handoff —
  proves the handoff contract end-to-end [S3]) and low-complexity, low-sensitivity augmenters
  (**Documentation**, **Project Intake & Triage**) that reuse the SA Agent's substrate directly.
- **Best "partial automation with review" candidate:** the **Data Governance Analyst** workload
  (cataloging, metadata cleanup, stewardship) — high-volume, structured, and currently on temporary
  contracts, matching the constrained-and-measurable profile of successful first deployments [S17]
  ([01](01-company-and-operating-context.md)). Governance *policy* work stays human judgment.
- **High value but gated by sensitivity/model-risk:** **Risk Analytics** and **Customer-Service
  Context** touch fraud/KYC/PII — high value but **Very High** oversight, an always-human-approval
  surface ([08](08-security-privacy-and-compliance.md)), and likely a model-risk review [S61]. These
  are *later*, not first, regardless of value.
- **Do not build as agents (build as deterministic software):** **Data Reconciliation** and the
  runtime of **Data Quality / Tracking QA / Dashboard QA**. The agentic value is *generating* the
  rules/checklists once; the checks themselves run as code — putting an LLM on the data-verification
  hot path is an explicit anti-pattern [S1]. This directly serves business priorities #4 and #6
  ([01](01-company-and-operating-context.md)) *better* without an LLM.
- **Dependency backbone:** most analytics/BI/SQL agents depend on **confirmed governed data models,
  standards, and ACLs** (decisions D3/D5 and the source-of-truth work) — so the governance/catalog
  and standards foundation unlocks a whole cluster. This is *evidence for*, not a decision on,
  sequencing.

## Cross-cutting requirements for every new agent

Each must, before build: re-pass the gating test [S1]; get a registry entry with owner + risk tier
[S13]; reuse shared services (retrieval, tools, evals, observability, governance —
[02](02-agentic-ai-operating-model.md)); define golden cases and SLIs [S4]; and honor the
one-role-one-agent boundary with schema-typed handoffs. Adding agents without meaningful
specialization is an explicit anti-pattern [S5].

## Explicitly out of scope for this phase

No final sequence, no dates, no per-agent roadmap. The next phase consumes this matrix plus the
decisions and risks in [14](14-risks-open-questions-and-decisions.md) to build the implementation
roadmap, beginning (as already established) with the Solutions Architecture Agent.
