# Amazon Bedrock Managed Knowledge Base — Verified Reference

**Topic:** Fully managed RAG on Amazon Bedrock (Managed Knowledge Base): connectors, ingestion, retrieval APIs, and its integration with AgentCore Gateway as an MCP tool.
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-build-managed.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-create.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-connect-ds.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-ds-sharepoint.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-ds-onedrive.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-regions.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-quotas.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/kb-gateway-target.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-managed-knowledge-base/ (GA announcement)
- https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-managed-knowledge-base-for-faster-more-accurate-enterprise-ai-applications/ (launch blog)

**Related summit note(s):** [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-managed-knowledge-base.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-managed-knowledge-base.md) — the summit note says what was announced; this note says how it works, verified.

## Verified facts (official docs)

### Two knowledge base types

Amazon Bedrock Knowledge Bases now has two flavors ([docs](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)):

- **Managed Knowledge Base** (GA **June 17, 2026** per the [What's New post](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-managed-knowledge-base/)) — Bedrock manages ingestion, indexing, auto-scaling storage, and retrieval. Service-managed embedding/reranking/reasoning models by default, with bring-your-own options. AWS explicitly recommends it over customer-managed.
- **Customer-managed Knowledge Base** — you provision/operate the vector store (OpenSearch Serverless, Aurora, Neptune, etc.). Third-party connectors, document-level permissions (ACLs), agentic retrieval, and native AgentCore Gateway integration are **only** available on the managed type.

### Connectors (all verified for the managed type)

Seven native connectors per [kb-build-managed](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-build-managed.html): **Amazon S3, SharePoint, Confluence, Web Crawler, Google Drive, OneDrive, Custom** (`connectorParameters.type`: `S3`, `SHAREPOINT`, `CONFLUENCE`, `WEB_CRAWLER`, `GOOGLE_DRIVE`, `ONEDRIVE`, plus Custom). The [connect-a-data-source page](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-connect-ds.html) additionally lists a **Box** connector topic (newer than the "7 connectors" table). Document-level ACL filtering at retrieval time is supported for all connectors **except Web Crawler**.

### SharePoint connector (our M365 estate) — [docs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-ds-sharepoint.html)

- Crawls files and pages from multiple SharePoint Online sites; incremental syncs (add/update/delete); path and date-range filters; site URLs must start with `/sites/`, `/teams/`, or `/personal/`.
- **Auth:** two methods, credentials stored in an **AWS Secrets Manager** secret (you supply the ARN + the M365 tenant ID):
  - `ENTRA_ID_APP_ONLY` (recommended) — Entra application authenticating with a **certificate**; required for ACLs.
  - `OAUTH2_APP` — client ID/secret + a user's username/password (ROPC flow). **Cannot** satisfy MFA/Conditional Access, **no ACL support**.
- **Least privilege is supported:** `Sites.Selected` on both Microsoft Graph and SharePoint REST limits the crawl to explicitly granted sites. ACLs add `User.Read.All` + `GroupMember.Read.All` (Graph) and require the `fullcontrol` role per site (`Sites.Selected`) or `Sites.FullControl.All` (all-sites) to read item-level permissions.
- ACL result filtering is applied at **query time** based on a `userContext` the calling application supplies.

### OneDrive connector — [docs](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-ds-onedrive.html)

- Crawls users' personal drives (OneDrive for Business); inclusion/exclusion filters by user email, item path, MIME type, date range. **OneNote notebooks are not supported.**
- **Auth:** `ENTRA_APP_ID` (recommended; client ID/secret via OAuth client-credentials, plus a certificate to SharePoint when ACLs are enabled) or `OAUTH2` (delegated refresh token from a user sign-in — token expires and must be re-minted; no ACLs; only crawls what that one user can see). Credentials in Secrets Manager.

### Ingestion: parsing, chunking, multimodal

- **Smart Parsing** (`parsingStrategy: "SMART_PARSING"`) auto-selects a parsing strategy per document type: PDFs, PPTX, DOCX, docs with embedded visuals, audio, video, scanned documents.
- Advanced indexing toggles for **visual content** (.png/.jpg/.tiff/.svg/.heic etc. and visuals embedded in .pdf/.docx/.ppt/.pptx), **audio** (.mp3/.wav/.m4a/.flac/.ogg), and **video** (.mp4/.mov/.m4v).
- Chunking: **default (built-in)**, **fixed-size**, or **no chunking**.
- Deletion safeguard: `deletionProtectionConfiguration` caps the % of documents a sync may delete (default threshold 15%).

### Embedding and model options — [kb-managed-create](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-create.html)

- **Managed embedding (default):** service-managed model, no selection or extra cost; required if you want the **managed reranker**.
- **Custom embedding:** any of Amazon Titan Text Embeddings V2, Cohere Embed English v3, Cohere Embed Multilingual v3, Cohere Embed v4, Amazon Nova Multimodal Embeddings — must be **1024-dim float32**. Choosing custom embedding **disables the managed reranker**, and the embedding type **cannot be changed** after creation.
- Reranking: managed (default) / custom Bedrock reranking model / none.

### Retrieval APIs

- **`Retrieve`** — single hybrid (keyword + vector) or semantic search; returns passages with source references and scores.
- **`AgenticRetrieveStream`** — **multi-step agentic retrieval**: plans a strategy, decomposes complex queries into sub-queries, retrieves iteratively across one or more managed KBs, optionally expands to full documents, evaluates sufficiency, and streams trace events plus a **synthesized citation-backed answer** (suppress with `generateResponse: false`). This verifies the summit slide's "multi-step agentic retrieval" claim.
- Control plane: `CreateKnowledgeBase` (`type: "MANAGED"`), `CreateDataSource` (`type: "MANAGED_KNOWLEDGE_BASE_CONNECTOR"`, asynchronous for managed KBs), `StartIngestionJob` for syncs.

### Claude support — FLAGGED EXPLICITLY

- **Answer synthesis (agentic retrieval):** `agenticRetrieveConfiguration.foundationModelType` is `MANAGED` (service-managed model, default) or `CUSTOM` with **any Bedrock foundation model ARN you supply — Anthropic Claude models qualify**. The [launch blog](https://aws.amazon.com/blogs/aws/introducing-amazon-bedrock-managed-knowledge-base-for-faster-more-accurate-enterprise-ai-applications/) states every foundation model available on Bedrock can power the generation step.
- **Classic `RetrieveAndGenerate`** (the pre-existing KB API) supports Claude generation models and inference profiles per [knowledge-base-supported](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html) / model cards. The managed-KB docs consistently describe `Retrieve` + `AgenticRetrieveStream` as its query surface; whether `RetrieveAndGenerate` also accepts a managed KB is not stated — see Open questions.
- **Parsing with Claude:** Claude vision models are a supported foundation-model parser option (documented for KB advanced parsing; managed KBs default to the built-in Smart Parser).

### Regions — [kb-managed-regions](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-regions.html)

`us-east-1` (N. Virginia), `us-west-2`, `eu-west-1`, `eu-west-2`, `eu-central-1`, `ap-northeast-1`, `ap-southeast-2`, `us-gov-west-1` (GovCloud with heavy feature restrictions: S3 only, no ACLs, no managed models, no agentic retrieval, no Gateway integration).
**No Latin America region: `sa-east-1` (São Paulo) is NOT supported for managed KBs.** For Viamericas, plan on **us-east-1**. (Customer-managed KBs with structured data stores do list São Paulo, but that is a different feature.)

### Quotas — [kb-managed-quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-quotas.html)

| Quota | Default | Adjustable |
|---|---|---|
| Managed KBs per account/region | 10,000 | Yes |
| Data sources per KB | 200 | No |
| Concurrent ingestion jobs per KB | 50 | No |
| Raw data storage per KB | 10 TB | No |
| Query input chars per Retrieve/AgenticRetrieveStream | 10,000 | No |
| Retrieve RPM per KB | 600 (burst 25 RPS) | Yes |
| AgenticRetrieveStream requests/min per account | 60 | Yes |

### Pricing

Per the GA announcement coverage: **~$5 per GB of raw indexed data per month** and **$1 per 1,000 standard Retrieve calls**, with managed parsing, embedding, and reranking included; agentic retrieval adds **$4 per 1,000 calls (planning) + $1 per 1,000 retrieve calls**. Confirm current numbers at https://aws.amazon.com/bedrock/pricing/ before budgeting (pricing page itself not re-verified line-by-line).

### Relation to AgentCore ("Managed Knowledge Base" as agent context)

- The managed KB console lives under **Amazon Bedrock AgentCore > Built-in tools > Knowledge Base** — AWS positions it as AgentCore's context/grounding layer.
- **AgentCore Gateway connector target** ([AgentCore devguide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html)): attach a managed KB to a Gateway and any MCP client discovers two tools via `tools/list` — `<target>___Retrieve` and `<target>___AgenticRetrieveStream`. The agent sends only `retrievalQuery.text` / `messages`; KB IDs, retrievers, model choices, `numberOfResults`, filters, and guardrails are administrator-set on the target (`parameterValues`), optionally exposed to agents via `parameterOverrides`. Outbound auth is **IAM-only** (`GATEWAY_IAM_ROLE`); the gateway service role needs `bedrock:Retrieve` on the KB ARN. Managed KBs only — customer-managed KBs cannot be Gateway targets.
- Native integration with **AgentCore Observability** (retrieval traces, agentic traces, per-KB metrics) per the [KB overview page](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html).
- ACL-filtered retrieval through Gateway requires the **application** (not the model) to pass `userContext` in `tools/call` arguments; the Gateway does not derive it from the caller's IAM identity.

## Implementation patterns (samples repo)

The samples repo has no managed-KB-specific sample yet (the service GA'd 2026-06); the closest RAG-adjacent patterns:

- [03-integrations/vector-stores/elasticsearch](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/vector-stores/elasticsearch) — notebook exposing Elasticsearch vector search as an AgentCore **Gateway Lambda target** for RAG over customer-support policies and product manuals. Stack: Gateway + Lambda + Elasticsearch. For Viamericas: the pre-managed-KB pattern to compare against; the managed KB connector target now replaces most of this plumbing.
- [03-integrations/data-platforms/databricks-dbsql-agentcore-gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/data-platforms/databricks-dbsql-agentcore-gateway) — exposes Databricks managed MCP servers (DBSQL) through Gateway with Cognito inbound auth and AgentCore Identity OAuth2 M2M outbound. Reusable pattern for grounding agents in *structured* transaction data alongside the KB's unstructured docs.
- [03-integrations/data-platforms/databricks-dbsql-per-user-delegation](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/data-platforms/databricks-dbsql-per-user-delegation) — per-user identity propagation **from Entra ID** through a Gateway REQUEST interceptor (Lambda, RFC 8693 token exchange) so downstream ACLs apply per user. Directly relevant blueprint for combining our Entra tenant with per-user data access — the same concern the KB's `userContext` ACL filtering addresses.
- [06-workshops/02-AgentCore-gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/02-AgentCore-gateway) — Gateway fundamentals (targets, inbound/outbound auth, semantic tool search); prerequisite skills for wiring a KB target.

## Gaps vs. the summit slides

The summit slide's claims **all hold** against the docs, with two precision notes:

1. **"GA" — confirmed.** GA since 2026-06-17 ([What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-managed-knowledge-base/)); the docs carry no preview markers for the core service.
2. **Connectors — confirmed and slightly understated.** All six announced connectors (S3, Web Crawler, SharePoint, Confluence, Google Drive, OneDrive) are documented; docs add a **Custom** connector and a **Box** topic the slide didn't mention ([connect-ds](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-connect-ds.html)).
3. **"Multi-step agentic retrieval" — confirmed** as `AgenticRetrieveStream` ([devguide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html)), but note the low default quota (60 req/min/account) and the extra planning charge.
4. Unstated on the slide but material: **no LatAm region** ([regions](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-regions.html)) and **embedding model type is immutable** after creation ([create](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-managed-create.html)).

## Open questions for our build plan

- Does `RetrieveAndGenerate` accept a managed KB, or is generation only via `AgenticRetrieveStream` synthesis / DIY on top of `Retrieve`? Needs a hands-on API test.
- Which model does the **service-managed** embedding/reranking/agentic-synthesis use, and is synthesis quality acceptable vs. pinning `foundationModelType: CUSTOM` to a Claude ARN? Test both on our compliance-style multi-hop questions.
- Spanish/multilingual retrieval quality of the managed embedding model (much of our content is Spanish); fallback is custom Cohere Embed Multilingual v3 — but that forfeits the managed reranker.
- SharePoint `Sites.Selected` + ACL flow end-to-end with our Entra tenant: certificate issuance/rotation process, per-site `fullcontrol` grants, and whether InfoSec accepts the permission set.
- Ingestion throughput/latency for our SharePoint corpus and actual monthly cost at our GB volume (verify against the live pricing page).
- `userContext`-based ACL filtering through Gateway: how we map our authenticated app users to SharePoint identities (`userId` = UPN/email?).
- Cross-region data residency: our data would be indexed in us-east-1 — confirm this is acceptable for the compliance team.

Last verified: 2026-08-11
