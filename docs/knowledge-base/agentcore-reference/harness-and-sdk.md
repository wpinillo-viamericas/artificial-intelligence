# AgentCore Harness & SDK — Verified Reference

**Topic:** The managed agent harness in Amazon Bedrock AgentCore (declare model/tools/instructions as config, AWS runs the orchestration loop) plus the SDK/CLI tooling around it.
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-models.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
- https://aws.amazon.com/bedrock/agentcore/pricing/ and https://aws.amazon.com/bedrock/agentcore/faqs/
- https://github.com/aws/bedrock-agentcore-sdk-python
- https://github.com/awslabs/amazon-bedrock-agentcore-samples (local clone, `01-features/01-harness`)

**Related summit note(s):**
- [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md)
- [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agent-harness-anatomy.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agent-harness-anatomy.md)
- [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md)

— the summit notes say what was announced; this note says how it works, verified.

## Verified facts (official docs)

### What it is
A **managed orchestration loop** (powered by open-source [Strands Agents](https://strandsagents.com/)): you declare model, system prompt, tools, skills, memory, and limits as configuration; AgentCore provides the environment, compute, memory, identity, networking, and observability. Each harness is backed by a managed AgentCore Runtime; every session is stateful and runs in an **isolated microVM per session** with its own filesystem and shell. Changing the model or adding a tool is a config change (or a per-invocation override), not a redeploy ([harness.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html)).

### API surface — the "3 API calls" path
1. `CreateHarness` (control plane `bedrock-agentcore-control`; needs `--harness-name` + `--execution-role-arn`; optional `--system-prompt`, `--tools`).
2. `GetHarness` — poll until `status: READY` (~150 s observed in samples).
3. `InvokeHarness` (data plane `bedrock-agentcore`; `harnessArn`, `runtimeSessionId` **min 33 chars**, `messages`) — returns a stream (`messageStart`/`contentBlockDelta`/`messageStop`/`metadata`; `stopReason` values include `end_turn`, `tool_use`, `max_tokens`, `max_iterations_exceeded`, `timeout_exceeded`, `max_output_tokens_exceeded`).

Full set: `Create/Get/Update/Delete/ListHarness(es)`, `ListHarnessVersions`, `Create/Get/Update/Delete/ListHarnessEndpoint(s)` (immutable versions + named endpoints, instant rollback), `InvokeHarness`, and `InvokeAgentRuntimeCommand` (run shell commands on the session microVM, bypassing the agent loop). A Step Functions `InvokeHarness` state exists for pipeline embedding ([harness-get-started.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html)).

### Models — Claude support (FLAGGED)
- **Default model when none is specified: Anthropic Claude Sonnet 4.6 on Amazon Bedrock (`global.anthropic.claude-sonnet-4-6`)** ([harness-models.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-models.html)). We build on Claude — the harness's zero-config default is already our model family.
- Docs examples use `us.anthropic.claude-sonnet-4-5-20250514-v1:0` and `us.anthropic.claude-opus-4-5-20251101-v1:0` via `bedrockModelConfig`; Claude via the Anthropic API directly is reachable through `liteLlmModelConfig` (`anthropic/claude-sonnet-4-6` + `apiKeyArn` stored in AgentCore Identity's token vault — agent code never sees the raw key).
- Providers: Amazon Bedrock, OpenAI (direct or via Bedrock Mantle), Google Gemini, any LiteLLM-compatible provider. **Mid-session provider switching** with context carried over. API formats: `converse_stream` (default, required for Bedrock Guardrails), `responses`, `chat_completions`.
- Per-invocation overrides: `model`, `systemPrompt`, `tools`, `maxIterations`, `maxTokens`, `timeoutSeconds`, skills, allowed tools, actor ID — defaults stay intact.

### Tools, skills, environment
Tools: AgentCore Gateway, remote MCP servers, built-in Browser and Code Interpreter, built-in `shell` and `file_operations`; inline/client-side tools require your code (stream stops with `stopReason: tool_use`). Skills attach from Git, S3, or the curated AWS skills catalog. BYO container for custom dependencies; mount S3 Files or EFS for cross-session shared storage. Bedrock Guardrails apply via `guardrailConfig` in `bedrockModelConfig.additionalParams` (stop reason `guardrail_intervened`). Short- and long-term memory persist across sessions. Everything is traced through AgentCore Observability; Evaluations/Recommendations/A-B testing iterate on real traffic.

### Harness vs. Runtime ([harness-vs-runtime.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html))
Runtime = you write the loop (any framework) and host it; harness = AWS runs the Strands-powered loop from config. Harness does **not** support: choice of agent framework, bidirectional streaming, graph/workflow (non-loop) patterns, hooks. Escape hatch: **export the harness to Strands code** and run it on Runtime; **Claude Agent SDK export is "coming soon"** per the docs.

### SDK / CLI entry points
- **AgentCore CLI** (`npm install -g @aws/agentcore`, Node 20+; https://github.com/aws/agentcore-cli): `agentcore create` (project type "Harness", `--model-provider bedrock|open_ai|gemini|lite_llm`), `agentcore add harness --model-id ...`, `agentcore deploy` (CDK), `agentcore invoke --session-id ...`, `agentcore dev` (local server + browser agent inspector), `agentcore status`.
- **boto3:** control plane client `bedrock-agentcore-control`, data plane `bedrock-agentcore` (`invoke_harness`).
- **Python SDK** `bedrock-agentcore` (pip, Apache 2.0; `BedrockAgentCoreApp` + `@app.entrypoint`) is for Runtime-hosted custom agents, not required for the harness itself; a TypeScript SDK also exists.

### Limits, pricing, regions
- Quotas: harness is a logical resource — **all AgentCore Runtime quotas apply** (8 h max session / 15 min idle default, 100 MB payload, 2 vCPU/8 GB per session, 1 GB session storage, 1,000 TPS data plane; see runtime.md). Per-invocation cost controls: `maxIterations`, `timeoutSeconds`, `maxTokens`, truncation strategies ([quotas](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html)).
- Pricing: **no separate harness charge** — you pay for the underlying capabilities consumed (Runtime microVM CPU/memory, Memory, Gateway calls, model tokens) ([pricing](https://aws.amazon.com/bedrock/agentcore/pricing/)).
- Regions: **GA**; available in **us-east-1** and **sa-east-1 (São Paulo)** among 18 regions — Latin America is covered by São Paulo only; no Mexico region ([agentcore-regions.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html)).

## Implementation patterns (samples repo)

- [01-features/01-harness/00-getting-started](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/01-harness/00-getting-started) — the complete workflow in direct boto3: IAM execution role → `create_harness` → `invoke_harness` with **two different Claude models (Haiku 4.5 and Sonnet 4.6) in the same session** → `invoke_agent_runtime_command` for imperative shell access. Python, no framework. Viamericas reuse: the canonical pilot script; proves model-switching (cheap Haiku for triage, Sonnet for reasoning) on one session.
- [01-features/01-harness/01-advanced-examples](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/01-harness/01-advanced-examples) — one folder per capability: `02-gateway-integration` (harness + Gateway MCP target, Claude Haiku 4.5), `03-execution-limits` (cost caps), `04-mcp-integration`, `05-agent-skills`, `07-oauth` (JWT inbound + OAuth outbound), `14-s3-filesystem` (S3-mounted persistent workspace incl. an LLM wiki), `01-custom-containers`. Python/boto3. Reuse: `07-oauth` is our identity-propagation pattern for compliance-facing agents; `03-execution-limits` for spend guardrails.
- [01-features/01-harness/02-use-cases](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/01-harness/02-use-cases) — end-to-end apps: travel agent (browser tool), webapp visual testing, AWS builder agent (harness + AWS Skills), weather agent (gateway + guardrails + evals + observability). Reuse: `04-weather-agent` is the fullest "production checklist" example (tools + guardrails + evaluation + tracing in one script) to copy for an internal ops-triage pilot.
- [00-getting-started](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/00-getting-started) — CLI-first path (Strands + Claude Sonnet on Bedrock, `agentcore create/dev/deploy/invoke`), shows the graduation path from harness prototype to custom Runtime agent.

## Gaps vs. the summit slides

- **"Create an agent in 3 API calls": holds** — `CreateHarness` → `GetHarness` (poll READY) → `InvokeHarness` ([harness-get-started.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-get-started.html); samples README states it verbatim).
- **"Generally available": holds per the dev guide** ("AgentCore harness is available in GA across all regions shown here", [harness.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html)). Note: the [AgentCore FAQ](https://aws.amazon.com/bedrock/agentcore/faqs/) still describes the managed harness as "preview" — the FAQ appears stale; the dev guide + region table are the authoritative, newer statements.
- **"Use any model": holds with nuance** — any model on Bedrock, OpenAI, Gemini, or any **LiteLLM-compatible** provider (which covers the Anthropic API); it is not literally unrestricted ([harness-models.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-models.html)). Also, the *framework* is fixed (Strands-powered loop; no graph/workflow patterns, no hooks — [harness-vs-runtime.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-vs-runtime.html)).
- **Platform-overview slide items marked preview, confirmed as such in docs/regions:** AWS Agent Registry (limited regions: us-east-1, us-west-2, Ireland, Sydney, Tokyo), AgentCore payments (preview, 4 regions). "Insights (preview)" from the slide has no dedicated page found in the dev guide — treat as unverified.
- **Anatomy slide (8 harness capabilities): consistent** with the docs' harness definition (compute, sandbox, tool connections, filesystem, memory, identity, observability + knowledge via skills/memory); no contradiction.
- **"No orchestration code, no infra config": holds**, with the caveat that you still create an IAM execution role and (via CLI) a CDK deployment runs under the hood.

## Open questions for our build plan

- **Claude Agent SDK export** is "coming soon" (only Strands export ships today) — timeline unknown; matters because our existing agents are Claude Agent SDK-based. Watch [harness-export docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-export.html).
- **Per-session cost in practice:** harness sessions keep a stateful microVM (idle time free per pricing, but background processes bill) — measure a realistic multi-turn compliance-triage session.
- Which **Claude model IDs** (global vs. `us.` cross-region profiles) resolve from sa-east-1-hosted harnesses, and with what latency — hands-on test.
- **Inline/client-side tools** require our own code on both harness and Runtime — evaluate whether Gateway-registered tools fully replace them for our internal APIs.
- Harness **concurrency behavior under the 25 TPS new-session quota** for a customer-facing workload — load test before production sizing.
- FAQ vs. dev guide GA discrepancy (above) — confirm GA in the AWS console for our target regions before committing.

Last verified: 2026-08-11
