# AgentCore Runtime — Verified Reference

**Topic:** Amazon Bedrock AgentCore Runtime — the serverless (microVM) / EC2-backed (Instances) hosting environment for agent code and tool servers; deployment paths, API surface, limits, pricing.
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
- https://aws.amazon.com/bedrock/agentcore/pricing/
- https://aws.amazon.com/bedrock/agentcore/faqs/
- https://github.com/aws/bedrock-agentcore-sdk-python
- https://github.com/awslabs/amazon-bedrock-agentcore-samples (local clone, `01-features/02-host-your-agent`, `04-infrastructure-as-code`, `00-getting-started`, `05-blueprints`)

**Related summit note(s):** [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-runtime-deployment.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-runtime-deployment.md) — the summit note says what was announced; this note says how it works, verified.

## Verified facts (official docs)

### What it is
Secure, serverless, purpose-built hosting for AI agents or tool servers. Framework-agnostic (LangGraph, Strands, CrewAI, custom code) and model-agnostic — the docs explicitly name **Anthropic Claude** alongside Bedrock-hosted models, Google Gemini, and OpenAI ([agents-tools-runtime.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)). **Claude support: confirmed** — you bring your own agent loop and call any Claude model (Bedrock Converse or Anthropic API); Runtime does not restrict the model.

### Two compute types
- **microVMs (default, serverless):** one dedicated Firecracker-style microVM per user session with isolated CPU/memory/filesystem; the entire microVM is terminated and memory sanitized after the session — no cross-session contamination. Instant start, scale on demand, pay per use.
- **Instances:** AWS-managed EC2 in your own account. Persistent multi-day sessions (up to 14 days), GPU workloads, multiple collaborating agents on one shared instance. See `runtime-instances` in the dev guide.

### Deployment options
- **Container:** ARM64 (Graviton) Docker image → Amazon ECR → `CreateAgentRuntime`. Only ARM64 images work. Max image size 2 GB.
- **Direct code deployment (zip):** code + pre-compiled `aarch64` wheels zipped → S3 → `CreateAgentRuntime`. Max 250 MB compressed / 750 MB uncompressed. No Docker required.
- **AgentCore CLI (`npm install -g @aws/agentcore`, Node 20+):** `agentcore create` (flags: `--framework Strands|LangChain_LangGraph|GoogleADK|OpenAIAgents`, `--protocol HTTP|MCP|A2A`, `--build CodeZip|Container`, `--model-provider Bedrock|Anthropic|OpenAI|Gemini` — note `Anthropic` is a first-class provider option), `agentcore dev` (local server, agent inspector), `agentcore deploy` (CDK/CloudFormation), `agentcore invoke`, `agentcore logs`, `agentcore traces`, `agentcore status`, `agentcore remove all`. Requires AWS CDK bootstrapped.
- **Python SDK (`pip install bedrock-agentcore`, Apache 2.0):** `BedrockAgentCoreApp` + `@app.entrypoint` decorator wraps any local agent for Runtime's HTTP contract (`POST /invocations` port 8080). A TypeScript SDK also exists (`bedrock-agentcore-sdk-typescript`).

### API surface
- **Control plane (`bedrock-agentcore-control`):** `CreateAgentRuntime`, `CreateAgentRuntimeEndpoint`, `UpdateAgentRuntime`, `UpdateAgentRuntimeEndpoint`, `DeleteAgentRuntime`, `DeleteAgentRuntimeEndpoint`, `Get*`, `List*` (runtimes, endpoints, versions). Immutable versions + named endpoints (aliases, `qualifier="DEFAULT"`).
- **Data plane (`bedrock-agentcore`):** `InvokeAgentRuntime` (payload + `runtimeSessionId`, min 33 chars), `InvokeAgentRuntimeCommand` (direct shell execution, command 1 B–64 KB, timeout 1–3600 s), `InvokeAgentRuntimeWithWebSocketStream`, `StopRuntimeSession`, `GetAgentCard` (A2A).
- **Protocols served:** HTTP, MCP (`POST /mcp` port 8000, deploy MCP tool servers), A2A (agent card), AG-UI; response streaming and bidirectional WebSocket streaming.

### Limits / quotas (defaults; [quotas page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html))
- Max payload 100 MB (not adjustable); streaming chunk 10 MB; WebSocket frame 64 KB.
- Sync request timeout 15 min; streaming connection max 60 min; async job max 8 h.
- Session lifecycle: idle timeout default 15 min (adjustable 60 s–28,800 s via `LifecycleConfiguration.idleRuntimeSessionTimeout`); max session duration 8 h (`maxLifetime`). Instances: up to 14 days.
- Hardware cap per microVM session: 2 vCPU / 8 GB. Session storage 1 GB.
- Active session workloads per account: 5,000 (us-east-1, us-west-2), 2,500 elsewhere — adjustable. 1,000 agents/account, 1,000 versions/agent, 10 endpoints/agent.
- Throttling: data-plane 1,000 TPS shared across invoke APIs (adjustable); new session creation 25 TPS; control-plane mutations 50 TPS.

### Pricing ([pricing page](https://aws.amazon.com/bedrock/agentcore/pricing/))
- microVMs: **$0.0895 per vCPU-hour + $0.00945 per GB-hour**, 1-second billing increments, 128 MB minimum memory. CPU billed on actual active processing — **I/O wait / idle time is free** if no background process runs (i.e., waiting on Claude responses is largely unbilled CPU).
- Instances: EC2 On-Demand rate + 12% management fee (7.8% for G-series GPU), ~1-minute minimum.
- No charge to create runtimes; consumption-based, no minimum commitment.

### Region availability ([regions page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html))
- Runtime **microVMs: 20 regions including us-east-1 (N. Virginia) and sa-east-1 (São Paulo)** — the only Latin America region listed. **No Mexico (mx-central-1) availability.**
- Runtime **Instances: NOT in sa-east-1** (us-east-1/us-east-2/us-west-2, Frankfurt, Ireland, Mumbai, Singapore, Sydney, Tokyo only).
- Compliance (FAQ): HIPAA eligible; validated against ISO 27001/27017/27018/27701, **PCI**, SOC; FedRAMP in progress. VPC connectivity supported across Runtime, Memory, Gateway, tools, Identity, Observability — relevant for our payments-data workloads.

### Other verified capabilities
Persistent filesystems across session stop/resume (plus S3 Files / EFS mounts); built-in agent tracing (OpenTelemetry → CloudWatch); inbound auth via IAM SigV4 or OAuth/JWT (AgentCore Identity; Okta / Entra ID / Cognito), outbound OAuth/API-key flows; OAuth-integrated agents must be invoked via HTTPS request, not the AWS SDK.

## Implementation patterns (samples repo)

- [01-features/02-host-your-agent/01-runtime](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/02-host-your-agent/01-runtime) — the canonical hosting samples. Python (boto3), three-script pattern per sample (`deploy.py` → zip + S3 + `create_agent_runtime()`; `invoke.py`; `cleanup.py`), organized by protocol (HTTP/MCP/A2A/AG-UI) and framework (Strands, LangGraph, CrewAI, Java, TypeScript). Viamericas reuse: the deploy scripts show every IAM/S3/runtime parameter explicitly — the template for our CI/CD path off the CLI.
- [01-features/02-host-your-agent/01-runtime/04-coding-agents](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/02-host-your-agent/01-runtime/04-coding-agents) — **Claude Code on AgentCore Runtime** with persistent S3 Files or EFS filesystems, plus a Claude Managed Agents self-hosted sandbox sample. Directly relevant since we build on Claude: this is the documented pattern for running Claude-based coding/ops agents with durable workspaces.
- [00-getting-started](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/00-getting-started) — customer-support agent (Strands + **Claude Sonnet on Bedrock**) built entirely with the AgentCore CLI: create → local dev → deploy → invoke in ~10 min. Viamericas reuse: fastest onboarding path for a first deployed agent; the tool-definition style (`@tool` + docstrings) maps to our FX-rate/payment-status lookups.
- [04-infrastructure-as-code](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/04-infrastructure-as-code) — CloudFormation, CDK (Python/TS), and Terraform for: basic runtime (ECR + Docker build + least-privilege IAM), MCP server on Runtime with Cognito JWT, multi-agent (orchestrator → specialist) runtimes, and an end-to-end weather agent (Browser + Code Interpreter + Memory). Viamericas reuse: the Terraform/CDK multi-agent sample is our IaC starting point for the AML/approval/anomaly subagent architecture from the summit business case.
- [05-blueprints/end-to-end-customer-service-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/end-to-end-customer-service-agent) and [05-blueprints/multitenant-agentic-platform](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/multitenant-agentic-platform) — full-stack blueprints (backend + frontend + infra + offline evaluation). Reuse: reference architectures for a production customer-service agent and for tenant isolation if we serve multiple business units from one platform.

## Gaps vs. the summit slides

- **Slide claim "Docker image → ECR or Zip → S3": holds.** Both paths verified ([runtime-get-started-cli.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html), build types `Container` and `CodeZip`), with the added constraint the slide omitted: **ARM64/Graviton only**, image ≤ 2 GB, zip ≤ 250 MB compressed.
- **Slide claim "any model + any framework + decorator": holds** ([agents-tools-runtime.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)); the "decorator" is `BedrockAgentCoreApp`/`@app.entrypoint` from the `bedrock-agentcore` Python SDK.
- **Slide omission (not a contradiction):** the slide showed only the serverless path; docs now also document the **Instances** compute type (EC2-backed, 14-day sessions, GPU) — and Instances are *not* available in sa-east-1 ([agentcore-regions.html](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html)).
- **Slide flow "configure → launch → endpoint": holds** — maps to `CreateAgentRuntime` → `CreateAgentRuntimeEndpoint` → `InvokeAgentRuntime` (samples repo deploy scripts and API reference).

## Open questions for our build plan

- **Real cost per conversation** with Claude-backed agents: the "I/O wait is free" claim means CPU cost should be small vs. model tokens, but needs a measured pilot (deploy the 00-getting-started agent, run a realistic transcript, read the meter).
- **VPC specifics:** FAQ confirms VPC connectivity, but subnet/SG design, PrivateLink endpoints, and latency from VPC-attached runtimes to internal payment APIs need a hands-on test (samples `03-advanced` covers VPC; not yet validated by us).
- **Latency:** microVM cold-start and per-invoke overhead vs. our current Lambda/ECS serving — no official numbers published; benchmark required.
- **sa-east-1 depth:** Runtime microVMs are in São Paulo, but which *Claude models* are available in Bedrock sa-east-1 (vs. cross-region inference profiles from us-east-1) is a Bedrock-model-catalog question, not answered by AgentCore docs.
- **Data residency/PCI scoping** when the agent runs in us-east-1 but touches remittance data — needs compliance review; AgentCore is PCI-validated per FAQ but our workload scoping is ours to prove.
- Anthropic-direct (`--model-provider Anthropic`, API key) vs. Claude-on-Bedrock from Runtime: functional parity and egress implications untested.

Last verified: 2026-08-11
