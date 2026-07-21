# 11 — Cost and Scalability

> Part of the **[Agentic AI Research Library](00-executive-summary.md)** — index and evidence-tier
> legend there. Citations `[S#]` resolve in [references.md](references.md).
>
> **Pricing caveat.** Prices are volatile. Anthropic-API rates are from the bundled `claude-api`
> catalog (cached **2026-06-24**) [S88]; AWS-side figures are web-sourced and dated [S81]. Treat all
> numbers as **"verify at time of use."**

## Design stance

**[Recommendation]** For a low-volume internal agent, cost is dominated not by clever token tricks
but by two levers: **(1) prompt caching + the smallest adequate model**, and **(2) the vector-store
idle floor.** Track **cost per successful task**, not raw tokens. Do not buy provisioned throughput.

## Cost drivers

| Driver | Typical weight (low-volume internal agent) | Lever |
|---|---|---|
| Model inference (input/output tokens) | Medium | Caching, smaller model, routing, context trimming |
| **Vector storage** | **Often the largest line item** | Scale-to-zero store; avoid OCU idle floor |
| Embeddings | Negligible vs generation | Batch; cheap embedding model |
| Retrieval / rerank calls | Low-medium | Cache reads; rerank only the shortlist |
| Tool execution | Low | — |
| Workflow orchestration | Low (managed) / your time (DIY) | Managed runtime vs DIY |
| Logging / tracing | Low-medium | Sampling in production |
| Evaluation | Low (periodic) | Batch eval runs |
| Human review | **Real cost** (reviewer time) | Low pilot volume; rubric efficiency |
| Infrastructure (runtime, state) | Low (serverless) | Scale-to-zero |
| Development & maintenance | Highest over time | Modular, framework-independent repo data [S17] |

## Model pricing (per 1M tokens, verify at use)

**Anthropic API** [S88], cached 2026-06-24:

| Model | Input | Output |
|---|---|---|
| Opus 4.8 / 4.7 | $5 | $25 |
| Sonnet 5 | $3 ($2 intro → 2026-08-31) | $15 ($10 intro) |
| Haiku 4.5 | $1 | $5 |
| Fable 5 | $10 | $50 |

**Amazon Bedrock** matches per-token rates for equivalent tiers but **lags on the newest model IDs**
(public pages list the 4.6-era lineup) [S81]; cross-region inference profiles reportedly add ~10%
*(unverified)*. Config pins `claude-opus-4-8`; prototype on the capable model, then downshift where
evals hold [S1].

## Cost-control techniques (ranked by impact here)

1. **Prompt caching** — biggest single lever. Cache reads cost ~0.1× input (up to ~90% off cached
   input); cache writes cost 1.25× (5-min TTL) or 2× (1-hour TTL, added on Bedrock 2026-01-26).
   Cache-heavy agents typically save **60–70% of task cost**; break-even ~2–3 requests [S82][S83]
   **[Extracted]**. The SA Agent's large, stable system prompt + injected org context is an ideal
   cache prefix.
2. **Smallest adequate model + cascade** — default to Haiku/Sonnet, escalate to Opus/Fable only on
   low confidence. A Haiku call is ~5× cheaper (in and out) than Opus. **Bedrock Intelligent Prompt
   Routing** automates within-family routing for up to ~30% savings without accuracy loss [S85].
3. **Context reduction** — trim/compact prompts, clear stale tool results (context editing) in long
   loops; fewer resent tokens each turn.
4. **Batch processing** — **50% off** for async, non-latency-sensitive work (Bedrock batch;
   Anthropic Message Batches) — useful for eval runs and bulk corpus processing [S84].
5. **Avoid provisioned throughput** — hourly per model-unit (~$40–200/hr); only economical at
   sustained high volume [S81]. Not for a dozens-of-runs/day agent.

## The vector-store trap (scalability + cost)

- **Classic OpenSearch Serverless historically required a ~2-OCU minimum → ~$350+/mo floor even when
  idle** — this typically **dwarfs** a low-volume agent's token spend [S87] **[Extracted]**.
- **NextGen OpenSearch Serverless (GA 2026-05-28) removes the OCU minimum and scales to zero after
  ~10 min idle** — materially better for low-volume RAG [S87]. **S3 Vectors** (GA 2025-12,
  sub-second, ~90% cheaper) and **pgvector** are alternatives that avoid the OCU floor.
- **[Recommendation]** For the MVP, use a **scale-to-zero** store (NextGen Serverless or S3 Vectors);
  reserve provisioned OpenSearch for sustained high query volume.

## Order-of-magnitude estimate (illustrative — not measured)

**[Assumption]** ~50 runs/day, ~15K input + ~2K output tokens/run, Sonnet-class ($3/$15), large
shared prompt cached:

- No cache: 50 × (15K×$3 + 2K×$15)/1M ≈ **~$3.75/day ≈ $110/mo**.
- With caching (~70% input cached at 0.1×): **~$1.6/day ≈ $50/mo**.
- Opus-class ≈ double.
- **Dominant line item is usually the vector store**: classic Serverless idle floor ≈ **$350+/mo**
  vs ~$50–110/mo token spend. With NextGen/pgvector, keep the whole agent in the **~$50–150/mo
  all-in** range [S87][S82].

Human review time is a real, separate cost — keep pilot volume low and reviews rubric-efficient.

## Cost governance

- **Cost allocation:** Bedrock **Application Inference Profiles** carry custom cost-allocation tags
  (e.g., `team:data-ai`, `agent:solution_architect`) for per-team/per-agent attribution — the
  AWS-native **showback/chargeback** path, no custom metering pipeline [S86] **[Extracted]**.
- **Budgets & quotas:** AWS Budgets threshold alerts; Bedrock RPM/TPM service quotas per model as
  spend guardrails; per-run and per-month token ceilings (decision **D10**) [S3].
- **Metric:** **cost per successful task** (total token+infra spend ÷ tasks passing acceptance) —
  captures retries, cascades, and failed runs that per-token views hide. Wire it into the eval/
  observability layer ([09](09-evaluation-and-testing.md), [10](10-observability-and-governance.md)).

## Decision matrix — cost posture by scale

| Posture | Model | Vector store | Throughput | When |
|---|---|---|---|---|
| **MVP (dozens/day)** | Haiku/Sonnet + cache; Opus on escalation | Scale-to-zero (NextGen SL / S3 Vectors) | On-demand | ✅ now |
| Growth (hundreds/day) | Cascade + routing [S85] | OpenSearch Serverless (active) | On-demand + batch evals | ⚠️ when volume rises |
| High volume (sustained) | Routing; consider fine-tune only if evals justify | Provisioned OpenSearch | Provisioned throughput if steady-state | ⚠️ only with measured steady load |

**Recommended:** MVP posture; re-evaluate on measured volume, never on anticipation. Multi-agent
economics are unforgiving (~15× chat cost; single agents match multi-agent under equal token budgets
[S3]) — another reason to stay single-agent until a trigger fires
([02](02-agentic-ai-operating-model.md)).
