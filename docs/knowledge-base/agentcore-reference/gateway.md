# AgentCore Gateway — Verified Reference

**Topic:** Amazon Bedrock AgentCore Gateway — the managed AI gateway that exposes APIs, Lambda functions, MCP servers, other agents, and even LLM inference behind one secured endpoint (MCP + HTTP + inference routing).
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-supported-targets.html and gateway-targets-mcp.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
- https://aws.amazon.com/bedrock/agentcore/pricing/ and https://aws.amazon.com/bedrock/agentcore/faqs/
- https://github.com/awslabs/amazon-bedrock-agentcore-samples (local clone, `01-features/07-centralize-and-govern-your-ai-infrastructure/01-gateway`, `03-integrations/gateway`, `01-features/01-harness/01-advanced-examples/02-gateway-integration`)

**Related summit note(s):** [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md) — the summit note says what was announced; this note says how it works, verified.

## Verified facts (official docs)

### What it is
A fully managed gateway that is the **single entry point for agentic traffic** — broader than an MCP tool gateway ([gateway.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)). Three target categories ([gateway-supported-targets.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-supported-targets.html)):
- **MCP targets (aggregation mode):** the gateway acts as one virtual MCP server combining all attached targets into a single `tools/list`. Target types: **AWS Lambda functions** (+ tool schema), **Amazon API Gateway REST stages**, **OpenAPI schemas**, **Smithy models**, **existing MCP servers**, built-in templates from integration providers, and built-in connectors (1-click: Salesforce, Slack, Jira, Asana, Zendesk).
- **HTTP targets (passthrough):** traffic forwarded directly without aggregation/translation — this is how the gateway fronts **other agents (including A2A traffic)** and HTTP services.
- **Inference targets:** model-based routing of LLM requests across providers behind one unified endpoint — the samples name **Amazon Bedrock, OpenAI, Anthropic, and OpenAI-compatible services** as routable providers. **Claude relevance: confirmed** — Anthropic is an explicit inference-routing provider, and every doc/sample agent driving the gateway uses a Claude model on Bedrock.

Cross-cutting capabilities: OAuth security guard, MCP↔API/Lambda protocol translation, composition, **secure per-target credential exchange** (AgentCore Identity credential providers: OAuth, API key), **semantic tool search** (agents can use thousands of tools while keeping prompts small), serverless with built-in observability/auditing.

### API surface / entry points
- Control plane (`bedrock-agentcore-control`): `CreateGateway`, `UpdateGateway`, `GetGateway`, `ListGateways`, `DeleteGateway`, `CreateGatewayTarget`, `UpdateGatewayTarget`, `GetGatewayTarget`, `ListGatewayTargets`, `DeleteGatewayTarget`.
- CLI: `agentcore add gateway --name X --authorizer-type NONE|CUSTOM_JWT [--discovery-url ... --allowed-audience ...] --runtimes <agent>`, `agentcore add gateway-target --type lambda-function-arn --lambda-arn ... --tool-schema-file tools.json`, then `agentcore deploy` (CDK) ([gateway-quick-start.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html)).
- Data plane: agents connect as MCP clients (streamable HTTP) to `https://{gateway-id}.gateway.bedrock-agentcore.{region}.amazonaws.com/mcp`; JSON-RPC `tools/list` / `tools/call`; validate with a plain `curl` POST. Logs at `/aws/bedrock-agentcore/gateways/{id}`.
- Auth: **inbound** = IAM SigV4, custom JWT (any OIDC discovery URL, e.g., Cognito/Okta/Entra), or NONE (dev only); **outbound** = per-target credential providers. Docs position it as the only fully managed service with both ingress *and* egress auth. Fine-grained access control and deterministic **AgentCore Policy** (Cedar) rules can bound tool calls.
- Private connectivity: secure egress into customer VPCs to reach internal APIs, plus private access to the gateway itself (samples `03-private-connectivity`; FAQ confirms VPC support).

### Limits / quotas (defaults, mostly adjustable; [quotas page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html))
1,000 gateways/account; **100 targets/gateway; 1,000 tools/target**; invocation timeout 15 min; inline schema ≤ 1 MB (10 MB via S3); tool-call/tool-list rate 200 TPS (gateway and account level); 5,000 concurrent connections; search-based tool-call 25 transactions/min; max tool payload 6 MB; Web Search Tool 10 TPS; control-plane Create/Update/Delete ~5 TPS.

### Pricing ([pricing page](https://aws.amazon.com/bedrock/agentcore/pricing/))
- API invocations (`ListTools`, `InvokeTool`, `Ping`): **$0.005 per 1,000**.
- Search API: **$0.025 per 1,000** invocations.
- Tool indexing: **$0.02 per 100 tools indexed per month**.
- Identity token/API-key retrieval is free when used through Gateway.

### Region availability ([regions page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html))
Gateway is in **all 20 listed regions, including us-east-1 and sa-east-1 (São Paulo)** — the widest footprint of any AgentCore feature alongside Identity/Tools/Observability. No Mexico region.

## Implementation patterns (samples repo)

- [01-features/07-centralize-and-govern-your-ai-infrastructure/01-gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/07-centralize-and-govern-your-ai-infrastructure/01-gateway) — the main gateway lab (Python 3.12 + boto3, arm64 packaging via uv). Structured tutorials: `01-attach-targets` (HTTP mode, MCP mode, and **llm-inference routing across Bedrock/OpenAI/Anthropic**), `02-set-up-inbound-authorization`, `03-private-connectivity` (VPC in both directions), `04-advanced-concepts`. Viamericas reuse: `01-attach-targets/http` + `mcp` are the exact recipe for exposing our payments-status/FX/compliance APIs once behind one MCP URL; `03-private-connectivity` for reaching APIs that never leave our VPC.
- [01-features/01-harness/01-advanced-examples/02-gateway-integration](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/01-harness/01-advanced-examples/02-gateway-integration) — full lifecycle with direct boto3: create gateway (MCP protocol) → add an MCP target (Exa search) → wire it into a harness via `tools=[{type: "agentcore_gateway", gatewayArn: ...}]` → agent (**Claude Haiku 4.5**) discovers and calls tools. Reuse: shows the zero-code path from harness agents to gateway tools.
- [03-integrations/gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/gateway) — integration recipes: `agentcore-tool-search-plugin` (semantic tool search in agent frameworks), `bedrock-kb-auto-register` (auto-register Bedrock Knowledge Bases as gateway tools), `dynatrace` (observability integration). Reuse: KB auto-register pairs with the Managed Knowledge Base summit note for RAG-as-a-tool.
- [Gateway quick start](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html) agent example — Strands `MCPClient` over streamable HTTP + `BedrockModel("anthropic.claude-3-7-sonnet-20250219-v1:0")`, with a paginated `list_tools` helper. Reuse: drop-in client snippet for any of our MCP-capable agents (works the same from Claude Agent SDK MCP config, VS Code, or Claude Code — the docs call out the "one URL for all IDEs" pattern explicitly).

## Gaps vs. the summit slides

- **Slide: agent connects via `/mcp` to list/invoke/search tools — holds.** Endpoint format, `tools/list`/`tools/call`, and the separate search API (with its own pricing and 25/min quota) are all documented ([gateway-quick-start.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-quick-start.html), [quotas](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html)).
- **Slide: OpenAPI services and Lambda functions become tools — holds**, and docs add more MCP target types the slide didn't show: Smithy models, API Gateway REST stages, existing MCP servers, and built-in connectors ([gateway-targets-mcp.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-targets-mcp.html)).
- **Slide: "Internet search" as a target type — not supported as drawn.** The supported-targets page lists only MCP / HTTP / Inference categories with no internet-search target ([gateway-supported-targets.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-supported-targets.html)). Web search exists in AgentCore as a **built-in Web Search Tool** (its rate quota appears under Gateway quotas, 10 TPS), but it is not a gateway *target* you attach like the slide implied. Treat the slide's framing as simplified.
- **Slide: "AgentCore agents" as targets — holds in a different form.** Other agents are fronted via **HTTP passthrough targets (including A2A)**, not via the MCP aggregation path ([gateway.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html)).
- **Slide omission:** the slide predates (or omitted) **inference targets** — model-based routing of LLM traffic across Bedrock/OpenAI/Anthropic through the same gateway — now a documented third target category. This matters to us as a potential single choke point for Claude traffic governance.

## Open questions for our build plan

- **Semantic search quality** over a realistic catalog of our internal tools (naming/description conventions drive it) — needs a prototype; also the low default of 25 search-based tool-calls/min may need a quota increase for production.
- **Latency overhead** per tool call through the gateway vs. direct Lambda/API invocation — no published numbers; benchmark with our payments-status API.
- **Inference-target routing for Claude:** whether routing Claude through gateway inference targets (vs. calling Bedrock directly) adds value (unified auth/audit) or unacceptable latency for us — hands-on test; per-provider capability parity unverified.
- **JWT identity propagation end-to-end** (end user → agent → gateway → target credential exchange) matching the summit fintech case — build the `02-set-up-inbound-authorization` + `07-oauth` combo and verify claims reach the target audit logs.
- **Multi-tenancy isolation** patterns (one gateway per business unit vs. shared with policy) — docs describe both; cost/blast-radius tradeoff untested.
- Exact pricing attribution when a harness agent calls gateway tools (Runtime CPU + Gateway invocation + model tokens) — verify on a metered pilot.

Last verified: 2026-08-11
