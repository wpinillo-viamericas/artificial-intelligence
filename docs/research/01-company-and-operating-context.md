# 01 — Company and Operating Context

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — see it for the full
> index and the evidence-tier legend. External citations `[S#]` resolve in
> [references.md](references.md); internal ground truth is cited by repo path.
>
> **Evidence caveat for this document.** The *company* facts below are drawn from the project
> brief that commissioned this research, not from verified corporate systems of record. Treat
> business-model, product, and platform specifics as **[Assumption]** to confirm with the
> business, unless they are grounded in a repo file (then **[Extracted — internal]**). The
> *Data & AI area* facts are grounded in
> [`shared/context/org_structure.md`](../../shared/context/org_structure.md) and
> [`shared/context/data_ai_operating_model.md`](../../shared/context/data_ai_operating_model.md),
> which are themselves marked as a starting template with TODOs.

## Why this document exists

Every agent in this program is meant to reason from a single, shared model of the business and
the Data & AI operating model (repo design principle #6: *shared ground truth*). This document
consolidates that context for the research library and, critically, **separates what is
confirmed from what is assumed** so that later agent designs never silently treat an assumption
as a fact. It is the grounding layer for docs [02](02-agentic-ai-operating-model.md) (operating
model), [04](04-solutions-architecture-agent.md) (the first agent), and
[13](13-future-agent-portfolio.md) (future agents).

## 1. Business model and channels **[Assumption — confirm with business]**

Viamericas operates a financial-services and payments ecosystem centered on money transfers and
related transactional products. The model is primarily **transaction-based**, with economics
that likely combine transaction fees, foreign-exchange spread, service fees, agency commissions,
and product-specific revenue.

Distribution spans four channel families that the data must reconcile against one another:

| Channel family | Examples | Data & AI implication |
|---|---|---|
| Physical agency / retail network | Agencies, agents, retail-assisted transactions | Agency & agent master data; commission attribution; hierarchy (agency → district → region) |
| Digital | ViaLink, ViaOne | Web/app event tracking (GA4/GTM); funnel & conversion measurement |
| Assisted digital | WhatsApp AI bot → ViaLink handoff; Salesforce-assisted commercial workflows | Session logs, bot-to-web attribution, handoff continuity |
| Internal operational platforms | Zaswind, transaction systems, compliance/KYC workflows, payout | Systems of record; source-of-truth reconciliation |

**Why this matters for agents [Inference]:** the recurring hard problems in this business —
*channel attribution without duplicates*, *funnel/abandonment measurement*, and
*cross-system reconciliation* — are data-quality and measurement problems first. Several are
better solved by deterministic pipelines and governed taxonomies than by an LLM agent (research
principle #2, and the gating test in [02](02-agentic-ai-operating-model.md)). The agent program
should accelerate the *design, documentation, and review* of those solutions, not replace the
deterministic machinery that produces the numbers.

## 2. Products and platform ecosystem **[Assumption — confirm]**

International & domestic transfers/remittances; bill payments; mobile top-ups; loyalty and
promotions; sender/beneficiary management; enrollment & onboarding; KYC / identity-document
collection; compliance-review workflows; payout processing; and the digital surfaces **ViaLink**,
**ViaOne**, **Zaswind**, and the **WhatsApp-assisted** transaction journey. WhatsApp is
described as a growing assisted-digital channel where an AI bot helps customers initiate or
complete a transaction before they continue in ViaLink.

**Sensitivity note:** customer, transaction, KYC, compliance, and risk data are **sensitive by
default** (research principle #9). This classification drives the security posture in
[08](08-security-privacy-and-compliance.md) and the always-human-approval list there.

## 3. Customers and internal stakeholders **[Extracted — internal, partial]**

- **External:** senders, beneficiaries, retail customers migrating to digital, net-new digital
  customers, WhatsApp-assisted customers.
- **Commercial:** retail agencies/agents, Business Development Executives, district & regional
  sales managers, sales leadership.
- **Internal functions:** Digital Channels, Product, Marketing, Operations, Customer Service,
  Compliance, Risk, Architecture, Software Development, and **Data & Artificial Intelligence**.

The Data & AI area serves the internal functions as its primary "customers," which aligns with
the verified finding that ~92.5% of production agents serve internal human users and that
internal-first deployment is the standard risk posture [S9] **[Verified]**.

## 4. Strategic priorities and how the Data & AI program maps to them

The eight business priorities from the brief, mapped to where agentic/deterministic capability
plausibly helps **[Inference]**:

| # | Priority | Primary Data & AI lever | Agent vs deterministic |
|---|---|---|---|
| 1 | Scale digital & assisted channels (WhatsApp, ViaLink) | Measurement + architecture for new journeys | Architecture agent (design); deterministic tracking |
| 2 | Improve customer & agency adoption | Funnel/adoption analytics, incremental-growth attribution | Mostly deterministic analytics; agent assists design/QA |
| 3 | Improve conversion / reduce fallout | Friction, abandonment, cancellation, recovery analysis | Deterministic analytics; agent for hypothesis framing |
| 4 | Improve measurement & attribution (no duplicates/overlap) | Channel-attribution taxonomy & identity resolution | **Deterministic** — do not put an LLM on the hot path |
| 5 | Scalable, governed reporting | Standard funnels, KPIs, taxonomies, ownership, SoT | Governance + BI agents (design/QA); deterministic delivery |
| 6 | Data quality & operational reliability | Duplicate/missing/inconsistent-record analysis, reconciliation | **Deterministic** checks; agent for rule *generation* & root-cause narrative |
| 7 | Introduce AI-enabled operations | Analytics, architecture, risk, support, KRM, data-quality copilots | Agent program (this initiative) |
| 8 | Maintain regulatory/security/privacy controls | PII/KYC protection, auditability, FS governance | Cross-cutting; see [08](08-security-privacy-and-compliance.md) |

The consistent pattern: **agents help humans design, document, QA, and reason; deterministic
software produces the governed numbers.** This is the throughline of the whole library.

## 5. The Data & AI area — organization **[Extracted — internal]**

Grounded in [`org_structure.md`](../../shared/context/org_structure.md). The area is led by a
**Head of Data & Analytics**; all specialized roles roll up to that leader.

```
Head of Data & Analytics
├── Solution Architect              (first agent target)
│   └── Data Engineer
├── Value Assurance Specialist
│   └── Data Assurance Specialist
├── Data Visualization Specialist
├── Digital Analytics Specialist
├── Data Governance Specialist
│   └── Data Governance Analysts    (x3, temporary contract)
├── Data Scientist
└── Project Manager
```

Canonical role keys (kept in sync with `shared/schemas/enums.json` → `downstream_role`):
`data_engineering`, `data_assurance`, `value_assurance`, `data_visualization`,
`digital_analytics`, `data_governance`, `data_science`, `project_management`, `head_of_data`.
The **three Data Governance Analyst positions are temporary contracts** — a detail that matters
for [13](13-future-agent-portfolio.md), because their high-volume, structured cataloging work is
the area's best candidate for partial automation-with-review.

### Area capabilities (four pillars)

1. **Digital Analytics & Measurement** — GA4, GTM, event taxonomy, parameter/schema design,
   funnel measurement, channel attribution, conversion/abandonment analysis, tracking QA,
   measurement governance, and **preventing PII/KYC exposure in analytics platforms**.
2. **Visual Analytics & BI** — Amazon QuickSight/QuickSuite, Tableau, executive & operational
   dashboards, Salesforce-embedded analytics, role-based reporting, agency/region/district/sales
   hierarchy analysis, access management.
3. **Data Management & Data Quality** — source validation, cross-system reconciliation,
   source-of-truth identification, Data Lake/BI availability, dataset/field documentation,
   duplicate/missing/inconsistent analysis, root-cause investigation, access management, KPI
   governance.
4. **Advanced Analytics & AI** — WhatsApp AI-assisted journeys and log analysis, session
   summarization, customer-service context generation, Amazon Bedrock agents, risk-analysis
   agents, GenAI for analytics, and **agentic AI for the area's own operating processes** (this
   initiative).

## 6. The Data & AI operating model — how work flows **[Extracted — internal]**

Grounded in [`data_ai_operating_model.md`](../../shared/context/data_ai_operating_model.md).
Requests arrive from business sponsors, product, compliance, or leadership as one of six types
(dashboard/reporting, digital-analytics/tracking, data-pipeline/integration,
data-quality/governance, AI/ML use case, mixed/platform), and are normalized by the Solution
Architect's intake before any design begins.

Target delivery flow:

```
Intake → Solution Architecture Brief → Downstream handoffs → Build → Assurance → Release → Value check
```

The Solution Architect reasons across seven solution-component families (ingestion/sources, data
models, analytics platforms, integrations, governance, scalability/reliability, delivery
dependencies) and produces a brief plus scoped handoffs. This flow is exactly why the
**Solutions Architecture Agent is the correct first agent**: it sits at the intake bottleneck and
produces the artifacts every downstream role consumes (see [02](02-agentic-ai-operating-model.md)
and [04](04-solutions-architecture-agent.md)).

### "What good looks like" for a brief (the operating model's Definition of Done)

One-sentence objective a sponsor would agree with; named business + data/technical owner (or a
flagged gap); every data source named with an owner or explicitly `unknown`; measurable success
metrics; specific, categorized, owned risks; scoped handoffs; explicit assumptions and open
questions. These are already re-encoded as the MCP validator's consistency warnings
([`shared/mcp/validation.py`](../../shared/mcp/validation.py)) and become the SA Agent's eval
rubric in [09](09-evaluation-and-testing.md).

## 7. Current technical environment **[Assumption — verify; not confirmed]**

The brief lists a candidate environment; **none of it is confirmed as the preferred agentic-AI
stack.** It is recorded here so later docs can reason about reuse, and every item is an open
question in [14](14-risks-open-questions-and-decisions.md):

- **Cloud / AI:** AWS, Amazon Bedrock, Amazon QuickSight/QuickSuite, Data Lake & BI platforms.
- **Analytics / product:** Google Analytics 4, Google Tag Manager, Salesforce, Tableau.
- **Delivery / knowledge:** Jira, Confluence, GitHub, Claude Code / AI-assisted development.
- **Languages / runtime:** Python, SQL, React apps & micro-frontends, serverless services.
- **Data / domain:** transactional databases, WhatsApp session logs, KYC/compliance data,
  agency & customer master data, Fiserv and other payment-related sources.

The operating-model template's platform and standards sections are still **TODO placeholders**
(classification levels, PII handling, compliance regimes, naming conventions are unconfirmed).
Until confirmed, **agents must treat platform choices as assumptions to flag, never facts** —
this is both an internal rule and the direct mitigation for the hallucinated-org-facts risk (R2,
[14](14-risks-open-questions-and-decisions.md)).

## Key open questions raised here (carried to doc 14)

- Confirmed data-classification levels, PII/KYC handling policy, and in-scope compliance regimes
  (BSA/AML, GLBA, PCI, state money-transmitter, SOC 2). **[Open decision]**
- The authoritative source of truth for channel attribution and agency/customer master data.
  **[Open decision]**
- Which listed platforms are actually the target agentic-AI stack vs. incidental. **[Open decision]**
- The real Data & AI headcount, seniority, and who can own agent platform/governance duties.
  **[Open decision]**
