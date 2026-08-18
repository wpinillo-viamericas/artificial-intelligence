# AWS Summit Bogotá 2026 — Knowledge Repository

Slides and diagrams photographed at **AWS Summit Bogotá 2026** (July 30, 2026, Agora Bogotá Convention Center), curated for Viamericas' AI initiatives. Each photo has a companion Markdown note with a transcription of the key content and why it matters to us. Dominant theme of the event: **Amazon Bedrock AgentCore** — running agents in production.

## Index

| Photo | Category | Topic | Summary |
|---|---|---|---|
| [bedrock-agentcore-platform-overview](./genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md) | genai-architectures | AgentCore platform overview | The full modular stack for production agents: harness, context, tools, optimization, runtime, and platform control. |
| [agent-harness-anatomy](./genai-architectures/2026-07-30_genai-architectures_agent-harness-anatomy.md) | genai-architectures | Anatomy of an agent | Conceptual model: an agent = model + harness (identity, data, observability, sandbox, knowledge base, compute, tools, memory). |
| [agentcore-runtime-deployment](./genai-architectures/2026-07-30_genai-architectures_agentcore-runtime-deployment.md) | genai-architectures | AgentCore Runtime deployment | Any model/framework + decorator, packaged as Docker→ECR or Zip→S3, launched as a managed runtime agent with an endpoint. |
| [agentcore-memory](./genai-architectures/2026-07-30_genai-architectures_agentcore-memory.md) | genai-architectures | AgentCore Memory | Short-term event memory with async automatic extraction into long-term summaries, preferences, facts, and episodes. |
| [agentcore-gateway-mcp](./genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md) | genai-architectures | AgentCore Gateway (MCP) | One MCP endpoint that turns OpenAPI services, Lambda functions, web search, and other agents into callable tools. |
| [bedrock-managed-knowledge-base](./genai-architectures/2026-07-30_genai-architectures_bedrock-managed-knowledge-base.md) | genai-architectures | Managed Knowledge Base (GA) | Fully managed RAG with native S3/SharePoint/Confluence/Drive/OneDrive connectors and multi-step agentic retrieval. |
| [agentcore-harness-launch](./genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md) | genai-architectures | AgentCore harness (GA) | Create a working agent in 3 API calls — no orchestration code or infrastructure, any model. |
| [aws-context-announcement](./data-platform/2026-07-30_data-platform_aws-context-announcement.md) | data-platform | AWS Context (coming soon) | Self-learning knowledge graph over structured/unstructured data, Iceberg-native, integrated with Glue Data Catalog and SageMaker Unified Studio. |
| [agentcore-fintech-orchestration-case](./business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md) | business-cases | Fintech multi-agent case | Payments company running AML, approval, and anomaly subagents on AgentCore with JWT identity propagation — the closest match to our domain. |

## Deep-dive reference

These notes are an immutable snapshot of what was presented. For verified, up-to-date technical detail on each topic (official docs, sample code, limits, pricing, gaps vs. these slides), see the living reference layer: [../agentcore-reference/](../agentcore-reference/README.md).

## Conventions (for adding future events)

- Folder per event: `docs/knowledge-base/<event>-<year>/`
- Categories: `genai-architectures/`, `data-platform/`, `mlops-deployment/`, `security-compliance/`, `business-cases/` (create on demand)
- Files: `YYYY-MM-DD_<category>_<kebab-topic>.jpg` + companion `.md` with the same base name
- Note format: title, source, category, AWS services, key takeaways (transcription), relevance to Viamericas, embedded image
