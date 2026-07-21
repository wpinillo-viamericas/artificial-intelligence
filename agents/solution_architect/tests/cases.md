# Solutions Architecture Agent — Test Cases & Evaluation Rubric

Golden cases and the rubric used to judge whether an output brief is good. Use these when changing the prompt or schema. In Phase 1, `shared/utils/schema_validator` automates the structural checks; the rubric checks stay human/LLM-judged for now.

## Evaluation rubric (applies to every case)

A brief **passes** only if all of these hold:

1. **Schema-valid.** Output validates against `schemas/output.schema.json` (enums resolve, required fields present, no extra fields).
2. **Objective is specific.** Not a generic aspiration; a sponsor would recognize and agree with it.
3. **Ownership is honest.** A business owner and a data/technical owner are named, or each missing one is flagged in `risks` (`missing_ownership`) and `open_questions`.
4. **No fabrication.** Every data source / stakeholder / metric is either supported by the input or marked `assumed`/`unknown`. Assumptions appear in `assumptions`.
5. **Risks are specific.** At least the relevant lenses are covered (ownership, data source, data quality, security/compliance, scalability, success metric, integration). No boilerplate.
6. **Handoffs are actionable.** Each handoff has an objective, concrete scope, and lets the receiving role start without re-interviewing the requester.
7. **Confidence matches input richness.** Thin input → `overall_confidence: low` and many open questions; rich input → higher confidence.

## Case 1 — GA4 funnel dashboard (worked example)

- **Input:** `examples/request_ga4_funnel.json`
- **Reference output:** `examples/output_ga4_funnel.json`
- **Must catch:** unknown app instrumentation (data source risk), PII/compliance risk, missing technical owner (ownership gap), non-measurable adoption metric.
- **Must hand off to:** `digital_analytics`, `data_governance`, `data_visualization`, `project_management`.

## Case 2 — Thin one-liner (tests honesty under missing info)

- **Input (request_text only):** "We need better reporting on customer churn."
- **Must produce:** `overall_confidence: low`; objective that flags churn is undefined; open questions for definition of churn, data sources, sponsor, success metric; ownership gaps flagged.
- **Must NOT:** invent data sources, a sponsor, or a specific churn definition.

## Case 3 — Data pipeline / integration

- **Input:** "Ingest transaction data from the payments system into the warehouse so analysts can query it daily."
- **Must catch:** data contract/quality needs, scalability (volume/cadence), source ownership, PII in transaction data.
- **Must hand off to:** `data_engineering` (primary), `data_governance`.
- **request_type:** `data_pipeline_integration`.

## Case 4 — AI/ML use case

- **Input:** "Build a model to predict which customers are likely to send a second transfer within 30 days."
- **Must catch:** label/target definition, feature/data availability, evaluation approach as open question, model governance/compliance.
- **Must hand off to:** `data_science` (primary), `data_engineering` (features), `value_assurance` (business value).
- **request_type:** `ai_ml_use_case`.

## Case 5 — Governance / data quality initiative

- **Input:** "We keep finding mismatched customer records across systems and need to fix data quality."
- **Must catch:** unclear scope, ownership/stewardship gaps, need for profiling, lineage/metadata needs.
- **Must hand off to:** `data_governance` (primary), `data_assurance`.
- **request_type:** `data_quality_governance`.

## How to run (Phase 1)

1. Run each case through the agent runner.
2. Validate output structurally with `schema_validator`.
3. Score against the rubric (human or LLM judge).
4. A prompt/schema change ships only if all existing cases still pass.

## Adding cases

Add real (anonymized) requests as new cases as they come in. Aim for coverage across all `request_type` values and across each downstream handoff role.
