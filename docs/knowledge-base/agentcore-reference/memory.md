# AgentCore Memory — Verified Reference

**Topic:** How Amazon Bedrock AgentCore Memory actually works: short-term events, long-term extraction strategies, APIs, isolation, limits, pricing.
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-get-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-strategies.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-strategies.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-custom-strategy.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-capacity.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-organization.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html
- https://aws.amazon.com/bedrock/agentcore/pricing/
- https://aws.amazon.com/bedrock/agentcore/faqs/
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-four-additional-regions/

**Related summit note(s):** [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-memory.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-memory.md) — the summit note says what was announced; this note says how it works, verified.

## Verified facts (official docs)

**Status:** Memory is **GA** (FAQ lists it among generally available components).

**Model.** A *memory* resource holds two layers:
- **Short-term memory** = raw **events** (conversation turns, checkpoints) written per `actorId` + `sessionId` via the data-plane `CreateEvent` operation. Retrieved with short-term operations (e.g., last-k turns).
- **Long-term memory** = **memory records** extracted asynchronously from events by **memory strategies** configured on the memory resource. **No strategies configured → no long-term records are ever extracted.** Records are retrieved by listing or by vector/semantic search (`RetrieveMemoryRecords`).

**Strategies** (devguide/memory-strategies.html, built-in-strategies.html):
- **Built-in:** `SEMANTIC` (facts), `USER_PREFERENCE`, `SUMMARY`, `EPISODIC`. Fully AWS-managed extraction/consolidation ("Reflection" step exists for episodic — insights across episodes). No model or prompt configuration; highest storage price.
- **Built-in with overrides:** same pipeline, but you override the instruction portion of the extraction/consolidation (and reflection, for episodic) system prompts (`appendToPrompt`) and **choose the Amazon Bedrock foundation model** used for those LLM calls. Requires `memoryExecutionRoleArn` in `CreateMemory`/`UpdateMemory`; the service assumes that role and **invokes the model in your account** — the LLM usage bills to you and consumes your Bedrock quotas (throttling can fail ingestion; enable log delivery to see errors). Output schema is not editable; do not rename consolidation ops (`AddMemory`/`UpdateMemory`).
- **Self-managed:** you own the whole extraction/consolidation pipeline (any model, any schema, any namespace); cheapest record storage.
A single memory resource can mix strategy types.

**Claude support (flagged):** For pure built-in strategies the docs do **not** disclose which foundation model performs extraction (AWS-managed, service side). For **built-in with overrides** and **self-managed**, you pick any Bedrock model you have access to — **Anthropic Claude models are fully usable** (the observability getting-started and multiple official samples use `us.anthropic.claude-3-7-sonnet-20250219-v1:0` and Claude Haiku 4.5). Model selection is explicitly a stated reason to use overrides (e.g., a model suited to financial/legal text — directly relevant to us).

**Organization & multi-tenant isolation** (memory-organization.html):
- Events keyed by `actorId` + `sessionId`.
- Long-term records live under hierarchical **namespaces** with variables: e.g. `/strategy/{memoryStrategyId}/actor/{actorId}/session/{sessionId}/`. Use a **trailing slash** to prevent prefix collisions in multi-tenant apps (`/actors/Alice/` not `/actors/Alice`).
- **IAM condition keys** `bedrock-agentcore:namespace` and `bedrock-agentcore:namespacePath` can restrict `RetrieveMemoryRecords` to a namespace or subtree — this is the documented mechanism for hard, policy-enforced client-scoped memory (key for our compliance model).

**API surface / entry points:**
- Control plane (`boto3.client('bedrock-agentcore-control')`): `CreateMemory`, `UpdateMemory`, `ListMemories`, delete. API ref: https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/
- Data plane (`boto3.client('bedrock-agentcore')`): `CreateEvent`, list events, `RetrieveMemoryRecords`, list memory records. API ref: https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/
- Python SDK `bedrock-agentcore` (pip): `MemorySessionManager` → `create_memory_session(actor_id, session_id)`, `add_turns()`, `get_last_k_turns()`, `list_long_term_memory_records()`, `search_long_term_memories(query, namespace_path, top_k)`. Strands integration: `AgentCoreMemorySessionManager` + `RetrievalConfig` (per-namespace `top_k` and `relevance_score`).
- AgentCore CLI (npm `@aws/agentcore`, needs Node 18+): `agentcore add memory --name X --strategies SEMANTIC,SUMMARIZATION`, `agentcore deploy`, `agentcore status`. Deployed agents get env var `MEMORY_<NAME>_ID` automatically.

**Limits / quotas** ([quotas page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html), defaults; "adj" = adjustable via Service Quotas):
- Resources: 150 memory resources per account/region (adj); **6 strategies max per memory resource**; 900 strategies per account (adj).
- Events: `CreateEvent` 200 TPS per account (adj), but only **5 TPS per actor+session** with conversational payloads (10 TPS without, both non-adjustable); ≤100 messages per event, ≤100 KB per message, ≤10 MB per event; event retention (`EventExpirationDuration`) 7–365 days.
- Retrieval: `RetrieveMemoryRecords` and `ListMemoryRecords` 30 TPS each (adj); `ListEvents` 200 TPS (adj).
- Extraction throughput: **150,000 tokens/min for built-in long-term extraction** per account (adj; monitor `TokenCount` metric in the `Bedrock-AgentCore` namespace); episodic extraction capped at 50,000 tokens/min per session (non-adjustable). Custom-strategy `appendToPrompt` ≤ 30 KB.

**Pricing** (aws.amazon.com/bedrock/agentcore/pricing/): short-term events **$0.25 per 1,000 new events**; long-term storage **$0.75 per 1,000 records/month (built-in strategies)** vs **$0.25 per 1,000 records/month (self-managed)**; retrievals **$0.50 per 1,000 record retrievals**. Overrides additionally bill the Bedrock model calls in your account.

**Regions:** FAQ (accessed 2026-08-11) lists AgentCore in 15 regions including **us-east-1 (N. Virginia)**, us-east-2, us-west-2, and — the only Latin America region — **sa-east-1 (São Paulo)**. Four more regions (Bangkok, Malaysia, Milan, Spain) were announced June 2026. For Viamericas: memory works in both us-east-1 and São Paulo.

**Other verified details:** extraction runs asynchronously after events are written (docs say analysis happens after `CreateEvent`; the samples repo states extraction typically takes ~1 minute — samples claim, not a doc SLA). Memory emits built-in CloudWatch metrics and optional spans/logs (see observability note). Advanced features documented: memory record streaming, cross-account memory access, event branching.

## Implementation patterns (samples repo)

- **Memory feature samples** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/04-manage-context-of-your-agent/memory — Python; folders `00-getting-started` → `06-production-patterns` covering short-term, long-term, integrations, observability, security, production patterns. The canonical code the docs link to; our starting point for a memory PoC.
- **Memory workshop** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/04-AgentCore-memory — Python; short-term memory with **Strands, LangGraph, LlamaIndex** (incl. checkpointing and human-in-the-loop), long-term strategies, advanced patterns, **memory branching**. Confirms the five strategy types (`SEMANTIC, SUMMARY, USER_PREFERENCES, EPISODIC, SELF_MANAGED`). We'd reuse the Strands + long-term pattern.
- **Memory security patterns** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/04-AgentCore-memory/05-memory-security-patterns — IAM policies scoped to memory namespaces and Cognito-identity-based scoping (`01-memory-iam-policies`, `02-memory-iam-cognito-identities`). This is the sample that operationalizes "each client sees only its own memory" — the most compliance-relevant one for us.

## Gaps vs. the summit slides

The summit note's claims **hold**: events → short-term; asynchronous automatic extraction ("built-in or self-managed") → long-term; taxonomy of summaries/preferences/facts/episodes maps 1:1 to the built-in `SUMMARY`/`USER_PREFERENCE`/`SEMANTIC`/`EPISODIC` strategies (https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-strategies.html). Two refinements the slide didn't show:
- There is a **third tier**, "built-in with overrides" (custom prompt + your choice of Bedrock model, billed to your account) between built-in and self-managed (https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-custom-strategy.html).
- Extraction is not free-floating "automatic": it happens **only if strategies are configured** on the memory resource (https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-strategies.html).

## Open questions for our build plan

- Which foundation model AWS uses for **pure built-in** strategy extraction is not documented — if model provenance matters for compliance, use overrides with a pinned Claude model and test extraction quality on remittance-domain Spanish/English conversations.
- Actual end-to-end extraction latency under load (samples say ~1 min; no documented SLA) — measure before relying on long-term memory within the same session.
- The **5 TPS per actor+session `CreateEvent`** cap is non-adjustable — verify our chattiest agent flows (multi-tool loops writing every turn) stay under it, or batch turns per event.
- Verify `bedrock-agentcore:namespace`/`namespacePath` IAM conditions behave as expected when namespaces are templated with `{actorId}` (multi-tenant test with two Cognito identities — sample 05-memory-security-patterns is the harness).
- PII in raw events: what redaction we must apply before `CreateEvent` (memory stores verbatim turns); confirm KMS/CMK encryption options for the memory resource.

Last verified: 2026-08-11
