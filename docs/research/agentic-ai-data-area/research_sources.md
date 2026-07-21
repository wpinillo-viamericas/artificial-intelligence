# Research Sources

> Part of the [agentic AI research package](research_overview.md). All documents in this package cite sources as `[S#]`, resolved here.
>
> **How this research was produced (methodology).** A deep-research pipeline decomposed the research question into 5 search angles (authoritative enterprise agent guidance; framework comparison/benchmarks; Solutions-Architecture-Agent-specific design; enterprise governance/security/maturity; contrarian/failure-mode evidence), ran parallel web searches per angle, fetched the 23 highest-value sources, extracted 115 falsifiable claims with verbatim quotes, and adversarially verified the top 25 claims with 3 independent verification votes each. **All 25 verified claims were confirmed 3–0; none were refuted.** Research date: 2026-07-06.
>
> **Evidence tiers used across this package:**
> - **[Verified]** — claim survived 3-vote adversarial verification against the primary source.
> - **[Extracted]** — claim extracted verbatim from a fetched source but not put through adversarial verification (budget-limited). Reliable as "the source says X," not independently corroborated.
> - **[Inference]** — our reasoned application of verified/extracted evidence to this organization's context. Not a sourced fact.
> - **[Assumption]** / **[Open decision]** — explicitly unconfirmed; listed in [implementation_prerequisites.md](implementation_prerequisites.md).

## Known bias and coverage caveats

- **Source concentration:** most verified claims come from four vendors' own guidance (OpenAI, Anthropic, Microsoft, AWS). These are the authoritative primary sources, are mutually consistent, and are notably self-critical (e.g., Anthropic's 15× cost admission), but vendor guidance shifts fast — Anthropic's Dec-2024 workflow-first emphasis softened by late 2025 toward agent-loop/context-engineering approaches, and OpenAI deprecated Agent Builder in June 2026. Architectural principles age slower than product framings.
- **Small-n empirical bases:** the production-practices statistics [S9] rest on 20 case studies plus a modest survey (N≈86) skewed toward mature teams. AgenticAKM [S11] is a single workshop-scale study (13 evaluators, no significance testing). The AAGMM maturity results [S13] are simulation-based, not field-observed.
- **Angles covered only by extraction/inference, not adversarial verification:** feature-level framework head-to-heads, concrete Jira/Confluence/GitHub/M365 integration patterns, arc42/C4 adoption data, staged maturity-model governance gates, and agent-to-role mapping for the other seven Data & AI roles. Documents flag these accordingly.
- LlamaIndex was named in the research scope but produced no surviving claims; [technology_options.md](technology_options.md) covers it from general framework knowledge, labeled as such.

## Primary vendor guidance

| # | Source | Why it matters |
|---|---|---|
| S1 | [OpenAI — *A Practical Guide to Building Agents* (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | The gating test for agent-worthy use cases; single-agent-first guidance; manager vs decentralized orchestration; layered guardrails; per-tool risk ratings; the two mandatory HITL triggers; tool-registry and model-downshift strategy. Most-cited source in this package. |
| S2 | [Anthropic — *Building Effective Agents*](https://www.anthropic.com/research/building-effective-agents) | Canonical workflow-vs-agent distinction; five composable patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer); "start with LLM APIs directly, not frameworks"; tool design as the agent-computer interface. |
| S3 | [Anthropic — *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system) | The best publicly available multi-agent cost/benefit data: 90.2% gain on parallelizable research, token usage explaining 80% of variance, 4×/15× token costs, delegation-specification failure modes, effort-scaling rules. Self-critical engineering postmortem. |
| S4 | [Anthropic — *Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Start evals at 20–50 tasks from real failures; grader taxonomy (code/LLM/human); outcome- not path-grading; pass@k vs pass^k; eval-driven development; Swiss-cheese layered quality model. |
| S5 | [Microsoft — Azure Architecture Center: *AI agent design patterns*](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | "Single agent with tools is often the right default for enterprise"; five orchestration patterns with explicit failure modes; security trimming per agent; content-safety at four points; LLM-as-judge integration testing; multi-agent antipatterns. Updated May 2026. |
| S6 | [Microsoft — *Agentic AI adoption maturity model: security & governance*](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/maturity-model-security-governance) | Five governance maturity levels (100–500); Level-100 prerequisites before any broad adoption; tiered (not uniform) controls by agent risk; agent registry + AI Council with real decision rights. |
| S7 | [AWS — Prescriptive Guidance: *Agentic AI patterns*](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html) | Workflow agents (centralized) vs multi-agent collaboration (decentralized); agentic patterns as evolutions of event-driven architecture; pattern selection is contextual and composable; concrete AWS service mappings. |
| S8 | [OpenAI Cookbook — *Agentic governance guide*](https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook) | Governance-as-code accelerates delivery; agent/tool/prompt registries with owner, risk tier, scopes, rollback; risk-tiered controls; policy-as-code as installable versioned library. |

## Peer-reviewed / academic

| # | Source | Why it matters |
|---|---|---|
| S9 | [*Measuring Agents in Production* — arXiv 2512.04123 (ICML 2026 oral)](https://arxiv.org/pdf/2512.04123) | Largest empirical study of production agents (20 case studies + practitioner survey): 68% ≤10 steps, 70% prompting-only, 80% structured workflows, 85% custom implementations, 74% human-primary evaluation, internal-first deployment, systems-level (not model-level) reliability. |
| S10 | [*Why Do Multi-Agent LLM Systems Fail?* (MAST) — OpenReview, NeurIPS 2025](https://openreview.net/forum?id=fAjbYBmonr) | 41–86.7% failure rates across 7 open-source multi-agent systems; 14 failure modes in 3 categories (specification 41.8%, inter-agent misalignment 36.9%, verification 21.3%); validated LLM-as-judge failure-annotation pipeline (94% accuracy). |
| S11 | [*AgenticAKM* — arXiv 2602.04445 (ICSE 2026 AGENT workshop)](https://arxiv.org/html/2602.04445v1) | Directly on-topic: orchestrated Extraction→Retrieval→Generation→Validation pipeline with human-architect supervision beat single-prompt LLMs at ADR generation (3.8–3.9 vs 3.3/5, blind study, 29 repos); bounded 3-iteration validator loops. Preliminary (small n). |
| S12 | [*GenAI in Software Architecture* systematic review — arXiv 2503.13310](https://arxiv.org/pdf/2503.13310) | Requirements-to-architecture is the #1 GenAI architecture use case (40% of studies); 85% of systems are human-in-the-loop assistive; rigorous output testing typically absent; C4/ADR generation is thinly evidenced (1 study each) — validates the use case and flags the evaluation gap. |
| S13 | [*Agentic AI Governance Maturity Model* (AAGMM) — arXiv 2604.16338](https://arxiv.org/pdf/2604.16338) | Five-level governance maturity across 12 domains; Level 3 (formal policies, central agent catalog, RBAC, HITL) as minimum viable governance; sprawl taxonomy (functional duplication, shadow/orphaned agents, permission creep, unmonitored delegation). Simulation-based results. |
| S14 | [Google Research — multi-agent scaling study, arXiv 2512.08296](https://arxiv.org/abs/2512.08296) | 180-configuration study: +81% on a parallelizable task, −70% on a sequential task — empirical confirmation of the parallelizable-vs-sequential fit criterion for multi-agent designs. |
| S15 | [Tran & Kiela — arXiv 2604.02460](https://arxiv.org/abs/2604.02460) | Single agents match multi-agent systems under equal token budgets — multi-agent gains largely come from extra compute, not architecture per se. |

## Practitioner / industry

| # | Source | Why it matters |
|---|---|---|
| S16 | [Cognition — *Don't Build Multi-Agents*](https://cognition.com/blog/dont-build-multi-agents) | Strongest contrarian practitioner voice: parallel-subagent architectures are fragile (dispersed decisions, unshared context); single-threaded linear agent + context compression suffices for most production tasks. |
| S17 | [Cleanlab — *AI Agents in Production 2025* survey](https://cleanlab.ai/ai-agents-in-production-2025/) | Adoption reality check: only ~5% of 1,837 leaders have agents in production; 70% of regulated enterprises rebuild their stack ≤ every 3 months (design for modularity, not lock-in); observability/evals are the weakest, top-investment layer; 42% of regulated firms adding approval controls. |
| S18 | [Langfuse — agent framework comparison](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) | Framework decision variables (task complexity, collaboration, integration, performance); LangGraph/CrewAI/Semantic Kernel positioning; tracing as production necessity. |
| S19 | [Turing — AI agent frameworks comparison](https://www.turing.com/resources/ai-agent-frameworks) | Six-framework comparison incl. failure modes: LangGraph supervisor loops, AutoGen debugging loops and token costs, CrewAI sequential-only orchestration (at time of writing), Semantic Kernel .NET enterprise fit. |
| S20 | [Atla — AI agent frameworks analysis](https://atla-ai.com/post/ai-agent-frameworks) | LangGraph as inspectable FSM for production; AutoGen reproducibility problems; CrewAI role-structure limits; when to skip frameworks for raw APIs; OpenAI Agents SDK primitives (agents, handoffs, guardrails, tracing). |
| S21 | [LangChain — AI agent frameworks resource](https://www.langchain.com/resources/ai-agent-frameworks) | Microsoft Agent Framework as unified successor to AutoGen + Semantic Kernel (1.0 GA April 2026); CrewAI production reliability gaps and pricing gates; OpenAI Agents SDK needs external durability (Temporal/DBOS); Google ADK session-isolation failure mode. Vendor-published; treat comparative judgments cautiously. |

## Architecture documentation standards

| # | Source | Why it matters |
|---|---|---|
| S22 | [joelparkerhenderson/architecture-decision-record (GitHub)](https://github.com/joelparkerhenderson/architecture-decision-record) | Canonical ADR reference: definition, quality rules (one decision per record, immutability/supersession), and the template landscape (Nygard, MADR, Tyree/Akerman, arc42). |
| S23 | [MSiccDev/arc42-toolkit (GitHub)](https://github.com/MSiccDev/arc42-toolkit) | Working example of LLM-driven arc42 documentation: ask-first intake (no generation before clarifying questions answered), 14 provider-agnostic skills, deterministic cross-artifact consistency linter in CI, C4-as-PlantUML output, three depth levels. |
| S24 | [bitsmuggler/arc42-c4-software-architecture-documentation-example (GitHub)](https://github.com/bitsmuggler/arc42-c4-software-architecture-documentation-example) | Docs-as-code reference: arc42 + C4 via Structurizr DSL → PlantUML export → CI-built HTML/PDF; ADRs as Markdown via adr-tools; Technical Debt Records as a distinct artifact; self-hosted-Kroki privacy caveat. |
| S25 | [Agenta — structured outputs & function calling guide](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms) | Schema-first pattern: define once in Pydantic/Zod, generate JSON Schema, enforce via API-native structured outputs (or Claude tool-based schema), validate on return; prompt/regex parsing is fragile in production. |
