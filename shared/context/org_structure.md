# Data & AI Org Structure

> Shared ground truth. Injected into agent prompts so every agent reasons from the same org model.
> When the org changes, update this file only.

The Data & AI area is led by a **Head of Data & Analytics** and organized into specialized roles across architecture, engineering, analytics, governance, assurance, visualization, and data science.

## Roles

### 1. Head of Data & Analytics
- Overall leader of the Data & AI area.
- Responsible for strategy, prioritization, governance, delivery alignment, and cross-functional coordination.
- Sits at the top of the structure; all specialized roles ultimately roll up here.

### 2. Solution Architect  *(first agent target)*
- Reports into the Head of Data & Analytics.
- Translates business needs into technical solution designs.
- Reasons across data ingestion, data models, analytics platforms, governance requirements, integrations, scalability, and implementation dependencies.

### 3. Data Engineer
- Connected under the Solution Architect.
- Owns pipelines, data ingestion, transformations, orchestration, and technical implementation of data flows.
- Future agent support: pipeline design, data contract validation, transformation logic, engineering documentation.

### 4. Value Assurance Specialist
- Reports into the Head of Data & Analytics.
- Validates business value, delivery quality, and alignment between solutions and expected outcomes.

### 5. Data Assurance Specialist
- Connected under Value Assurance.
- Validates data quality, completeness, consistency, and reliability.
- Future agent support: QA rule generation, data validation checklists, anomaly-detection logic, test-case creation.

### 6. Data Visualization Specialist
- Reports into the Head of Data & Analytics.
- Owns dashboards, reporting design, visualization standards, and decision-making outputs.
- Future agent support: dashboard requirements, KPI mapping, visualization QA, stakeholder reporting briefs.

### 7. Digital Analytics Specialist
- Reports into the Head of Data & Analytics.
- Owns digital measurement strategy, event taxonomy, tagging requirements, analytics implementation, funnel measurement, attribution, and behavioral data quality.
- Future agent support: GA4 event schema generation, tracking QA, data layer documentation, funnel mapping, analytics governance.

### 8. Data Governance Specialist
- Reports into the Head of Data & Analytics.
- Owns governance frameworks, policies, standards, ownership, metadata, lineage, and compliance alignment.

### 9. Data Governance Analysts  *(temporary contract — 3 positions)*
- Connected under Data Governance.
- Three analyst positions, marked as **temporary contract** roles.
- Support governance execution: documentation, cataloging, metadata cleanup, stewardship workflows, policy operationalization.

### 10. Data Scientist
- Connected within the broader Data & Analytics structure.
- Owns advanced analytics, modeling, machine learning, experimentation, forecasting, and AI/ML use cases.
- Future agent support: model framing, feature discovery, experiment design, model documentation, evaluation workflows.

### 11. Project Manager
- Connected to the overall structure.
- Owns delivery coordination, timelines, dependencies, status tracking, and stakeholder alignment.
- Future agent support: project planning, RAID logs, delivery status summaries, backlog structuring.

## Reporting map (text)

```
Head of Data & Analytics
├── Solution Architect
│   └── Data Engineer
├── Value Assurance Specialist
│   └── Data Assurance Specialist
├── Data Visualization Specialist
├── Digital Analytics Specialist
├── Data Governance Specialist
│   └── Data Governance Analysts  (x3, temporary contract)
├── Data Scientist
└── Project Manager
```

## Notes from the org chart
- Roles with diagonal hatching represent **temporary contracts**.
- The **Data Governance Analyst** group is temporary contract and includes **three** positions.

## Downstream handoff targets (canonical role keys)

Agents use these canonical keys when addressing handoffs. Keep in sync with `shared/schemas/enums.json` (`downstream_role`).

| Key | Role |
|---|---|
| `data_engineering` | Data Engineer |
| `data_assurance` | Data Assurance Specialist |
| `value_assurance` | Value Assurance Specialist |
| `data_visualization` | Data Visualization Specialist |
| `digital_analytics` | Digital Analytics Specialist |
| `data_governance` | Data Governance Specialist (+ Analysts) |
| `data_science` | Data Scientist |
| `project_management` | Project Manager |
| `head_of_data` | Head of Data & Analytics |
