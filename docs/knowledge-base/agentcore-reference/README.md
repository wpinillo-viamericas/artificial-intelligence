# AgentCore Reference Layer

Living, topic-based deep-dive notes on Amazon Bedrock AgentCore, verified against official AWS documentation, the [amazon-bedrock-agentcore-samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples) repo, and the AWS MCP catalogs. Each note expands one or more snapshot notes from [../aws-summit-2026/](../aws-summit-2026/README.md): the summit note says *what was announced*; the reference note says *how it works, verified* — including limits, pricing, region availability, Claude support, and explicit gaps versus the slides. Re-verify any note whose `Last verified:` date has gone stale.

## Index

| Topic | Related summit note | Key sources | Last verified |
|---|---|---|---|
| [runtime.md](./runtime.md) — hosting, deploy paths, quotas, pricing | [agentcore-runtime-deployment](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-runtime-deployment.md) | devguide (runtime, limits, regions), pricing, samples `02-host-your-agent` | 2026-08-11 |
| [harness-and-sdk.md](./harness-and-sdk.md) — managed loop, 3-API-call path, CLI/SDK | [agentcore-harness-launch](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md), [agent-harness-anatomy](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agent-harness-anatomy.md) | devguide (harness, harness-models, harness-vs-runtime), samples `01-harness` | 2026-08-11 |
| [gateway.md](./gateway.md) — MCP/HTTP/inference targets, auth, quotas | [agentcore-gateway-mcp](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md) | devguide (gateway, targets, limits), samples `07-.../01-gateway` | 2026-08-11 |
| [memory.md](./memory.md) — strategies, extraction, namespace isolation | [agentcore-memory](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-memory.md) | devguide (memory, strategies, organization, limits), pricing | 2026-08-11 |
| [identity-and-guardrails.md](./identity-and-guardrails.md) — inbound/outbound auth, JWT propagation, Cedar Policy | [agentcore-fintech-orchestration-case](../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md), [platform-overview](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md) | devguide (identity, runtime-oauth, policy), whats-new, samples `05-authenticate-and-authorize` | 2026-08-11 |
| [observability-and-evals.md](./observability-and-evals.md) — OTEL→CloudWatch, evaluators, preview Optimization | [agentcore-fintech-orchestration-case](../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md), [platform-overview](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md) | devguide (observability, evaluations, evaluators), samples `06-observe-evaluate-optimize` | 2026-08-11 |
| [knowledge-base-rag.md](./knowledge-base-rag.md) — Managed KB, SharePoint/OneDrive connectors, agentic retrieval | [bedrock-managed-knowledge-base](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-managed-knowledge-base.md) | Bedrock userguide (kb-managed-*), AgentCore KB gateway target, GA announcement | 2026-08-11 |
| [mcp-tooling.md](./mcp-tooling.md) — dev-time MCP servers + Claude Code registration snippets | [agentcore-gateway-mcp](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md) | awslabs.github.io/mcp, agent-toolkit userguide, AgentCore mcp-getting-started | 2026-08-11 |
| [learning-path.md](./learning-path.md) — ordered hands-on onboarding (11 steps + capstones) | [agentcore-harness-launch](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md), [fintech case](../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md) | get-started CLI docs, samples `06-workshops` (13 modules), hosted workshops | 2026-08-11 |

## Highlights for our build plan (cross-note)

- **Regions:** us-east-1 has every feature. São Paulo (sa-east-1) covers the core platform — harness, Runtime microVMs, Memory, Gateway, Identity, Observability, Policy, Evaluations, optimization — but **not** Runtime Instances, payments, or Agent Registry, and **Managed Knowledge Base has no LatAm region at all**. No Mexico region anywhere.
- **Claude:** first-class everywhere checked — the harness's zero-config default model is Claude Sonnet 4.6; the CLI treats Anthropic as a named provider; official samples run Claude throughout.
- **Slide corrections worth remembering:** "Guardrails" on the platform slide is Bedrock Guardrails (not an AgentCore component); Gateway "web search" is a built-in tool, not a target; the fintech case's JWT-per-agent pattern requires deliberate engineering (RFC 8693 token attenuation), and its "self-reflection to Slack" was customer-built, not platform.
- **Non-adjustable quotas that shape design:** Memory `CreateEvent` 5 TPS per actor+session; Policy Cedar schema 400 KB per engine; Runtime 2 vCPU/8 GB per microVM session; ARM64-only deployments.

## Conventions

One note per topic, kebab-case. Header links the related summit note(s); every fact cites an official URL; unverifiable claims live under "Open questions", never as fact; notes end with `Last verified: <date>`. When re-verifying, update the date here and in the note.
