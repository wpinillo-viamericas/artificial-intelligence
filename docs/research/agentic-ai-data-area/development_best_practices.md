# Agent Development Best Practices

> Document 7 of 9 — see [research_overview.md](research_overview.md) for the index; citations `[S#]` in [research_sources.md](research_sources.md).

## Repository structure

The existing layout (`/agents/<role>` with prompt/config/schemas/examples/tests + `/shared` for context/schemas/prompts/utils) is consistent with the evidence and should be kept **[Recommendation]**. Research-driven additions:

```
/agents/<role>/           # unchanged: prompt.md, config.yaml, schemas/, examples/, tests/
/shared
  /context                # org ground truth (unchanged)
  /schemas                # cross-agent fragments incl. NEW: adr, diagram, clarification
  /prompts                # shared prompt blocks (unchanged)
  /utils                  # runner, validators, consistency linter
/registry                 # NEW: agents.yaml, tools.yaml (owner, risk tier, scopes, eval status)  [S8]
/evals                    # NEW: golden cases, rubrics, judge prompts, run reports              [S4]
/policies                 # NEW (when guardrails land): policy-as-code, versioned              [S8]
/docs/research/...        # this package
```

Key properties: prompts/schemas/evals are **framework-independent data** (survives the quarterly stack churn documented in [S17]); everything an auditor needs is in git history; a new agent is a folder copy plus registry entry.

## Prompt management

- Prompts are versioned, PR-reviewed repo artifacts with lineage and rollback — "version and govern prompts like code" [S8] **[Extracted]**.
- Compose from shared blocks + role logic; inject org facts from `/shared/context` rather than hardcoding (existing principle #6); derive agent instructions from existing operating procedures and policy documents where they exist [S1] **[Extracted]**.
- Treat **tool definitions as prompt engineering**: Anthropic spent more time optimizing tools than prompts; a single interface change eliminated an error class; rewriting flawed tool descriptions cut downstream task time 40% [S2][S3] **[Extracted]**. Review tool names/descriptions/parameter docs with the same rigor as prompts.
- Keep tools few and orthogonal — overload comes from similarity/overlap, not count [S1] **[Extracted]**.
- Model strategy: prototype with the most capable model, establish the eval baseline, then downshift smaller models where accuracy holds [S1] **[Extracted]**. Pin model versions in `config.yaml`; upgrades go through evals like any other change.

## Schema design (schema-first outputs)

- **Define once in code (Pydantic), generate JSON Schema, enforce at the API, validate on return.** Prompt-and-parse/regex approaches are fragile and break across model changes; schema-enforced structured outputs are the production pattern [S25] **[Extracted]**. With Claude, enforcement is via tool-based structured output (schema passed as a tool definition) [S25] **[Extracted]**.
- Structured output is the source of truth; prose is a rendering (existing principle #2).
- Shared enums for anything that must be consistent across agents (roles, severities, categories) — specification defects cause the plurality (41.8%) of multi-agent failures, so contracts-by-schema is the cheapest insurance available [S10] **[Extracted]**.
- Uncertainty is part of the schema: `unknown`/`not_provided` states, `assumptions[]` with `impact_if_wrong`, `open_questions[]` with `directed_to` (existing design, evidence-aligned [S12]).
- Version schemas; breaking changes bump major versions and require coordinated updates to consumers (downstream agents' input schemas).

## Testing and evaluation

The most important practice area — rigorous testing of GenAI architecture outputs is "typically missing" in the field [S12] **[Extracted]**, and evals/observability are the industry's weakest layer [S17] **[Extracted]**.

- **Start now, start small: 20–50 tasks drawn from real failures/requests.** Teams that wait to build hundreds end up reverse-engineering success criteria from a live system [S4] **[Extracted]**. Anthropic's research system started with ~20 representative queries [S3] **[Extracted]**.
- **Three grader types, layered**: deterministic code graders where possible (schema validity, required fields, enum conformance, cross-artifact consistency); LLM-as-judge where necessary; human graders judiciously for calibration [S4] **[Extracted]**.
- **Grade outcomes, not paths.** Asserting specific tool-call sequences produces brittle tests; agents find valid unanticipated approaches [S4] **[Extracted]**. For the SA Agent: grade the brief (completeness, planted-risk detection, correct handoff targeting), not the intermediate steps.
- **A single rubric-scoring judge call (0.0–1.0 + pass/fail) beat panels of specialized judges** for consistency and human alignment [S3] **[Extracted]**. Calibrate the judge against the human architect's scores periodically [S4].
- **Pick the right reliability metric**: pass@k for one-success-suffices tools; **pass^k for consistency-critical outputs** — at 75% per-trial success, all-3-of-3 is only ~42% [S4] **[Extracted]**. Downstream-consumed briefs are consistency-critical → track pass^k **[Inference]**.
- **LLM-judge is a pre-screen, never the verdict**: production norm is judge paired with human review; 74% of deployed agents rely primarily on human evaluation [S9] **[Verified]**.
- **Eval-driven development**: write evals for planned capabilities before building them; iterate until green [S4] **[Extracted]**. Ownership model: central eval infrastructure, domain experts contribute tasks [S4].
- **Tag failures with a taxonomy** (MAST's 14 modes/3 categories: specification, misalignment, verification) so recurring failure classes become visible; an LLM-judge annotation pipeline achieved 94% accuracy vs experts — automatable later [S10] **[Extracted]**.

## Regression testing and CI/CD

**[Recommendation]**, assembled from [S4][S8][S23][S22]:

| Gate | Runs on | Blocks merge? |
|---|---|---|
| Schema validation of examples + golden outputs | Every PR | Yes |
| Deterministic output checks (enums, cross-refs, consistency linter across brief/ADR/diagram [S23]) | Every PR | Yes |
| Golden-case regression (N=20–50): run agent, judge-score against rubric, compare to baseline | PRs touching prompts/schemas/config/model | Yes, on regression |
| Human spot review of sampled outputs | Pre-release | Release gate |
| Fitness-function-style conformance checks (decisions enforced as automated checks, optionally LLM-assisted) | CI, scheduled | Advisory → hardening |

- Nondeterminism rule: use scoring rubrics or LLM-as-judge in integration tests, never exact-match assertions [S5] **[Verified]**.
- Deploy path: dev → test (against golden cases + sandboxed tools) → prod, with environment separation as a governance prerequisite [S6] **[Extracted]**; sandboxed testing before autonomy [S2] **[Verified]**.
- Docs-as-code publishing (brief → HTML/Confluence, diagrams exported from DSL) is CI-automatable end to end [S24] **[Extracted]**.

## Monitoring, logging, and QA in production

- **Trace every prompt, response, and tool call** in a structured timeline [S18] **[Extracted]**; instrument all operations and handoffs, track per-agent token consumption for cost targeting [S5] **[Verified]**.
- **Layered quality (Swiss-cheese model)**: automated evals for iteration speed, production monitoring for ground truth, A/B testing for deployed changes, periodic human review to calibrate judges — no single layer catches everything [S4] **[Extracted]**.
- Product-level health metrics for the SA Agent **[Inference]**: reviewer approval rate; draft-vs-approved edit distance; open-questions-per-brief trend; downstream rework attributable to brief gaps; cost per brief.
- Budget/failure alerting: iteration-cap hits, schema-failure spikes, token budget breaches → escalate with trace [S1] **[Verified — failure-threshold trigger]**.

## Documentation standards

- Each agent ships its contract: README (what/how/IO contract), examples, golden cases (existing anatomy).
- Output artifacts follow recognized standards — MADR/Nygard ADRs with immutability/supersession semantics [S22], arc42-informed brief structure, C4 diagrams as versionable text [S23][S24] (details in [solutions_architecture_agent_research.md](solutions_architecture_agent_research.md)).
- Decisions about the agent platform itself are recorded as ADRs in this repo — the platform should eat its own cooking **[Recommendation]**.
- Run metadata on every output (agent/prompt/model versions, input ref, reviewer) — the traceability spine ([governance_security_and_risk.md](governance_security_and_risk.md)).
