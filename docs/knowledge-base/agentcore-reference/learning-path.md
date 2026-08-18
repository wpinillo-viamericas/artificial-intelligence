# AgentCore Hands-On Learning Path (Tech Lead Onboarding)

**Topic:** Ordered, hands-on onboarding through the AgentCore CLI, the official samples repo, and the 13 workshop modules — sequenced for Viamericas' adoption (Claude on Bedrock, payments/remittance domain).
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html
- https://github.com/awslabs/amazon-bedrock-agentcore-samples (local clone at commit `0082e84`, 2026-08-09; README, 00-getting-started, 06-workshops/\*, 01-features/08, 05-blueprints/\*)
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
- https://catalog.workshops.aws/agentcore-getting-started/en-US
- https://catalog.workshops.aws/agentcore-deep-dive/en-US
- https://catalog.us-east-1.prod.workshops.aws/workshops/2ab3895e-8b7c-4f5c-b0c7-8597d6954290/en-US (Claude Agent SDK + AgentCore)

**Related summit note(s):** [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-harness-launch.md), [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md), [../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md](../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md) — the summit notes say what was announced; this note is the verified path to build it ourselves.

## Verified facts (official docs)

- **Two build paths, one CLI** ([get-started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html)): **managed harness** (declare model/prompt/tools/memory in config, AgentCore runs the loop) or **code-based agent** (Strands, LangChain/LangGraph, Google ADK, or OpenAI Agents SDK on AgentCore Runtime). CLI: `npm install -g @aws/agentcore`, then `agentcore create` → `agentcore dev` (local server + browser agent inspector) → `agentcore deploy` (CDK under the hood, CodeZip default or Container) → `agentcore invoke`. Add-ons: `agentcore add memory|gateway|credential|evaluator|payment-manager|payment-connector`. Logs/traces: `agentcore logs`, `agentcore traces`. Cleanup: `agentcore remove all && agentcore deploy`.
- **Prerequisites** (docs + samples README): AWS account with credentials, Node.js 20+, Python 3.10+, `uv`, IAM permissions for AgentCore APIs + CDK bootstrap roles; samples repo recommends `BedrockAgentCoreFullAccess` + `AmazonBedrockFullAccess` and **Anthropic Claude model access enabled in the Bedrock console** ("Claude 4.0" per the repo README). **Claude is the default model** in the CLI scaffold (`model/load.py` defaults to Claude Sonnet on Bedrock) and the wizard also accepts Anthropic (direct API), OpenAI, Gemini providers — Claude support flagged: first-class throughout.
- **Regions** ([agentcore-regions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html)): **us-east-1 supports every feature** (harness, Runtime, Memory, Gateway, Identity, built-in tools, Observability, Policy, Evaluations, optimization, Agent Registry, and payments preview). **sa-east-1 (São Paulo)** now has most features (harness, Runtime microVMs, Memory, Gateway, Identity, tools, Observability, Policy, Evaluations, optimization) but **not payments or Agent Registry**, and note the Managed Knowledge Base is **not** in sa-east-1. Standardize training and dev on **us-east-1**.
- **Cost/preview flags:** AgentCore payments is **preview**, testnet-only samples (Base Sepolia / Solana Devnet USDC, no real funds; one use case runs Base **mainnet** — real USDC). Every workshop notebook has cleanup cells; harness README warns explicitly to delete resources to avoid charges.
- **Official hosted workshops (verified to exist via search; content not fetched — the catalog is JS-rendered):**
  - Getting started with AgentCore (official): https://catalog.workshops.aws/agentcore-getting-started/en-US
  - Diving Deep into Bedrock AgentCore (official): https://catalog.workshops.aws/agentcore-deep-dive/en-US
  - Agentic AI with **Claude Agent SDK** + AgentCore: https://catalog.us-east-1.prod.workshops.aws/workshops/2ab3895e-8b7c-4f5c-b0c7-8597d6954290/en-US — most relevant to our Claude-first stack.
  - The samples-repo `06-workshops/` folder remains the canonical self-paced path; the hosted workshops mirror it.

## The ordered path

Times marked *(est.)* are my estimates; READMEs rarely state durations. Assume us-east-1, Claude model access enabled, and an isolated sandbox account.

**Phase 0 — Environment (once, ~1 h est.)**
AWS sandbox account; `aws configure`; Node 20+, Python 3.10+, `uv`, Jupyter; attach `BedrockAgentCoreFullAccess` + `AmazonBedrockFullAccess`; enable Claude model access in the Bedrock console; `npm install -g @aws/agentcore`.

**Step 1 — CLI quickstart (docs) — ~30–45 min (est.)**
Follow [agentcore-get-started-cli](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html): scaffold a Strands + Bedrock (Claude) agent, `agentcore dev` with the inspector, `agentcore deploy`, `agentcore invoke`, then `agentcore remove all && agentcore deploy` to tear down. You build: the full local→cloud loop. Cost: minutes of Claude inference + trivial infra; first deploy CDK-bootstraps the account.

**Step 2 — [00-getting-started](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/00-getting-started) — "under 10 minutes" (stated), plan ~30 min with reading**
Customer support agent with custom tools (product lookup, return policy) on Claude Sonnet via Bedrock, run locally then deployed. You build: your first tool-using agent and the project anatomy (`agentcore.json`, `app/`, CDK).

**Step 3 — Harness quickstart: [06-workshops/11-AgentCore-harness](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/11-AgentCore-harness) — ~1–2 h (est.)**
The GA "agent in 3 API calls" from the summit slide, via CLI and boto3 notebook. You build: a config-declared agent with no orchestration code; also covers the `HarnessExecutionRole` IAM pattern (model invocation, ECR, X-Ray, CloudWatch, `bedrock-agentcore:*` features). Prereq: Step 1. Justifies its position: fastest mental model of "model + harness" before touching code-based runtime; cleanup script included.

**Step 4 — [06-workshops/01-AgentCore-runtime](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/01-AgentCore-runtime) — ~2–3 h (est.)**
Hosting agents, **hosting MCP servers**, advanced concepts (streaming). You build: a code-based agent (`@app.entrypoint`) and an MCP server on Runtime. This is where framework choice (Strands vs LangGraph) becomes concrete.

**Step 5 — [06-workshops/02-AgentCore-gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/02-AgentCore-gateway) — ~2–3 h (est.)**
Lambda and OpenAPI/Smithy targets, inbound/outbound auth, semantic tool search. Tutorial uses Strands + **Claude Haiku 4.5** / Nova Pro, boto3. You build: our core integration pattern — internal APIs (payment status, compliance checks, FX rates) as MCP tools registered once. Directly validates the summit Gateway slide.

**Step 6 — [06-workshops/04-AgentCore-memory](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/04-AgentCore-memory) — ~2–3 h (est.)**
Short-term (session/checkpointing) and long-term memory with SEMANTIC / SUMMARY / USER_PREFERENCES / EPISODIC / SELF_MANAGED strategies; extraction runs ~1 min in background. You build: a personalized agent; single- and multi-agent memory. Placed before identity because memory namespaces per user make the identity module's "on behalf of user" concepts tangible.

**Step 7 — [06-workshops/03-AgentCore-identity](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/03-AgentCore-identity) — ~2–3 h (est.)**
Inbound auth (IAM/OAuth), outbound auth (2LO/3LO), workload token exchange — "delegation rather than impersonation". You build: Cognito/Entra-backed auth flows. Critical for us: the summit fintech case propagated JWT identity through subagents; this is that mechanism. Pairs with the Entra per-user delegation integration sample.

**Step 8 — Observability + Evaluations: [06](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/06-AgentCore-observability) & [07](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/07-AgentCore-evaluations) — ~3 h combined (est.)**
OTel traces to CloudWatch (runtime-hosted and self-hosted agents; partner backends Arize/Braintrust/Langfuse exist under 03-integrations), then the 13 built-in evaluators + custom evaluators, on-demand and online (sampled) evaluation. You build: the monitoring/quality loop we need before anything customer-facing.

**Step 9 — [06-workshops/08-AgentCore-policy](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/08-AgentCore-policy) — ~1–2 h (est.)**
Cedar policies on Gateway tool calls; the getting-started demo is an **insurance underwriting** system ("only allow applications under $1M") — directly analogous to remittance amount/corridor limits. Requires boto3 ≥ 1.42.0. Inserted before E2E because the E2E labs use Policy.

**Step 10 — Capstone A: [06-workshops/09-AgentCore-E2E](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/09-AgentCore-E2E) — ~1 day (est.)**
Six labs: prototype → production customer support agent combining Runtime, Memory, Gateway + Identity, Policy, Observability, Evaluations, plus a Streamlit front end. Strands track available today (Google ADK / LangGraph "coming soon"). You build: the full production shape of an agent — the template for our first internal assistant.

**Step 11 — Capstone B (domain): [06-workshops/13-AgentCore-payments](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/13-AgentCore-payments) — ~1–2 days (est.)**
Eight tutorials: payment stack setup (IAM roles, PaymentManager/Connector, embedded wallet, budgeted PaymentSession) → agents that pay x402 endpoints with budget enforcement (Strands & LangGraph) → runtime deploy → wallet ops → paid MCP tools via Gateway (Coinbase Bazaar) → browser paywall payments → payment memory → multi-agent budgets. **Preview**; needs preview access + Coinbase CDP or Stripe (Privy) credentials; testnet USDC from faucet.circle.com (the pay-for-data use case is mainnet — skip in training). Last deliberately: it composes Runtime+Gateway+Memory+Browser and is our domain-relevant capstone, but preview APIs may change.

**Optional / later:** [05-AgentCore-tools](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/05-AgentCore-tools) (Code Interpreter + Browser — pull in when a use case needs them, e.g., document analysis), [10-Agent-Registry](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/10-Agent-Registry) (multi-team governance — matters at scale, limited regions), [12-AgentCore-optimization](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/12-AgentCore-optimization) (baseline eval → prompt/tool-description recommendations → config bundles → A/B canary — adopt once an agent is in production).

**Blueprints to mine when designing our platform:** [customer-support-agent-with-agentcore](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/customer-support-agent-with-agentcore) (Runtime+Gateway+Policy+Memory+Cognito JWT, Claude Sonnet), [multitenant-agentic-platform](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/multitenant-agentic-platform) (tenant isolation, per-tenant token limits/429s, cost allocation — Claude Sonnet 4.5; the shape of an internal agent platform), [shopping-concierge-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/shopping-concierge-agent) and [travel-concierge-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/travel-concierge-agent) (both tagged **FSI / Agentic Payments**, multi-agent, Strands+MCP), [end-to-end-customer-service-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/end-to-end-customer-service-agent) (LangGraph + LLM gateway + guardrails). Feature deep-dive for payments beyond the workshop: [01-features/08-agents-that-transact](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/08-agents-that-transact).

> Repo-structure caveat: the repo is migrating from Starter-Toolkit-era numbered folders to the AgentCore CLI layout (top-level README already references `getting-started/`, `features/`, etc.; see [MIGRATION.md](https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/MIGRATION.md)). Links above match the clone at commit `0082e84` (2026-08-09); if a numbered link 404s, check MIGRATION.md for the new path.

## Coverage vs. our adoption sequence

The path front-loads exactly what the summit positioned as our sequence: ground-truth loop (CLI, harness) → hosting (Runtime) → integration (Gateway, matching the Gateway summit note) → personalization (Memory) → security (Identity, Policy — the fintech-case mechanics) → operability (Observability, Evaluations) → composition (E2E) → domain capstone (payments, preview). Two summit topics are intentionally **not** in this path: Managed Knowledge Base RAG (covered by [knowledge-base-rag.md](./knowledge-base-rag.md); add a KB-as-Gateway-target lab after Step 5 once we create our first managed KB) and AWS Context (announced "coming soon"; nothing hands-on exists to train against). Reordering vs. the workshops README ("start at 01-runtime, go in order"): harness first (fastest win, GA highlight of the summit), memory before identity (didactic), policy pulled before E2E (E2E labs depend on it), tools/registry/optimization deferred (not on the adoption critical path).

## Open questions for our build plan

- Actual wall-clock time per module for our team — READMEs don't state durations; validate my estimates in the first cohort and record real timings here.
- Payments preview access: how to request it for our account, and whether Coinbase CDP vs Stripe (Privy) is the right connector for a remittance use case.
- Whether the hosted catalog workshops (getting-started / deep-dive) match the current CLI (`@aws/agentcore`) or still use the legacy Starter Toolkit — check the first lab before recommending to the team.
- E2E workshop LangGraph track availability (currently "coming soon") if we standardize on LangGraph instead of Strands.
- Cost telemetry for training: set an AWS Budget alarm on the sandbox account before Phase 0; quantify Claude inference cost of one full pass through Steps 1–10.

Last verified: 2026-08-11
