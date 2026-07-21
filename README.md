# Data & AI Agents

A modular foundation for role-specific AI agents supporting the **Data & AI** area of the organization.

We are building this bottom-to-top. The first agent is the **Solutions Architecture Agent**, which supports the Solution Architect role by turning business, data, analytics, and AI requests into structured, reusable solution architecture briefs.

📊 **Operating model diagram:** see [`docs/diagrams/agent_operating_model.md`](docs/diagrams/agent_operating_model.md) (renders inline on GitHub). It is a regenerable, Viamericas-themed blueprint — edit colors/structure and re-run `python docs/diagrams/render.py` ([how-to](docs/diagrams/README.md)).

## Why this repo exists

The Data & AI area has several specialized roles (see [`shared/context/org_structure.md`](shared/context/org_structure.md)). Each role does repetitive, structured thinking that an AI agent can accelerate without replacing judgment. Rather than build one monolithic assistant, we build **one focused agent per role** on top of shared context, schemas, and prompts so that:

- Agents stay small, testable, and easy to reason about.
- Outputs are standardized so downstream roles can consume them directly.
- Adding a new agent is a matter of copying a template and filling in role-specific logic.

## Repository layout

```
/agents                       # One folder per role-specific agent
  /solution_architect         # FIRST AGENT (this milestone)
    prompt.md                 # System prompt / agent instructions
    config.yaml               # Model, params, I/O wiring, metadata
    schemas/                  # Input & output JSON Schemas for this agent
    examples/                 # Worked request → brief examples
    tests/                    # Golden cases and evaluation criteria
    README.md
  /_template                  # Copy this to bootstrap a new agent

/shared
  /context                    # Reusable knowledge about the Data & AI operating model
    org_structure.md
    data_ai_operating_model.md
  /schemas                    # Cross-agent schema fragments (enums, common types)
  /prompts                    # Shared prompt building blocks (base system, style)
  /utils                      # Shared helper logic (loaders, validators)
  /mcp                        # Internal MCP server: schemas, context, validation,
                              # handoff extraction, governance registry, diagrams

/docs
  project_overview.md
  roadmap.md
  agent_design_principles.md
  /research
    /agentic-ai-data-area     # Deep-research package (9 docs) informing the roadmap
      research_overview.md    # Start here: findings, direction, risks, open decisions
  /diagrams                   # Regenerable, Viamericas-themed diagrams (Mermaid + palette)
    brand_palette.json        # Single source of truth for colors
    agent_operating_model.mmd.tpl
    render.py                 # python render.py -> regenerates the diagram

/tests                        # Cross-cutting / integration tests
```

## Design principles (short version)

1. **One role, one agent.** Each agent has a single clear owner role and job.
2. **Composition over duplication.** Shared context, schemas, and prompt blocks live in `/shared` and are referenced, not copied.
3. **Structured I/O.** Every agent has a defined input and output schema. Free-text is a rendering of structured data, not the source of truth.
4. **Handoff-first.** Outputs are designed to be consumed by the *next* role (Data Engineering, Governance, etc.), not just read by a human.
5. **Testable.** Every agent ships golden examples and evaluation criteria.

See [`docs/agent_design_principles.md`](docs/agent_design_principles.md) for the full version.

## Getting started

1. Read [`docs/project_overview.md`](docs/project_overview.md) for the big picture.
2. Read [`agents/solution_architect/README.md`](agents/solution_architect/README.md) to understand the first agent.
3. Read [`docs/roadmap.md`](docs/roadmap.md) to see how we expand to the other roles.

## Status

| Agent | Role | Status |
|---|---|---|
| Solutions Architecture Agent | Solution Architect | 🟢 v0.1 (initial) |
| Data Engineering Agent | Data Engineer | ⚪ planned |
| Data Assurance Agent | Data Assurance Specialist | ⚪ planned |
| Digital Analytics Agent | Digital Analytics Specialist | ⚪ planned |
| Data Governance Agent | Data Governance Specialist | ⚪ planned |
| Data Visualization Agent | Data Visualization Specialist | ⚪ planned |
| Data Science Agent | Data Scientist | ⚪ planned |
| Value Assurance Agent | Value Assurance Specialist | ⚪ planned |
| Project Management Agent | Project Manager | ⚪ planned |
