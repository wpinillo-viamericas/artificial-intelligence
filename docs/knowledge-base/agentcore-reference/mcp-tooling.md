# MCP Tooling for Our AgentCore + Claude Code Workflow

**Topic:** The AWS MCP server landscape (open-source catalog, the managed AWS MCP Server, and the AgentCore MCP server) and which ones to wire into Claude Code for developing AgentCore agents.
**Sources consulted (accessed 2026-08-11):**
- https://awslabs.github.io/mcp/ (AWS open-source MCP servers catalog)
- https://awslabs.github.io/mcp/servers/bedrock-kb-retrieval-mcp-server
- https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html
- https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/mcp-getting-started.html
- https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available/ (via search; page not fetched)
- https://github.com/awslabs/mcp (server sources)

**Sources consulted (accessed 2026-08-21):**
- https://awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server (current AgentCore MCP server tool surface + install configs)
- https://pypi.org/project/awslabs.amazon-bedrock-agentcore-mcp-server/ (version and release history)
- https://github.com/awslabs/mcp/blob/main/src/amazon-bedrock-agentcore-mcp-server/CHANGELOG.md (via PyPI; use for re-verification diffs)

**Related summit note(s):** [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_agentcore-gateway-mcp.md) — the summit note says what was announced (Gateway as one MCP endpoint for agents at runtime); this note covers the complementary **development-time** MCP tooling, verified.

> Distinction that matters: **AgentCore Gateway** is the MCP endpoint your *deployed agents* call in production. The servers below are MCP tools your *coding assistant* (Claude Code) uses while you build those agents. Registration status: **#1 (AgentCore MCP server) registered 2026-08-21** — local (per-user) scope, `AWS_PROFILE=via-dev` (dev account, never `via-prod`), pinned `0.1.4`, `AGENTCORE_DISABLE_TOOLS=browser,code_interpreter`. Servers #2 and #3 remain document-only.

## Verified facts (official docs)

### 1. The managed AWS MCP Server (Agent Toolkit for AWS)

Per the [Agent Toolkit userguide](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html):

- A **managed remote MCP server** — single endpoint, no local server code to maintain. Endpoints: `https://aws-mcp.us-east-1.api.aws/mcp` (us-east-1) and `https://aws-mcp.eu-central-1.api.aws/mcp` (eu-central-1). The endpoint region is where the server runs; the `AWS_REGION` metadata sets the default region for operations (defaults to `us-east-1`).
- Capabilities: **AWS documentation search without authentication**; with IAM credentials, **AWS API execution**, **sandboxed Python script execution**, and **curated skills** (tools like `aws___search_documentation`, `aws___retrieve_skill`).
- Governance: **CloudWatch metrics**, **IAM-based access controls** (incl. condition keys, read-only mode under SigV4), and **CloudTrail logging of all API calls**.
- Two auth modes ([setup page](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)): **OAuth 2.1** (browser sign-in; needs the `AWSMCPSignInOAuthAccessPolicy` managed policy; tokens 1 h, auto-refresh up to 12 h; no multi-account switching) or **SigV4** via the local proxy [`mcp-proxy-for-aws`](https://github.com/aws/mcp-proxy-for-aws) (uvx-launched stdio proxy; supports multi-profile/cross-account and read-only mode; recommended for terminal coding agents like Claude Code).
- AWS recommends **removing** the older `aws-api-mcp-server` and `aws-knowledge-mcp-server` entries when adopting it, to avoid tool conflicts.
- GA per the [AWS News blog](https://aws.amazon.com/blogs/aws/the-aws-mcp-server-is-now-generally-available/) (surfaced via search).

### 2. The AgentCore MCP server ("vibe coding with your coding assistant")

Per the [catalog page](https://awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server) (accessed 2026-08-21) and the [AgentCore devguide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/mcp-getting-started.html):

- Local uvx-run server: `awslabs.amazon-bedrock-agentcore-mcp-server` — current release **0.1.4** (2026-08-10; 28 releases since 2025-10, [CHANGELOG](https://github.com/awslabs/mcp/blob/main/src/amazon-bedrock-agentcore-mcp-server/CHANGELOG.md)).
- **Surface expanded massively since first documented here (2026-08-11 revision said 2 doc tools — the devguide lagged the package).** As of 0.1.4: **122 tools across 8 primitives** (runtime, memory, identity, gateway, policy, browser, code interpreter, documentation), the operational ones backed by real boto3 control-plane calls made with the developer's local AWS credentials. Current per-primitive breakdown: ask the server's own `search_agentcore_docs` tool or see the [catalog page](https://awslabs.github.io/mcp/servers/amazon-bedrock-agentcore-mcp-server) — not mirrored here.
- The 2 documentation tools need **no AWS credentials** and remain safe to auto-approve; the other 120 use local credentials (`AWS_PROFILE` / access keys / IAM role) — **IAM permissions on the profile are the guardrail**. Data-plane operations that would return credentials are intentionally excluded so secrets never enter LLM context.
- Tool scoping via env vars: `AGENTCORE_ENABLE_TOOLS=memory,runtime,identity` (allowlist) **or** `AGENTCORE_DISABLE_TOOLS=browser,code_interpreter` (denylist).
- Workflow it enables from Claude Code/Cursor/Kiro/Q: **transform** an existing agent to AgentCore Runtime compatibility (adds `from bedrock_agentcore.runtime import BedrockAgentCoreApp`, `app = BedrockAgentCoreApp()`, `@app.entrypoint`, `app.run()`), then **deploy** and **invoke** it by driving the AgentCore CLI.
- Prerequisites: `uv` installed + Python 3.10+ (`uv python install 3.10`), AWS account with AgentCore permissions; for the deploy loop also **Node.js 20+** (AgentCore CLI: `npm install -g @aws/agentcore`), AWS CLI with credentials, `pip install bedrock-agentcore`.
- ⚠️ **Security note (payments context):** the jump from read-only doc search to full control-plane access (create/delete runtimes, gateways, identity providers, token vault) changes the InfoSec review for this server. Mitigations: least-privilege IAM on the dev profile, `AGENTCORE_*_TOOLS` scoping, and pinning the reviewed version (snippets below pin `0.1.4`; bump deliberately — read the changelog, re-verify, update the "Describes" footer).

### 3. The open-source catalog (awslabs.github.io/mcp) — servers relevant to our stack

Standard install pattern: `{"command": "uvx", "args": ["awslabs.<server-name>@latest"]}` with AWS credentials via `AWS_PROFILE`/`AWS_REGION` env vars. Servers relevant to us (one-liners per the catalog):

| Server | Type | One-liner |
|---|---|---|
| AWS MCP (managed, preview→GA) | Remote | Secure, auditable AWS operations: API access, docs, skills, CloudTrail logging (see §1) |
| AWS Knowledge MCP Server | Remote, **no auth** | Latest AWS docs, code samples, official content at `https://knowledge-mcp.global.api.aws`; aggressively rate-limited (~1 req/15 s per IP per [issue #2949](https://github.com/awslabs/mcp/issues/2949)) |
| AWS Documentation MCP Server | Local uvx | Current AWS docs and API references (local alternative to Knowledge) |
| Amazon Bedrock Knowledge Bases Retrieval | Local uvx | Query Bedrock KBs in natural language with citations; `uvx awslabs.bedrock-kb-retrieval-mcp-server@latest`; env: `AWS_PROFILE`, `AWS_REGION`, optional `KB_INCLUSION_TAG_KEY`, `BEDROCK_KB_RERANKING_ENABLED` |
| Amazon Bedrock AgentCore MCP Server | Local uvx | 122 tools: full AgentCore control plane (runtime, memory, identity, gateway, policy, browser, code interpreter) + doc search — see §2 |
| AWS Pricing MCP Server | Local uvx | Pre-deployment cost estimation and optimization |
| AWS Billing and Cost Management | Local uvx | Cost analysis of the running account |
| AWS Lambda Tool MCP Server | Local uvx | Execute Lambda functions as AI tools (reach private VPC resources) |
| AWS Cloud Control API MCP Server | Local uvx | CRUD on AWS resources with integrated security scanning |
| AWS Serverless MCP Server | Local uvx | Full serverless app lifecycle with SAM CLI |
| Amazon SageMaker AI MCP Server | Local uvx | SageMaker resource management and model development |

Note: the managed AWS MCP Server subsumes the Documentation/Knowledge/API servers' roles; prefer it and add the specialized ones (KB Retrieval, Lambda Tool, Pricing) only when needed. Exact uvx package names other than the two verified above should be copied from each server's page under https://awslabs.github.io/mcp/ at install time.

## Implementation patterns (samples repo)

- [06-workshops/02-AgentCore-gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/02-AgentCore-gateway) — turn OpenAPI/Smithy APIs and Lambda functions into MCP tools with inbound OAuth + outbound API-key/IAM/OAuth auth and built-in **semantic tool search**. This is the production counterpart of the summit Gateway slide; what we'd use for payments-status/compliance/FX tools.
- [06-workshops/01-AgentCore-runtime/02-hosting-MCP-server](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/01-AgentCore-runtime) — host your **own** MCP server on AgentCore Runtime (when a tool needs custom logic rather than a Gateway target).
- [03-integrations/data-platforms/databricks-dbsql-agentcore-gateway](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/data-platforms/databricks-dbsql-agentcore-gateway) — attach an external vendor's managed MCP server behind Gateway with AgentCore Identity handling OAuth2 M2M; the template for any third-party MCP service we adopt.
- [13-AgentCore-payments tutorial 04 (Coinbase Bazaar via Gateway)](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/13-AgentCore-payments) — discovering 10,000+ paid MCP tools through Gateway and paying per call (x402); shows Gateway as an MCP *marketplace* client.

## Top 3 for our workflow (Claude Code + AgentCore development) — registration snippets

**Do not run these yet — documented for when we decide to register.** Project-scope `.mcp.json` lives at the repo root; `claude mcp add` defaults to local (per-user) scope, add `--scope project` to share via `.mcp.json`.

### #1 — AgentCore MCP server (AgentCore control plane + docs inside Claude Code)

Pinned to the version this note describes (`0.1.4`) — not `@latest` — so what gets installed is what was reviewed. Bump the pin deliberately (changelog → re-verify → update footer).

```bash
claude mcp add bedrock-agentcore --env AWS_PROFILE=default --env AWS_REGION=us-east-1 -- uvx awslabs.amazon-bedrock-agentcore-mcp-server@0.1.4
```

`.mcp.json` equivalent — **Windows variant** (per the catalog page, uses `uv tool run` with the `.exe` entry point; our dev machines are Windows 11). `AGENTCORE_DISABLE_TOOLS` trims the two primitives we have no near-term use for:

```json
{
  "mcpServers": {
    "bedrock-agentcore": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "tool", "run",
        "--from", "awslabs.amazon-bedrock-agentcore-mcp-server@0.1.4",
        "awslabs.amazon-bedrock-agentcore-mcp-server.exe"
      ],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR",
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "AGENTCORE_DISABLE_TOOLS": "browser,code_interpreter"
      }
    }
  }
}
```

Linux/macOS/CI equivalent: `"command": "uvx", "args": ["awslabs.amazon-bedrock-agentcore-mcp-server@0.1.4"]`, same `env`.

Why first: purpose-built for our exact loop (transform → deploy → test AgentCore agents from the editor). Only the 2 doc tools are read-only/credential-free; the other 120 act on AWS with the local profile — see the §2 security note before registering. Requires `uv` installed and the AgentCore CLI for the deploy steps.

### #2 — AWS MCP Server (managed; docs search + governed AWS API access)

OAuth variant (simplest; verbatim from the [AWS setup page](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)):

```bash
claude mcp add aws-mcp https://aws-mcp.us-east-1.api.aws/mcp --transport http
```

SigV4 variant (multi-account, read-only mode; verbatim from the same page):

```bash
claude mcp add-json aws-mcp '{"type":"stdio","command":"uvx","args":["mcp-proxy-for-aws@1.6.4","https://aws-mcp.us-east-1.api.aws/mcp","--metadata","AWS_REGION=us-east-1"],"env":{}}'
```

`.mcp.json` equivalents:

```json
{
  "mcpServers": {
    "aws-mcp": {
      "type": "http",
      "url": "https://aws-mcp.us-east-1.api.aws/mcp"
    }
  }
}
```

```json
{
  "mcpServers": {
    "aws-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws@1.6.4",
        "https://aws-mcp.us-east-1.api.aws/mcp",
        "--metadata", "AWS_REGION=us-east-1"
      ],
      "env": {}
    }
  }
}
```

Why: one endpoint covers docs search (unauthenticated), AWS API calls, sandboxed Python, and skills — with IAM guardrails and CloudTrail audit, which matters in a payments company. OAuth needs `AWSMCPSignInOAuthAccessPolicy` attached to the IAM principal; SigV4 needs AWS CLI ≥ 2.32.0 + `uv`. We used `AWS_REGION=us-east-1` (our AgentCore/managed-KB region) instead of the doc's `us-west-2` example value.

### #3 — Bedrock Knowledge Bases Retrieval (query our KBs from Claude Code)

```bash
claude mcp add bedrock-kb-retrieval --env AWS_PROFILE=default --env AWS_REGION=us-east-1 -- uvx awslabs.bedrock-kb-retrieval-mcp-server@latest
```

`.mcp.json` equivalent:

```json
{
  "mcpServers": {
    "bedrock-kb-retrieval": {
      "type": "stdio",
      "command": "uvx",
      "args": ["awslabs.bedrock-kb-retrieval-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1",
        "KB_INCLUSION_TAG_KEY": "mcp-multirag-kb",
        "BEDROCK_KB_RERANKING_ENABLED": "false"
      }
    }
  }
}
```

Why: once the managed KB over SharePoint/OneDrive exists, this lets us ask our own corpus questions while coding (discovery, NL query, source filtering, reranking). Becomes useful at that point, not before. Caveat: its docs predate Managed Knowledge Bases — verify it lists/queries `type: MANAGED` KBs (open question below).

## Gaps vs. the summit slides

The related summit slide covered **AgentCore Gateway**, not dev-time MCP servers, and its claims stand: [Gateway docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html) confirm OpenAPI/Smithy + Lambda targets and MCP `listTools`/`invokeTool`/semantic search. Two refinements from the docs:

1. The slide's four target types (API, Lambda, internet search, other agents) are directionally right; the workshop README ([06-workshops/02](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/02-AgentCore-gateway)) documents **Lambda ARNs and OpenAPI/Smithy specs** as target types, and the devguide adds **connector targets** (e.g., [Managed Knowledge Bases](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-target-connector-managed-kb.html)). The slide's "web search" and "other agents" boxes are already resolved in [gateway.md](./gateway.md): web search is a **built-in Web Search Tool**, not an attachable target, and other agents are fronted via **HTTP passthrough targets (incl. A2A)**, not MCP aggregation.
2. Transport is **Streamable HTTP only** (workshop README) — relevant when choosing MCP client libraries.

## Open questions for our build plan

- Does `awslabs.bedrock-kb-retrieval-mcp-server` support **Managed** KBs (`Retrieve` works against them?) or only classic vector-store KBs? Hands-on test after we create the first managed KB.
- AWS MCP Server OAuth vs SigV4 in our org: is `signin:AuthorizeOAuth2Access` permitted by our SCPs, and do we want read-only mode (SigV4-only feature) as the default for developers?
- AWS MCP Server managed endpoint runs in us-east-1/eu-central-1 — confirm InfoSec is comfortable with prompts/tool traffic transiting it, and what CloudTrail events look like in practice.
- Exact uvx package names for Pricing/Billing/Lambda Tool/Cloud Control/Serverless/SageMaker servers (catalog page verified the servers exist; copy install strings from each server page when adopting).
- ~~Whether to pin `mcp-proxy-for-aws` (docs pin `1.6.4`) or track latest.~~ **Resolved 2026-08-21: pin.** The AgentCore server's silent 2→122 tool expansion is the case study — an MCP server's tool surface is security-relevant, so pin reviewed versions everywhere (keep `mcp-proxy-for-aws@1.6.4`, AgentCore server `@0.1.4`) and bump deliberately via changelog review.
- Least-privilege IAM for the AgentCore server's 120 operational tools: which `bedrock-agentcore:*` actions do the Runtime/Memory/Identity/Gateway/Policy primitives actually call, and what does a scoped developer role look like? Enumerate before registering with a credentialed profile.
- Do `AGENTCORE_ENABLE_TOOLS`/`AGENTCORE_DISABLE_TOOLS` accept exactly the primitive names listed in §2 (e.g., `code_interpreter` spelling)? Confirm against the server README at install time.

Describes: `awslabs.amazon-bedrock-agentcore-mcp-server` **0.1.4** (released 2026-08-10). To re-verify: diff [PyPI latest](https://pypi.org/project/awslabs.amazon-bedrock-agentcore-mcp-server/) against this line and skim the [CHANGELOG](https://github.com/awslabs/mcp/blob/main/src/amazon-bedrock-agentcore-mcp-server/CHANGELOG.md) between the two versions.
Last verified: 2026-08-21
