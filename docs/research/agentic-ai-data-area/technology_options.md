# Technology Options — Frameworks and Runtime Comparison

> Document 5 of 9 — see [research_overview.md](research_overview.md) for the index; citations `[S#]` in [research_sources.md](research_sources.md).
>
> **Evidence caveat:** the strongest verified findings here are about the *category* choice (custom-lightweight vs framework), not feature-level head-to-heads. Per-framework rows below rest on **[Extracted]** single-source claims from comparison articles [S18][S19][S20][S21] — treat as directionally reliable, verify against current docs before adoption. LlamaIndex produced no surviving research claims; its row is general knowledge, marked accordingly.

## The category decision first: framework vs custom-lightweight

The most decision-relevant evidence in the entire research is category-level, and it is verified:

- Anthropic, across dozens of enterprise teams: the most successful implementations used **simple, composable patterns, not complex frameworks — start with LLM APIs directly** [S2] **[Verified]**.
- Production reality: **85% (17/20) of production case studies built custom in-house implementations with direct API calls**; the leading framework (LangChain/LangGraph) reached only 25% of survey respondents; teams explicitly migrated *off* CrewAI for production [S9] **[Verified]**.
- Stack churn: 70% of regulated enterprises rebuild their agent stack every ≤3 months — modularity beats lock-in; one team moved LangChain→Azure in two months and considered moving back [S17] **[Extracted]**.
- When frameworks *do* help: teams that don't need precise control over reasoning/memory patterns get battle-tested patterns and community support [S20] **[Extracted]**; frameworks earn their keep when they absorb durability/state/observability complexity rather than bolting it on [S21] **[Extracted]**.

**[Recommendation]** For this repo — one bounded workflow agent, schema-first, already Anthropic-targeted — **custom-lightweight on direct model APIs is the right MVP choice**, with the explicit option to adopt a graph framework later *if* orchestration complexity materializes. This matches both the evidence and the existing `config.yaml`.

## Framework comparison

| Option | Strengths | Weaknesses / documented failure modes | Best fit | Evidence |
|---|---|---|---|---|
| **Custom lightweight (direct API + thin runner)** | Full control; minimal deps; matches how 85% of production case studies ship; easiest to audit and to swap models/providers amid stack churn | You own retries, tracing, state — must build the thin substrate yourself | Bounded workflows; schema-first structured outputs; small teams | [S2][S9] **[Verified]**, [S17] |
| **Anthropic Claude API + tool use / Agent SDK** | Schema enforcement via tool-use; strong architecture-reasoning models; Agent SDK adds the agent loop, tool harness, MCP integration when needed | Tool-based structured output (vs a native response_format) is the enforcement path [S25]; SDK adds a dependency layer you may not need for a workflow | This repo's MVP runtime (already selected) | [S2][S25] **[Extracted]** |
| **LangGraph** | Explicit graph/FSM of nodes and edges; cyclical stateful flows; inspectable, retry-friendly, production-monitorable; the natural upgrade path if orchestration grows | Complexity for beginners; supervisor pattern can loop, resending output to itself and inflating tokens/runtime; poor fit for informal experimentation | Complex conditional multi-step orchestration with audit requirements | [S18][S19][S20] **[Extracted]** |
| **LangChain (classic)** | Huge integration catalog; fast prototyping | Abstraction layers obscure failure modes; the category evidence (custom-first) weighs against it; superseded by LangGraph for agent control flow | Quick integration experiments | [S9][S21] **[Extracted]** |
| **CrewAI** | Role-based multi-agent abstraction ("Crew") that mirrors org-role mapping; quick prototypes | Production reliability gaps (action traces not reflecting actual execution); teams migrated off it in production; free tier caps 50 executions/month → Enterprise contract; historically sequential-only orchestration | Role-play prototyping; demos of multi-role concepts | [S9] **[Verified — migration]**, [S19][S21] **[Extracted]** |
| **AutoGen** | Conversational multi-agent research; HITL experiments | Reproducibility/debugging problems; loop-trap and token-cost issues; **maintenance mode** — superseded by Microsoft Agent Framework | Research exploration only; not new enterprise investment | [S19][S20][S21] **[Extracted]** |
| **Semantic Kernel** | Enterprise .NET/multi-language; Azure integration; powers M365 Copilot/Bing | v1.x now bug-fix-only (≥1 year); superseded by Microsoft Agent Framework; limited memory support | Existing .NET estates — via its successor | [S19][S21] **[Extracted]** |
| **Microsoft Agent Framework** | Unified successor to AutoGen + Semantic Kernel (1.0 GA April 2026); Microsoft's single go-forward orchestration SDK | New (short production track record); gravitates to Azure ecosystem | Microsoft-stack enterprises standardizing on Azure AI | [S21] **[Extracted]** |
| **OpenAI Agents SDK / Responses API** | Minimal primitives (agents, handoffs, guardrails, tracing); provider-agnostic (100+ models); successor to experimental Swarm | No native durable execution — pair with Temporal/DBOS for workflow durability; handoff-centric patterns are the ones vendors warn about for process automation | OpenAI-centric stacks; triage/handoff use cases | [S20][S21] **[Extracted]**; handoff caveat [S1][S5] **[Verified]** |
| **LlamaIndex** | Mature RAG/data-connector toolkit; useful for the retrieval layer specifically | Agent orchestration is not its core strength | Retrieval/indexing layer under a custom agent | **[General knowledge — not covered by surviving research claims]** |

Context signal on volatility: OpenAI's Swarm was experimental and explicitly not for production, then superseded within months [S19] **[Extracted]**; OpenAI deprecated Agent Builder in June 2026 (research caveat log). Framework landscapes age in quarters — another argument for a thin, swappable core.

## Decision criteria

Apply in order **[Recommendation]** (synthesized from [S18][S21][S1][S2]):

1. **Workflow or agent?** Predictable steps → code the workflow; don't buy an orchestration framework for a pipeline [S2] **[Verified]**.
2. **Single or multi-agent?** Until a documented trigger fires (instruction failures, tool overload, parallel work exceeding context [S1][S5] **[Verified]**), orchestration frameworks solve a problem you don't have.
3. **Who absorbs reliability?** Prefer options that absorb durability/state/tracing rather than requiring bolt-ons (Temporal/Redis) that shift complexity to the team [S21] **[Extracted]**.
4. **Auditability & inspectability** — graph/FSM explicitness (LangGraph-style) beats conversational emergence (AutoGen-style) for governed environments [S20] **[Extracted]**.
5. **Exit cost** — given quarterly stack churn [S17], every choice must keep prompts, schemas, tools, and evals framework-independent (they live in the repo as data, not framework code) **[Recommendation]**.
6. **Ecosystem alignment** — if the org later standardizes on Azure/M365, Microsoft Agent Framework becomes the credible orchestrator candidate; on an Anthropic-first stack, Claude Agent SDK + MCP is the aligned path **[Inference]**.

## Recommendations

**MVP (now):**
- **Runtime:** thin custom runner (Python) calling the **Anthropic Claude API** directly; structured output enforced via tool-use against JSON Schema generated from Pydantic models [S25]; low temperature for architecture reasoning (existing config).
- **Retrieval:** start with simple indexed retrieval over the small approved corpus; LlamaIndex only if/when connector breadth is needed.
- **Observability:** trace capture from day one (e.g., a Langfuse-class tool or structured logging) — the industry's weakest, most-invested layer [S17][S18].
- **Integrations:** evaluate **MCP servers** for Jira/Confluence/catalog access when those integrations arrive — standardized, registry-friendly tool reuse [S1 tool-registry logic] **[Inference]**; needs a spike (integration patterns were not verified by this research).

**Scaling (later, trigger-gated):**
- If orchestration complexity materializes: **LangGraph** (inspectable graph control) or **Claude Agent SDK** loops; if the org is Azure-standardized by then: **Microsoft Agent Framework**.
- Keep the migration cheap by construction: prompts/schemas/tests as versioned repo data; tools behind a registry interface; runner swappable. The evidence says you will likely rebuild parts of the stack within quarters [S17] — architect for it.

**Avoid:**
- CrewAI/AutoGen for production (reliability gaps; maintenance mode) [S9][S19][S21].
- Peer-handoff architectures for process automation [S1][S5] **[Verified]**.
- Any framework adoption *before* the single agent has proven itself against evals — the framework question is premature until then [S2][S9] **[Verified]**.
