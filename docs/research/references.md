# References and Methodology

> Source registry for the **[Agentic AI Research Library](00-executive-summary.md)**. All documents
> cite sources as `[S#]`, resolved here.

## How this research was produced

**Two passes.**

- **Pass 1 (2026-07-06)** — the original deep-research pipeline behind the predecessor package
  (`docs/research/agentic-ai-data-area/`). It decomposed the question into 5 search angles, fetched
  23 sources, extracted 115 falsifiable claims, and adversarially verified the top 25 with 3
  independent votes each — **all 25 confirmed 3-0**. Sources `[S1]–[S25]`.
- **Pass 2 (2026-07-16)** — a targeted refresh for this library across 7 clusters (platforms/
  frameworks, knowledge/retrieval, integration, security/compliance, evaluation, observability/
  governance, cost). Prioritized primary vendor docs, standards bodies, and peer-reviewed work,
  recording publication/update dates. Sources `[S26]+`. Pass-2 claims are tagged **[Extracted]**
  (single fetched source) unless corroborated; they were **not** put through the 3-vote adversarial
  verification, and time-sensitive facts (pricing, GA dates, feature availability) are flagged
  "verify at time of use."

## Evidence tiers

- **[Verified]** — survived Pass-1 3-vote adversarial verification against the primary source.
- **[Extracted]** — quoted/near-quoted from a fetched source; reliable as "the source says X," not
  independently corroborated.
- **[Inference]** — our reasoned application of evidence to this organization; not a sourced fact.
- **[Recommendation]** — our proposed course of action.
- **[Assumption]** / **[Open decision]** — explicitly unconfirmed; tracked in
  [14](14-risks-open-questions-and-decisions.md).

## Known bias and coverage caveats

- **Vendor concentration:** many claims come from vendor guidance (OpenAI, Anthropic, Microsoft,
  AWS, Atlassian, GitHub, Salesforce). These are authoritative primaries but shift fast and are
  self-interested on comparative judgments — treat framework/product comparisons as directional.
- **Small-n empirical bases:** the production-practices statistics [S9] rest on ~20 case studies +
  a modest survey; AgenticAKM [S11] is one workshop-scale study; AAGMM [S13] is simulation-based.
- **Pass-2 dates:** several practitioner-blog dates are publisher-stated and unverified against
  original publication; AWS/vendor primary docs are authoritative for their own feature claims.
- **Explicitly unverified Pass-2 items** (confirm before relying): GTM official MCP server
  (none found); GA4 Data API exact quotas; Salesforce MCP throttles; Bedrock "Classic"/Q close
  dates; cross-region +10% pricing; Helicone maintenance-mode; a reported SR 11-7 extension to AI;
  OpenAI Evals shutdown date; a single ratified per-agent governance-card template.

---

## Pass 1 — `[S1]–[S25]`

### Primary vendor guidance

| # | Source | Why it matters |
|---|---|---|
| S1 | [OpenAI — *A Practical Guide to Building Agents* (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | Gating test; single-agent-first; manager vs decentralized orchestration; layered guardrails; per-tool risk ratings; two mandatory HITL triggers; tool-registry & model-downshift |
| S2 | [Anthropic — *Building Effective Agents*](https://www.anthropic.com/research/building-effective-agents) | Workflow-vs-agent distinction; five composable patterns; "start with LLM APIs directly"; tool design as the agent-computer interface |
| S3 | [Anthropic — *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system) | Multi-agent cost/benefit; token spend explains 80% of variance; 4×/15× costs; delegation-specification failure modes |
| S4 | [Anthropic — *Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 20–50 tasks from real failures; grader taxonomy; outcome- not path-grading; pass@k vs pass^k; Swiss-cheese quality |
| S5 | [Microsoft — Azure Architecture Center: *AI agent design patterns*](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Single-agent-with-tools default; five orchestration patterns + failure modes; security trimming; 4-checkpoint content safety (updated May 2026) |
| S6 | [Microsoft — *Agentic AI adoption maturity model: security & governance*](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/maturity-model-security-governance) | Levels 100–500; Level-100 prerequisites; tiered (not uniform) controls; AI Council with real decision rights |
| S7 | [AWS — Prescriptive Guidance: *Agentic AI patterns*](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html) | Workflow (centralized) vs multi-agent (decentralized); agentic patterns as evolved event-driven architecture |
| S8 | [OpenAI Cookbook — *Agentic governance guide*](https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook) | Governance-as-code accelerates delivery; agent/tool/prompt registries; risk-tiered controls; policy-as-code |

### Peer-reviewed / academic

| # | Source | Why it matters |
|---|---|---|
| S9 | [*Measuring Agents in Production* — arXiv 2512.04123](https://arxiv.org/pdf/2512.04123) | Largest production-agent study: 68% ≤10 steps, 70% prompting-only, 80% structured workflows, 85% custom, 74% human-primary eval, internal-first |
| S10 | [*Why Do Multi-Agent LLM Systems Fail?* (MAST) — OpenReview](https://openreview.net/forum?id=fAjbYBmonr) | 41–86.7% failure rates; 14 failure modes / 3 categories; 94%-accurate LLM-judge failure annotation |
| S11 | [*AgenticAKM* — arXiv 2602.04445](https://arxiv.org/html/2602.04445v1) | Orchestrated Extraction→Retrieval→Generation→Validation beat single-prompt LLMs at ADR generation; bounded 3-iteration validator loops (preliminary) |
| S12 | [*GenAI in Software Architecture* systematic review — arXiv 2503.13310](https://arxiv.org/pdf/2503.13310) | Requirements-to-architecture = #1 use case (40%); 85% human-in-the-loop; rigorous testing typically absent; ADR/C4 thinly evidenced |
| S13 | [*Agentic AI Governance Maturity Model* (AAGMM) — arXiv 2604.16338](https://arxiv.org/pdf/2604.16338) | 5 levels / 12 domains; Level 3 = minimum viable governance; sprawl taxonomy (simulation-based) |
| S14 | [Google Research — multi-agent scaling, arXiv 2512.08296](https://arxiv.org/abs/2512.08296) | +81% parallelizable / −70% sequential — confirms the parallelizable-vs-sequential fit criterion |
| S15 | [Tran & Kiela — arXiv 2604.02460](https://arxiv.org/abs/2604.02460) | Single agents match multi-agent under equal token budgets |

### Practitioner / industry

| # | Source | Why it matters |
|---|---|---|
| S16 | [Cognition — *Don't Build Multi-Agents*](https://cognition.com/blog/dont-build-multi-agents) | Parallel-subagent fragility; single-threaded + context compression suffices for most production tasks |
| S17 | [Cleanlab — *AI Agents in Production 2025*](https://cleanlab.ai/ai-agents-in-production-2025/) | ~5% have agents in production; 70% of regulated firms rebuild stack ≤3 months; observability/evals weakest; 42% adding approval controls |
| S18 | [Langfuse — agent framework comparison](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) | Framework decision variables; LangGraph/CrewAI/SK positioning; tracing as production necessity |
| S19 | [Turing — AI agent frameworks comparison](https://www.turing.com/resources/ai-agent-frameworks) | Six-framework comparison incl. failure modes |
| S20 | [Atla — AI agent frameworks analysis](https://atla-ai.com/post/ai-agent-frameworks) | LangGraph as inspectable FSM; AutoGen reproducibility issues; OpenAI Agents SDK primitives |
| S21 | [LangChain — AI agent frameworks resource](https://www.langchain.com/resources/ai-agent-frameworks) | MS Agent Framework as unified successor; CrewAI gaps; OpenAI SDK durability; ADK session-isolation failure |
| S22 | [joelparkerhenderson/architecture-decision-record (GitHub)](https://github.com/joelparkerhenderson/architecture-decision-record) | Canonical ADR reference: quality rules, immutability/supersession, template landscape |
| S23 | [MSiccDev/arc42-toolkit (GitHub)](https://github.com/MSiccDev/arc42-toolkit) | LLM-driven arc42: ask-first intake, consistency linter in CI, C4-as-PlantUML |
| S24 | [bitsmuggler/arc42-c4 example (GitHub)](https://github.com/bitsmuggler/arc42-c4-software-architecture-documentation-example) | Docs-as-code: arc42 + C4 via Structurizr; ADRs as Markdown; self-hosted-render privacy caveat |
| S25 | [Agenta — structured outputs & function calling guide](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms) | Schema-first: define once → generate JSON Schema → enforce via API/tool-use → validate; prompt-parsing is fragile |

---

## Pass 2 — `[S26]+` (mid-2026 refresh)

### Platforms & frameworks

| # | Source (publisher, date) | Note |
|---|---|---|
| S26 | [Amazon Bedrock AgentCore is GA — AWS, 2025-10-13](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available/) | Runtime/Memory/Gateway/Identity/Observability; 8-hr runtime; MCP-native gateway |
| S27 | [What is Bedrock AgentCore — AWS docs, n.d.](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) | Code Interpreter & Browser tools |
| S28 | [AgentCore in AWS GovCloud (US-West) — AWS, 2026-05](https://aws.amazon.com/about-aws/whats-new/2026/05/bedrock-agentcore-launch-aws-govcloud-us/) | Regulated/gov readiness |
| S29 | [Orchestration models — AWS Prescriptive Guidance (Agentic AI serverless), n.d.](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/orchestration-models.html) | Step Functions/Lambda/EventBridge as deterministic, auditable orchestration |
| S30 | [LangChain & LangGraph reach v1.0 — LangChain, 2025-10](https://blog.langchain.com/langchain-langgraph-1dot0/) | LangGraph = durable stateful runtime; LangChain = agent-building layer |
| S31 | [Microsoft ships Agent Framework 1.0 — Visual Studio Magazine, 2026-04-06](https://visualstudiomagazine.com/articles/2026/04/06/microsoft-ships-production-ready-agent-framework-1-0-for-net-and-python.aspx) · [Overview — Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/overview/) | Unified successor to SK + AutoGen; Azure-leaning |
| S32 | [Donating MCP / Agentic AI Foundation — Anthropic, 2025-12](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) | MCP → Linux Foundation; broad vendor backing |
| S33 | [Amazon Q Developer features — AWS, n.d.](https://aws.amazon.com/q/developer/features/) | Agentic coding assistant (adjacent tool) |
| S34 | [Choosing an AWS vector DB for RAG — AWS Prescriptive Guidance, 2025](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-comparison.html) | OpenSearch default; pgvector/Neptune/S3 Vectors trade-offs |

### Knowledge & retrieval

| # | Source (publisher, date) | Note |
|---|---|---|
| S35 | [Access control via metadata filtering (Bedrock KB) — AWS ML Blog, 2025](https://aws.amazon.com/blogs/machine-learning/access-control-for-vector-stores-using-metadata-filtering-with-knowledge-bases-for-amazon-bedrock/) | Per-user ACL on a shared KB; filter is *your* responsibility |
| S36 | [Secure multi-tenant RAG w/ Verified Permissions — AWS Architecture Blog, 2025](https://aws.amazon.com/blogs/architecture/secure-multi-tenant-rag-with-amazon-bedrock-and-verified-permissions/) | Cedar policies build the metadata filter at query time |
| S37 | [Bedrock KB GraphRAG (Neptune) GA — AWS, 2025-03](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-knowledge-bases-graphrag-generally-available/) | Managed GraphRAG |
| S38 | [Why Vector Search Alone Isn't Enough — InfoQ, 2026](https://www.infoq.com/articles/vector-search-hybrid-retrieval-rag/) | Dense fails on exact IDs; hybrid BM25+dense; cross-encoder rerank |
| S39 | [Permission-Aware Retrieval — TianPan, 2026-05](https://tianpan.co/blog/2026-05-04-permission-aware-retrieval-enterprise-rag-access-control) | Enforce ACLs at the retrieval layer, not the app layer |
| S40 | [The RAG Freshness Problem — TianPan, 2026-04](https://tianpan.co/blog/2026-04-10-rag-freshness-problem-stale-embeddings-silent-failure) | Vector similarity has no time dimension; recency + source-authority + deterministic conflict resolution |
| S41 | [Best Chunking Strategies for RAG — Firecrawl, 2026](https://www.firecrawl.dev/blog/best-chunking-strategies-rag) | Semantic chunking often not worth its cost; contextual/parent-context; ~512 tokens |
| S42 | [RAG vs GraphRAG — Graffitecs, 2026](https://graffitecs.com/pages/insights/rag-vs-graphrag.html) | GraphRAG ~6–8× index / ~3× ops; use only for multi-hop/lineage |
| S43 | [AWS Vector Store for RAG beyond OpenSearch (S3 Vectors) — Cevo, 2025/26](https://cevo.com.au/post/aws-vector-store-for-rag-beyond-opensearch/) | S3 Vectors GA 2025-12; cheap, sub-second |

### Integration

| # | Source (publisher, date) | Note |
|---|---|---|
| S44 | [Atlassian Remote MCP Server — Atlassian, 2025-05](https://www.atlassian.com/blog/announcements/remote-mcp-server) · [atlassian/atlassian-mcp-server (GitHub), 2026](https://github.com/atlassian/atlassian-mcp-server) | GA 2026-02; respects user permissions |
| S45 | [Jira rate limiting (points model, effective 2026-03-02) — Atlassian](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/) | Writes cost more; 429 + Retry-After |
| S46 | [Remote GitHub MCP Server GA — GitHub, 2025-09-04](https://github.blog/changelog/2025-09-04-remote-github-mcp-server-is-now-generally-available/) | OAuth 2.1 / PAT |
| S47 | [GitHub MCP vs API auth — Scalekit, 2026](https://www.scalekit.com/blog/github-mcp-vs-api) | App-install tokens unsupported by MCP; use REST for multi-org |
| S48 | [Salesforce Hosted MCP Servers GA — Salesforce, 2026-04](https://developer.salesforce.com/blogs/2026/04/salesforce-hosted-mcp-servers-are-now-generally-available) · [Connect Claude w/ Salesforce MCP (ECA/OAuth), 2026-05](https://developer.salesforce.com/blogs/2026/05/connect-claude-with-salesforce-hosted-mcp-servers) | Runs as authenticated user; Connected Apps not usable |
| S49 | [google-analytics-mcp (read-only) — Google/GitHub](https://github.com/googleanalytics/google-analytics-mcp) | Service account / OAuth `analytics.readonly` |
| S50 | [Understanding IAM for Managed AWS MCP Servers — AWS Security, 2025](https://aws.amazon.com/blogs/security/understanding-iam-for-managed-aws-mcp-servers/) · [Secure AI agent access patterns via MCP — AWS Security, 2025](https://aws.amazon.com/blogs/security/secure-ai-agent-access-patterns-to-aws-resources-using-model-context-protocol/) | SigV4; STS short-lived creds; agent-vs-human context keys |
| S51 | [HITL approval workflows (propose-then-commit) — StackAI](https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation) | Risk-tier gating; pause/queue/resume |
| S52 | [Idempotent tool calls & agent retry safety — Chanl](https://www.channel.tel/blog/idempotent-tool-calls-agent-retry-safety) | Idempotency key before approval; backoff + jitter; capped retries |

### Security, privacy & compliance

| # | Source (publisher, date) | Note |
|---|---|---|
| S53 | [OWASP Top 10 for LLM Applications 2025 — OWASP GenAI Security Project](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | LLM01–LLM10 incl. prompt injection, sensitive-info disclosure, supply chain, poisoning, excessive agency |
| S54 | [OWASP Agentic AI – Threats & Mitigations — OWASP GenAI, 2025-02](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) · [Top 10 for Agentic Applications — OWASP GenAI, 2025-12](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Behavior hijacking, tool misuse, identity/privilege abuse |
| S55 | [NIST AI 600-1 Generative AI Profile — NIST, 2024-07](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | Govern/Map/Measure/Manage; 12 GenAI risk areas |
| S56 | [MITRE ATLAS Fact Sheet — MITRE, 2025](https://atlas.mitre.org/pdf-files/MITRE_ATLAS_Fact_Sheet.pdf) · [ATLAS](https://atlas.mitre.org/) | Adversary tactics/techniques incl. RAG poisoning; red-team reference |
| S57 | [Amazon Bedrock Security, Privacy & Responsible AI — AWS, 2025](https://aws.amazon.com/bedrock/security-privacy-responsible-ai/) | No prompt/output retention; no provider sharing; no training on inputs |
| S58 | [Anthropic API & data retention — Claude Platform Docs, 2025](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) · [ZDR scope — Anthropic Privacy Center](https://privacy.claude.com/en/articles/8956058-i-have-a-zero-data-retention-agreement-with-anthropic-what-products-does-it-apply-to) | No training without permission; 7-day standard retention; ZDR/HIPAA available |
| S59 | [FTC Safeguards Rule (GLBA) — FTC, 2024](https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know) | InfoSec program; encryption; MFA; least-privilege review; breach notice (500+, 2024-05-13) |
| S60 | [BSA Requirements for MSBs — FinCEN](https://www.fincen.gov/bsa-requirements-msbs) · [CIP — FFIEC BSA/AML Manual](https://bsaaml.ffiec.gov/manual/RegulatoryRequirements/01) | Registration, AML program, CIP/CDD, OFAC, SAR/CTR, Travel Rule |
| S61 | [SR 11-7 Model Risk Management — Federal Reserve, 2011](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) | Model development/validation/governance; applied by analogy to AI (AI extension *unverified*) |
| S62 | [Least privilege for AI agents — Okta, 2025](https://www.okta.com/identity-101/how-to-implement-least-privilege-for-ai-agents/) · [Agentic IAM / non-human identity — Ping Identity, 2025](https://www.pingidentity.com/en/resources/identity-fundamentals/agentic-ai.html) | Agent as governed NHI; JIT/time-bounded creds; audit trails |

### Evaluation & testing

| # | Source (publisher, date) | Note |
|---|---|---|
| S63 | [New RAG eval & LLM-as-judge in Amazon Bedrock — AWS, 2025](https://aws.amazon.com/blogs/aws/new-rag-evaluation-and-llm-as-a-judge-capabilities-in-amazon-bedrock/) | Managed model/RAG/agent eval; citation precision/coverage; correctness/faithfulness |
| S64 | [Evaluate Bedrock Agents with Ragas & LLM-as-judge — AWS, 2025](https://aws.amazon.com/blogs/machine-learning/evaluate-amazon-bedrock-agents-with-ragas-and-llm-as-a-judge/) | Ragas ↔ Bedrock agents |
| S65 | [Ragas available metrics — docs, 2025](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) | Context precision/recall (retrieval) vs faithfulness/relevance (generation) |
| S66 | [LLM-as-a-Judge vs Human Evaluation — Galileo, 2025](https://galileo.ai/blog/llm-as-a-judge-vs-human-evaluation) | Position/verbosity/self-preference bias; calibration |
| S67 | [Evaluating AI Agents: trajectories not just outcomes — TianPan, 2026](https://tianpan.co/blog/2026-02-07-evaluating-ai-agents-trajectories-not-just-outcomes) | Grade both outcome and trajectory |
| S68 | [Evaluation & Benchmarking of LLM Agents — KDD'25 tutorial, 2025](https://sap-samples.github.io/llm-agents-eval-tutorial/2025_KDD_Evaluation_and_Benchmarking_of_LLM_Agents.pdf) | pass@k vs pass^k; gate on significant deltas; regression from incidents |
| S69 | [Agent Rollout Strategies — FutureAGI, 2026](https://futureagi.com/blog/agent-rollout-strategies-2026/) · [Shadow Traffic & Canary — FutureAGI, 2026](https://futureagi.com/blog/llm-eval-shadow-traffic-canary-2026/) | Shadow → canary → % → full; agent quality as SLO |
| S70 | [LLM Eval Tools Compared — benchmarkingagents.com, 2026](https://benchmarkingagents.com/tools-compared/) · [LLM Evaluation Platforms — Arize, 2025](https://arize.com/llm-evaluation-platforms-top-frameworks/) | LangSmith/Langfuse/Braintrust/Phoenix positioning |
| S71 | [Evaluation datasets & synthetic data — DeepEval docs, 2026](https://deepeval.com/docs/evaluation-datasets) · [Building a Golden Dataset — Maxim AI, 2025](https://www.getmaxim.ai/articles/building-a-golden-dataset-for-ai-evaluation-a-step-by-step-guide/) | Golden datasets; synthesis→human-verification |

### Observability & governance

| # | Source (publisher, date) | Note |
|---|---|---|
| S72 | [gen-ai semantic conventions v1.37 — OpenTelemetry GitHub, 2025](https://github.com/open-telemetry/semantic-conventions/tree/v1.37.0/docs/gen-ai) · [GenAI Observability — OpenTelemetry blog, 2026](https://opentelemetry.io/blog/2026/genai-observability/) | `gen_ai.*` client/agent/tool spans; still Development status |
| S73 | [LLM Observability Overview — Langfuse, 2026](https://langfuse.com/docs/observability/overview) | Traces/spans/generations; OSS self-host or SaaS |
| S74 | [Tracing Overview — Arize Phoenix, 2026](https://arize.com/docs/phoenix/tracing/llm-traces) | OpenInference/OTel tracing + monitoring |
| S75 | [Add observability to AgentCore — AWS docs, 2026](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html) · [CloudWatch GenAI Observability Preview — AWS, 2025](https://aws.amazon.com/blogs/mt/launching-amazon-cloudwatch-generative-ai-observability-preview/) | OTEL to CloudWatch by default; exports to Datadog/Grafana |
| S76 | [Datadog supports OTel GenAI SemConv — Datadog, 2026](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) | SaaS APM mapping `gen_ai.*` |
| S77 | [Google donates A2A to Linux Foundation — Google, 2025](https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/) · [A2A one-year — Linux Foundation, 2026](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) | Agent Cards (discovery); Signed Agent Cards |
| S78 | [What Is an AI Registry — Atlan, 2025](https://atlan.com/know/what-is-ai-registry/) | Central inventory: models, prompts, tools, sources, owners, risk class, approvals |
| S79 | [NIST AI RMF / EU AI Act / ISO 42001 compared — Trustible, 2025](https://trustible.ai/post/nist-ai-rmf-eu-ai-act-iso-42001-compared/) | Risk-tier scheme (EU Act) to fill NIST's classification gap |
| S80 | [Policy Cards — arXiv 2510.24383, 2025](https://arxiv.org/pdf/2510.24383) | Machine-readable runtime governance artifacts |

### Cost & scalability

| # | Source (publisher, date) | Note |
|---|---|---|
| S81 | [Amazon Bedrock Pricing — AWS](https://aws.amazon.com/bedrock/pricing/) · [AWS Bedrock Pricing 2026 — pecollective](https://pecollective.com/tools/aws-bedrock-pricing/) | Per-token rates; Bedrock lags newest model IDs (*verify*) |
| S82 | [Bedrock one-hour prompt caching — AWS, 2026-01](https://aws.amazon.com/about-aws/whats-new/2026/01/amazon-bedrock-one-hour-duration-prompt-caching/) · [Prompt caching docs — AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) | Cache reads ~0.1×; writes 1.25×/2×; up to ~90% off cached input |
| S83 | [Prompt caching — Caylent, 2025](https://caylent.com/blog/prompt-caching-saving-time-and-money-in-llm-applications) | Cache-heavy agents save ~60–70% of task cost |
| S84 | [Bedrock batch inference 50% off — AWS, 2024](https://aws.amazon.com/about-aws/whats-new/2024/08/amazon-bedrock-fms-batch-inference-50-price/) | Async batch discount |
| S85 | [Bedrock Intelligent Prompt Routing — AWS](https://aws.amazon.com/bedrock/intelligent-prompt-routing/) | Within-family routing; ~30% savings claimed |
| S86 | [Optimize LLM costs on Bedrock (billing attribution) — AWS CFM blog](https://aws.amazon.com/blogs/aws-cloud-financial-management/optimize-llm-costs-on-amazon-bedrock-from-billing-attribution-to-operational-telemetry/) | Application Inference Profiles + cost-allocation tags = showback/chargeback |
| S87 | [OpenSearch Service pricing — AWS](https://aws.amazon.com/opensearch-service/pricing/) · [OpenSearch Serverless NextGen GA — AWS, 2026-05-28](https://aws.amazon.com/about-aws/whats-new/2026/05/amazon-opensearch-serverless-next-generation-generally-available/) | OCU idle floor trap; NextGen scales to zero |
| S88 | Anthropic `claude-api` skill catalog (internal, cached **2026-06-24**) | Authoritative model IDs/rates: Opus 4.8 $5/$25, Sonnet 5 $3/$15, Haiku 4.5 $1/$5, Fable 5 $10/$50 |
