# AgentCore Observability and Evaluations — Verified Reference

**Topic:** How AgentCore Observability (OTEL → CloudWatch GenAI Observability) and AgentCore Evaluations (LLM-as-judge scoring of traces) actually work, plus the preview "Optimization" layer (Insights, Recommendations, A/B testing).
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-get-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/built-in-evaluators-overview.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/custom-evaluators.html
- https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available
- https://aws.amazon.com/bedrock/agentcore/pricing/
- https://aws.amazon.com/bedrock/agentcore/faqs/

**Related summit note(s):**
- [../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md](../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md)
- [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md)

The summit notes say what was announced; this note says how it works, verified.

## Verified facts (official docs)

### Observability (GA)
- Telemetry is **OpenTelemetry-compatible**; everything (metrics, spans, logs) lands in **Amazon CloudWatch**, viewable in the **GenAI Observability dashboard** (Agents / Sessions / Traces views: trace trajectory, timeline, error breakdowns, token usage, latency, session counts). Built-in metrics are emitted by default for **agents, gateway, and memory** resources (memory spans/logs are opt-in).
- **One-time prerequisite per account/region:** enable **CloudWatch Transaction Search** (X-Ray span ingestion to CloudWatch Logs; 1% trace indexing free, configurable). Without it, no traces appear.
- **Runtime-hosted agents:** automatic OTEL instrumentation on `agentcore deploy` — no OTEL libraries or config needed.
- **Agents hosted elsewhere (EKS, Lambda, ECS, on-prem):** add **ADOT SDK** (`aws-opentelemetry-distro`) and run under `opentelemetry-instrument`, with env vars `AGENT_OBSERVABILITY_ENABLED=true`, `OTEL_PYTHON_DISTRO=aws_distro`, OTLP headers pointing at your log group, `OTEL_RESOURCE_ATTRIBUTES=service.name=<agent-name>`. Lambda uses the AWS OTEL Lambda layer + `AWS_LAMBDA_EXEC_WRAPPER=/opt/otel-instrument` instead. **The ADOT Collector is explicitly NOT supported** for agent observability.
- **Session correlation** across runs via OTEL baggage: `baggage.set_baggage("session.id", session_id)`; runtime session id also travels in header `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id`.
- Log locations: stdout/stderr and OTEL structured logs under `/aws/bedrock-agentcore/runtimes/<agent_id>-<endpoint>/...`; spans in the agent log group or shared `aws/spans`. Metrics namespace: `bedrock-agentcore`.
- Custom instrumentation (extra spans/metrics/logs) is supported on top of the defaults; docs' best practices explicitly call out **filtering sensitive data from span attributes/payloads** (PII — mandatory for us).
- **Pricing:** no AgentCore-specific charge; you pay **CloudWatch rates** for ingestion/storage/queries (plus Transaction Search indexing above 1%).
- **Claude support (flagged):** framework/model-agnostic; the official getting-started example itself runs Strands with **`us.anthropic.claude-3-7-sonnet-20250219-v1:0`** on Bedrock. Auto-instrumentation covers Strands, Bedrock calls, tools; LangChain/LangGraph/CrewAI need their auto-instrumentor packages (e.g., `opentelemetry-instrumentation-langchain`, OpenInference).

### Evaluations (GA 2026-03-31, was preview from Dec 2025)
- Scores agent behavior from **OTEL/OpenInference traces** (converted to a unified format) using **LLM-as-a-judge** — i.e., Evaluations consumes what Observability emits; instrument first, evaluate second. Integrates with **Strands and LangGraph** per the devguide.
- **13 built-in evaluators** covering response quality, safety, task completion, tool usage; referenced as `Builtin.<Name>` (e.g., `Builtin.Helpfulness`, ARN `arn:aws:bedrock-agentcore:::evaluator/Builtin.Helpfulness`). Built-in evaluator **models and prompt templates are fixed and cannot be modified** (the judge model behind built-ins is not disclosed in the docs).
- **Custom evaluators:** your own evaluator model + instructions + scoring schema (`CreateEvaluator`/`Get`/`List`/`Update`/`Delete`), or **code-based evaluators**. Judge model is your choice of Bedrock model — **Claude is usable as judge** (the GA announcement: "choice of prompts and model for LLM-based evaluation"). Custom evaluators are private, shareable via IAM resource policies.
- **Evaluation modes:** **on-demand** (synchronous, per-trace; returns score + explanation + token usage; CI/CD-friendly), **online** (continuous sampling of live production traces with your sample-size/selection criteria), **batch** (historical sessions, 25% discount), **dataset** and **ground-truth** evaluations (reference answers + behavioral assertions), and **simulation**.
- **Quotas:** default 1,000 evaluation configurations per region/account; up to 1M input+output tokens/minute per account in large regions.
- **Pricing:** built-in evaluators **$0.0024 per 1k input + $0.012 per 1k output tokens**; custom evaluators **$1.50 per 1,000 evaluations** (judge-model charges billed separately); batch −25%.
- **Regions:** GA'd initially in nine regions (us-east-1, us-east-2, us-west-2, Mumbai, Singapore, Sydney, Tokyo, Frankfurt, Ireland; March 2026 announcement); coverage has since expanded — the [current regions page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html) (accessed 2026-08-11) **now lists Evaluations (and optimization) as available in sa-east-1 (São Paulo)** alongside us-east-1.

### Optimization layer (preview)
Per the FAQ, **"Optimization" — failure/intent/trajectory Insights, Recommendations, and A/B testing — is in preview** (not GA). The samples show the shape: batch/online **Insights** (`FailureAnalysis`, `UserIntent`, `ExecutionSummary` — root-cause clustering of failures), AI-generated prompt/tool-description **Recommendations** from production traces, and **A/B testing** via versioned configuration bundles (prompt-level, no redeploy) or target-based routing (code-level, 90/10 canary).

## Implementation patterns (samples repo)

- **Observe / Evaluate / Optimize feature samples** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/06-observe-evaluate-optimize-your-agent — Python/Strands. `01-observe`: custom span creation, **PII data protection via Bedrock Guardrails + CloudWatch Logs data-protection policies**, attribute redaction, span filters — directly reusable for our compliance telemetry. `02-evaluate`: LLM-as-judge, code-based, and ground-truth evaluation. `03-optimize`: full Insights → baseline eval → Recommendations → A/B testing (config bundles + target routing) workflow on an HR-assistant agent.
- **Observability workshop** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/06-AgentCore-observability — notebooks for runtime-hosted (Strands, CrewAI, LlamaIndex on Bedrock models), non-runtime-hosted (LangGraph, CrewAI), Lambda invocation, EKS-hosted agents, partner observability, plus a CloudFormation template to enable Transaction Search (also at `05-infrastructure-as-code/01-enable-transaction-search`). Reuse the IaC + Strands notebook.
- **Evaluations workshop** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/07-AgentCore-evaluations — prereqs sample agent, custom evaluators, on-demand + online runs, ground-truth evaluations, programmatic evaluators, querying results from CloudWatch with boto3, local dashboards. Our template for a compliance-review evaluator (e.g., "did the agent follow AML escalation procedure").
- **3P observability integrations** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/3p-observability — OTLP export from runtime-hosted agents to Langfuse, Datadog, Dynatrace, Arize, Braintrust, Honeycomb, Instana, Dash0, OpenLIT. The Langfuse sample is Strands + **Claude Haiku 4.5**. Useful if we standardize on a non-CloudWatch stack.
- **AgentOps flywheel with Langfuse** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/AgentOps-Langfuse — continuous evaluation loop (offline test datasets incl. adversarial inputs → experiments → production monitoring) with CI/CD; the operating model behind the fintech case's "continuous improvement" story.

## Gaps vs. the summit slides

- **Platform-overview slide** listed Observability, Evaluations, **Insights (preview)**, Recommendations, A/B testing under "Optimization." Verified: Observability GA (https://aws.amazon.com/bedrock/agentcore/faqs/); Evaluations GA since 2026-03-31 (https://aws.amazon.com/about-aws/whats-new/2026/03/agentcore-evaluations-generally-available) — the slide's "Evaluations" claim holds; **Insights, Recommendations, and A/B testing remain preview** as part of "Optimization" per the FAQ — the slide correctly marked Insights as preview but did not flag Recommendations/A-B testing, which are also preview. Do not build production dependencies on them yet.
- **Fintech case slide** — "OpenTelemetry per session, every loop step": verified as exactly how AgentCore Observability works (session-scoped OTEL traces per step; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html). "**Self-reflection** at the end of a run, posting improvements to Slack": **not an AgentCore feature** — that was customer-built application logic; the closest platform equivalents are Evaluations (online) plus the preview Insights/Recommendations (https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/evaluations.html). "IDP (Port), agents born from templates" is third-party tooling, out of AgentCore scope.
- **Regional note:** Evaluations was absent from São Paulo at its March 2026 GA but is now listed there on the [current regions page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html) — no LatAm gap for Evaluations anymore.

## Open questions for our build plan

- Which judge model powers the **built-in** evaluators is undocumented — if judge provenance matters for model risk management, use custom evaluators pinned to a Claude judge; needs a hands-on comparison of built-in vs Claude-judged custom evaluators on our transcripts.
- Verify online-evaluation **sampling controls** (criteria granularity, per-agent sampling rates) and the latency between a production trace and its score landing in CloudWatch.
- Test CloudWatch Logs **data-protection policies + attribute redaction** against our PII taxonomy (names, account numbers, remittance amounts) before enabling span/payload capture in production; confirm what raw prompt/response content ends up in `aws/spans`.
- Data-residency check: with Evaluations now in sa-east-1, confirm a fully in-region telemetry + evaluation pipeline is possible for LatAm customer data (and which judge models Bedrock offers in São Paulo).
- Cost model at our volume: CloudWatch ingestion for full-span capture vs sampled; Transaction Search indexing percentage.
- Trial the preview Optimization A/B testing (config bundles) in a sandbox — pricing and GA timeline are unpublished.

Last verified: 2026-08-11
