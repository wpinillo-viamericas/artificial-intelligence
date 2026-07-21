# Data & AI Operating Model

> Shared ground truth about *how* the Data & AI area works: how requests flow, what artifacts exist, and what "good" looks like. Injected into agent prompts.
>
> This is a **starting template**. Replace bracketed placeholders and TODOs with the organization's real platforms, standards, and policies as they are confirmed.

## 1. How work enters the area

Requests arrive from business sponsors, product teams, compliance, or leadership. A request may be a business problem, an analytics need, a data need, or an AI/ML idea. Regardless of shape, it enters the Solution Architect's intake and is normalized into a structured request before any design begins.

Typical request types:
- **Dashboard / reporting** — decision-making outputs, KPIs.
- **Digital analytics / tracking** — event measurement, funnels, attribution.
- **Data pipeline / integration** — ingesting or moving data between systems.
- **Data quality / governance** — completeness, ownership, compliance initiatives.
- **AI / ML use case** — modeling, forecasting, experimentation.
- **Mixed / platform** — combinations of the above.

## 2. Delivery flow (target)

```
Intake → Solution Architecture Brief → Downstream handoffs → Build → Assurance → Release → Value check
```

1. **Intake & clarify** (Solution Architect): normalize the request, surface unknowns.
2. **Architecture brief** (Solution Architect): options, components, risks, dependencies.
3. **Handoffs**: scoped packets to Data Engineering, Governance, Analytics, Viz, Science as relevant.
4. **Build**: role specialists (and their future agents) execute.
5. **Assurance**: Data Assurance validates data quality; Value Assurance validates business value.
6. **Release & value check**: deploy, then confirm outcomes against success metrics.

## 3. Solution components the architect reasons about

- **Data ingestion / sources** — where data originates, how it lands, cadence, volume.
- **Data models** — canonical/warehouse models, semantic layers, contracts.
- **Analytics platforms** — the tools/layers where analysis and serving happen.
- **Integrations** — system-to-system connections, APIs, event streams.
- **Governance** — ownership, metadata, lineage, classification, compliance.
- **Scalability & reliability** — volume growth, SLAs, cost, resilience.
- **Delivery dependencies** — sequencing, prerequisites, cross-team needs.

## 4. Platform & tooling reference (TODO — confirm and fill in)

Populate with the organization's actual stack so agents reason concretely:

- **Ingestion / ETL:** _[e.g., Fivetran, Airbyte, custom]_
- **Storage / warehouse / lakehouse:** _[e.g., BigQuery, Snowflake, Databricks]_
- **Transformation / orchestration:** _[e.g., dbt, Airflow, Dagster]_
- **Analytics / BI / visualization:** _[e.g., Looker, Power BI, Tableau]_
- **Digital analytics:** _[e.g., GA4, GTM, server-side tagging]_
- **ML / data science:** _[e.g., Vertex AI, SageMaker, Databricks ML]_
- **Governance / catalog / lineage:** _[e.g., Collibra, DataHub, Purview]_
- **Cloud / infra:** _[e.g., GCP, AWS, Azure]_

Until confirmed, agents should treat platform choices as **assumptions to flag**, not facts.

## 5. Standards & guardrails (TODO — confirm and fill in)

- **Data classification levels:** _[public / internal / confidential / restricted — confirm]_
- **PII / sensitive data handling:** _[policy reference]_
- **Compliance regimes in scope:** _[e.g., GDPR, CCPA, PCI, SOX — confirm which apply]_
- **Naming / modeling conventions:** _[reference]_
- **Definition of Done for a solution brief:** clear objective, named stakeholders, identified data sources (or flagged gaps), risk register, success metrics, at least one downstream handoff.

## 6. What "good" looks like for an architecture brief

- The **objective** is stated in one sentence a sponsor would agree with.
- **Stakeholders** include a business owner and a data/technical owner (or the gap is flagged).
- Every required **data source** is named with an owner, or explicitly marked unknown.
- **Success metrics** are measurable, not aspirational.
- **Risks** are specific, categorized, and have an owner or a gap flag.
- **Handoffs** are scoped so the receiving role can start without re-interviewing the sponsor.
- **Assumptions** and **open questions** are explicit — nothing important is silently invented.

## 7. Roles as consumers/producers

| Role | Consumes | Produces |
|---|---|---|
| Solution Architect | Raw request | Architecture brief + handoffs |
| Data Engineer | Engineering handoff | Pipelines, contracts, transformations |
| Data Assurance | Data-quality handoff | QA rules, validation checklists, tests |
| Value Assurance | Business context + metrics | Value validation, outcome alignment |
| Digital Analytics | Analytics handoff | Event schema, tagging, funnels |
| Data Visualization | Viz handoff | Dashboards, KPI maps, reporting briefs |
| Data Governance | Governance handoff | Policies, ownership, metadata, lineage |
| Data Scientist | Science handoff | Models, experiments, evaluations |
| Project Manager | Dependencies + risks | Plans, RAID logs, status |
| Head of Data & Analytics | Portfolio of briefs | Prioritization, governance, alignment |
