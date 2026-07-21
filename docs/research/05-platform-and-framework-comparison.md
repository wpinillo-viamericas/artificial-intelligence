# 05 — Platform and Framework Comparison

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — index and evidence-tier
> legend there. Citations `[S#]` resolve in [references.md](references.md).
>
> **Evidence caveat.** The strongest *verified* finding is the **category** choice
> (custom-lightweight vs heavy framework) [S2][S9]. Product-level facts below are **[Extracted]**
> from vendor docs/changelogs refreshed to mid-2026; release dates from secondary sources are
> flagged. Verify against current docs before adoption — the landscape ages in quarters [S17].

## The category decision comes first

Verified, and decision-dominant:

- Anthropic, across dozens of enterprise teams: the most successful implementations used **simple,
  composable patterns, not complex frameworks — start with LLM APIs directly** [S2] **[Verified]**.
- Production reality: **85% of case studies are custom in-house implementations calling APIs
  directly**; the leading framework reached only ~25% of respondents; teams migrated *off* CrewAI
  for production [S9] **[Verified]**.
- **70% of regulated enterprises rebuild their agent stack every ≤3 months** — modularity beats
  lock-in [S17] **[Extracted]**.

**[Recommendation]** For one bounded, schema-first, Anthropic-targeted workflow agent,
**custom-lightweight on direct model APIs is the right MVP core**, with a clear upgrade path to a
managed runtime (AgentCore) and/or a durable graph framework (LangGraph) *if* orchestration
complexity or operational burden materializes. Keep prompts, schemas, tools, and evals as
framework-independent repo data so the core is swappable.

## What changed by mid-2026 (refresh)

- **Amazon Bedrock AgentCore** went **GA 2025-10-13** — a framework-agnostic platform with
  **Runtime, Memory, Gateway, Identity, Observability** services plus built-in Code Interpreter and
  Browser tools; Runtime gives 8-hour execution windows and session isolation; Gateway turns
  APIs/Lambda into tools **and connects to existing MCP servers**; it inherits Bedrock compliance and
  is **in AWS GovCloud (US-West) as of 2026-05** [S26][S27][S28]. This materially changes the
  build-vs-buy math for an AWS-hosted regulated agent.
- **Bedrock Agents "Classic"** (the original low-code Action-Groups agents) is reported **closed to
  new customers 2026-07-30** — AgentCore is the strategic path [S26] *(close date via secondary
  source — verify)*.
- **LangChain and LangGraph both hit 1.0 GA (2025-10)** — LangGraph is now a low-level durable/
  stateful runtime (persistence, HITL, checkpoints) [S30].
- **Microsoft Agent Framework 1.0 GA (2026-04-03)** unifies and supersedes Semantic Kernel + AutoGen
  (both now maintenance-mode) [S31]; Azure-leaning.
- **MCP** became the de-facto tool-integration standard and was **donated to the Linux Foundation's
  Agentic AI Foundation (2025-12)** with AWS/Google/Microsoft backing; it is native in AgentCore
  Gateway [S32].
- **OpenSearch (hybrid vector) GA on Bedrock KB (2025-03)**; cheaper **S3 Vectors** and
  **scale-to-zero NextGen OpenSearch Serverless (GA 2026-05)** now exist [S87]
  ([11](11-cost-and-scalability.md)).

## Framework / runtime comparison (mid-2026)

| Option | Strengths | Weaknesses / failure modes | Best fit here | Evidence |
|---|---|---|---|---|
| **Custom lightweight** (direct API + thin runner) | Full control; minimal deps; matches how 85% of prod ships; easiest to audit and to swap models | You own retries, tracing, state | ✅ **MVP core** | [S2][S9] **[Verified]**, [S17] |
| **Anthropic Claude API + Agent SDK** | Schema via tool-use; strong reasoning models; SDK adds loop/tool harness/MCP when needed | SDK is a dependency you may not need for a workflow | ✅ MVP runtime (per `config.yaml`) | [S2][S25] |
| **Amazon Bedrock AgentCore** | Managed runtime/memory/gateway/identity/observability; VPC/PrivateLink; GovCloud; MCP-native; framework-agnostic | Newer; AWS-hosted (though low framework lock-in) | ✅ **strong** managed-runtime candidate for an AWS regulated shop | [S26][S27][S28] |
| **LangGraph 1.0** | Durable, inspectable graph/FSM; persistence, checkpoints, HITL; portable | Complexity for simple pipelines; supervisor loops can inflate tokens | ⚠️ adopt if orchestration grows | [S30][S18][S19] |
| LangChain 1.0 | Huge integration catalog; fast prototyping | Abstraction obscures failure modes; superseded by LangGraph for control flow | ⚠️ quick experiments | [S9][S30] |
| Microsoft Agent Framework 1.0 | Unified MS successor; graph workflows; telemetry | Short track record; Azure-leaning | ⚠️ only if org standardizes on Azure/M365 | [S31] |
| OpenAI Agents SDK | Minimal primitives; provider-agnostic; tracing | No native durability (pair Temporal/DBOS); handoff-centric patterns vendors warn about | ⚠️ OpenAI-centric stacks | [S20]; handoff caveat [S1][S5] |
| CrewAI | Fast role-based multi-agent prototyping | Production reliability gaps; teams migrated off; pricing gates | ❌ prototyping/demos only | [S9][S19] |
| AutoGen | Conversational multi-agent research | Reproducibility/loop issues; **maintenance mode** (folded into MS AF) | ❌ not new investment | [S19][S31] |
| Semantic Kernel | .NET/Azure; powered M365 Copilot | Bug-fix-only; superseded by MS AF | ❌ via successor only | [S31] |
| LlamaIndex | Mature RAG/data-connector toolkit | Orchestration isn't its strength | ⚠️ retrieval layer under a custom agent | **[General knowledge]** |
| AWS Step Functions / Lambda / EventBridge | Deterministic, auditable serverless orchestration around the agent; direct Bedrock integration | Not an "agent framework"; infra to operate | ✅ deterministic glue + event/scheduled triggers | [S29] |

## Decision matrix — 15 criteria

Scoring: **●** strong · **◐** partial · **○** weak, judged **for this org** (one AWS-hosted,
regulated, low-volume internal agent). This is a directional aid, not a benchmark — weights should
be set with the platform owner.

| Criterion | Custom-light + Claude API | Bedrock AgentCore | LangGraph 1.0 | MS Agent Framework |
|---|---|---|---|---|
| Enterprise readiness | ◐ (you build hardening) | ● (managed, GA) | ● | ● |
| AWS integration | ◐ | ● (native) | ◐ (runs on AWS) | ○ (Azure-leaning) |
| Security | ◐ (DIY) | ● (Bedrock inherits SOC2/ISO/HIPAA; GovCloud) | ◐ | ◐ |
| Compliance / data handling | ● (Bedrock/Anthropic ZDR options [S57][S58]) | ● | ◐ | ◐ |
| Observability | ○ (build it) | ● (CloudWatch GenAI + OTEL export) | ◐ (LangSmith-leaning) | ◐ |
| Vendor lock-in (lower = better) | ● (lowest) | ◐ (AWS, but MCP/any-framework) | ● (portable) | ○ |
| Development complexity (lower = better) | ● (simplest) | ◐ | ◐ | ◐ |
| Testing | ● (plain code) | ◐ | ◐ | ◐ |
| Scalability | ◐ | ● (8-hr runtime, isolation) | ● | ● |
| State management | ○ (DIY) | ● (Memory service) | ● (checkpoints) | ● |
| Tool integration | ◐ (wire yourself / MCP) | ● (Gateway + MCP-native) | ● | ● |
| Cost (lower = better) | ● (pay only tokens) | ◐ (managed services) | ● | ◐ |
| Latency | ● (no extra hops) | ◐ | ◐ | ◐ |
| Model portability | ● (any provider) | ◐ (Bedrock catalog) | ● | ◐ |
| Community maturity / maintainability | ● (Anthropic) / ◐ | ● / ● | ● / ● | ◐ / ◐ |

**Reading:** custom-light wins on simplicity, lock-in, cost, and latency (right for an MVP);
AgentCore wins on managed security/observability/state (right when the operational burden of DIY
outweighs the simplicity). They are **complementary, not exclusive** — the recommended path starts
custom-light and can *host* that same thin agent on AgentCore Runtime later with minimal change,
because the logic is framework-independent.

## Build vs buy

- **Build (own it):** the agent's reasoning (prompts), contracts (schemas), golden cases, and the
  thin runner — these are your differentiation and must survive stack churn as repo data [S17].
- **Buy / reuse (managed):** runtime hosting, memory, retrieval (Bedrock KB/OpenSearch),
  observability (CloudWatch GenAI + a tracing tool), identity/gateway, and evaluation tooling —
  wherever a managed AWS service removes undifferentiated heavy lifting without deep lock-in.
- **Centralize (shared services):** anything ≥2 agents use — retrieval, tool registry, prompt/
  schema versioning, evals, observability, governance registry ([02](02-agentic-ai-operating-model.md)).

## Recommendations

**MVP (now):** thin Python runner on the **Anthropic Claude API** (per `config.yaml`), structured
output via tool-use against Pydantic-generated JSON Schema [S25]; simple indexed retrieval over the
small approved corpus; **trace capture from day one** [S17]; internal MCP server (already built) as
the first, lowest-risk tool integration.

**Scaling (trigger-gated):** if operational burden grows, **host the thin agent on Bedrock
AgentCore Runtime** (managed state, identity, observability, GovCloud) [S26]; if orchestration
complexity materializes, adopt **LangGraph 1.0** for durable graph control [S30]; expose enterprise
tools via **MCP through AgentCore Gateway** [S26][S32]. Reconsider Microsoft Agent Framework only if
the org standardizes on Azure/M365 [S31].

**Avoid:** CrewAI/AutoGen for production; peer-handoff architectures for process automation
[S1][S5]; Bedrock Agents "Classic" for new build; and **any framework adoption before the single
agent has proven itself against evals** [S2][S9].
