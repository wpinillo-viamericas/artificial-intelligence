# AgentCore Identity, Policy, and Guardrails — Verified Reference

**Topic:** How AgentCore secures agents: inbound/outbound auth, JWT propagation, workload identity, token vault, Cedar-based Policy, and where Bedrock Guardrails actually fits.
**Sources consulted (accessed 2026-08-11):**
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-overview.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-getting-started.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/inbound-jwt-authorizer.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-outbound-credential-provider.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html
- https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html
- https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-policy-guardrails-generally-available/
- https://aws.amazon.com/bedrock/agentcore/pricing/
- https://aws.amazon.com/bedrock/agentcore/faqs/

**Related summit note(s):**
- [../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md](../aws-summit-2026/business-cases/2026-07-30_business-cases_agentcore-fintech-orchestration-case.md)
- [../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md](../aws-summit-2026/genai-architectures/2026-07-30_genai-architectures_bedrock-agentcore-platform-overview.md)

The summit notes say what was announced; this note says how it works, verified.

## Verified facts (official docs)

**Status:** Identity **GA**; Policy **GA since 2026-03-03** (was preview from Dec 2025). There is **no separate "AgentCore Guardrails" service** — Guardrails is Amazon Bedrock Guardrails, consumed by AgentCore (see below).

### Identity — inbound auth
- Every AgentCore Runtime and Gateway is fronted by one of two mutually exclusive inbound mechanisms: **IAM SigV4** (default) or a **custom JWT authorizer** (OAuth 2.0 bearer tokens). One runtime version cannot support both simultaneously (devguide/runtime-oauth.html).
- JWT authorizer (`CustomJWTAuthorizerConfiguration`, set at `CreateAgentRuntime`/`CreateGateway`): IdP-agnostic OIDC — **discovery URL** (`.../.well-known/openid-configuration`, must match `iss`), **allowedAudience** (`aud`), **allowedClients** (`client_id`), **allowedScopes**, and **required custom claims** (STRING or STRING_ARRAY with EQUALS / CONTAINS / CONTAINS_ANY — e.g., "group must equal Developer"). At least one criterion required; all provided criteria are verified (devguide/inbound-jwt-authorizer.html).
- `allowedWorkloadConfiguration` on the authorizer can restrict a runtime so **only a specific AgentCore Gateway** can invoke it; for SigV4 runtimes, the same lock-down is done with a resource-based policy allowing only the gateway execution role. This is the documented "gateway as single governed entry point" pattern (Policy + Guardrails + interceptors applied outside agent code).

### Identity — what the agent code actually receives
- On a JWT-authorized invocation, Runtime validates the token, then **exchanges it via `GetWorkloadAccessTokenForJWT`** and delivers a **Workload Access Token** (AWS-signed, opaque, bound to the agent's workload identity + the user identity from the JWT) to the agent code in the payload header `WorkloadAccessToken`.
- The **raw JWT is not forwarded by default.** You can opt in via `RequestHeaderConfiguration` (request-header allowlist) to pass the `Authorization` header through, and decode claims in agent code (signature already validated by Runtime) — devguide/runtime-oauth.html Step 7.
- Alternative header `X-Amzn-Bedrock-AgentCore-Runtime-User-Id` (uses `GetWorkloadAccessTokenForUserId`, requires extra IAM action `bedrock-agentcore:InvokeAgentRuntimeForUser`) exists for customer-managed user IDs, but docs explicitly say it is **unverified against an authenticated identity** — production should use the JWT path.

### Identity — outbound auth
- Model: **delegation, not impersonation** — the agent authenticates as itself (a **workload identity**, auto-created per runtime) carrying verifiable user context.
- **Credential providers** (control plane: `CreateOauth2CredentialProvider`, `CreateApiKeyCredentialProvider`, `CreateWorkloadIdentity`): OAuth2 **2LO** (client credentials, M2M) and **3LO** (authorization code, `USER_FEDERATION`), API keys; vendor configs for Google, GitHub, Slack, Salesforce, Microsoft, Okta, Cognito, custom OIDC. Data plane: `GetWorkloadAccessToken[ForJWT|ForUserId]`, `GetResourceOauth2Token`, `GetResourceApiKey`.
- **Token vault** stores resource tokens keyed by (workload identity, user id from the inbound JWT), so repeat calls skip re-consent until expiry. Agents never hold long-term secrets/refresh tokens.
- Python SDK decorators: `@requires_access_token(provider_name=..., scopes=..., auth_flow="USER_FEDERATION"|M2M, on_auth_url=...)` and `@requires_api_key`.
- Since 2025-10-13, workload-identity permissions come from a service-linked role (`AWSServiceRoleForBedrockAgentCoreRuntimeIdentity`); older agents need the manual `GetWorkloadAccessToken*` IAM policy on the execution role.

### Policy (the platform-control piece the summit slide called "Policy")
- Policy engines hold **deterministic Cedar policies** and attach to **Gateways**; every tool call through the gateway is intercepted and evaluated **outside agent code** before tool access. Principal types: `AgentCore::OAuthUser` (JWT-authenticated users — decisions can use token claims) and `AgentCore::IamEntity`. Fine-grained conditions on user identity **and tool input parameters** (e.g., cap a transfer amount).
- **Natural-language authoring**: English → candidate Cedar, validated against tool schema with automated reasoning (flags overly permissive/restrictive/unsatisfiable policies). Also supports **Dogwood** policies: input-based rules + **session-aware temporal conditions** (e.g., "approval must precede transfer", running budget totals) + information providers.
- **Bedrock Guardrails integration (GA June 2026):** Cedar `when` conditions can reference Guardrails safeguards; Gateway/Policy calls `bedrock:InvokeGuardrailChecks` and injects confidence scores (content safety, prompt attack) into policy evaluation. Gateway execution role needs that permission.
- All policy decisions logged to CloudWatch (audit trail — key for our compliance evidence).

### Guardrails
- Amazon Bedrock **Guardrails is a Bedrock feature, not an AgentCore component**. Documented ways to apply it to AgentCore agents: (1) model-level in agent code (e.g., Strands `BedrockModel(guardrail_config=...)`); (2) gateway-level via the Policy + `InvokeGuardrailChecks` integration above; (3) CloudWatch Logs data-protection policies for telemetry (see observability note).

### Pricing / regions / models
- Identity: **$0.010 per 1,000 token/API-key requests for non-AWS resources; free when used through Runtime or Gateway.** Policy: **$0.000025 per authorization request; NL authoring $0.13 per 1,000 tokens** (pricing page).
- Quotas ([quotas page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html), defaults, adjustable unless noted): 11,000 workload identities/account; 50 credential providers each for OAuth2 / API-key / payment; token-fetch APIs (`GetWorkloadAccessToken*`, `GetResourceOauth2Token`, `GetResourceApiKey`) 200 TPS; provider/identity CRUD 20 TPS. Policy (non-adjustable): 1,000 policy engines/account, 1,000 policies/engine, 10 KB/policy, 400 KB Cedar schema per engine (grows with tool count/parameter complexity — may force separate engines per gateway at scale), authorization via gateway tool-call path.
- Identity is in all AgentCore regions (incl. **us-east-1** and **sa-east-1 São Paulo**). Policy GA'd in 13 regions in March 2026 (São Paulo not among them), but coverage has since expanded: the [current regions page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html) (accessed 2026-08-11) **now lists Policy as available in sa-east-1 (São Paulo)** — 19 regions, GovCloud excluded.
- **Claude support (flagged):** Identity/Policy are model-agnostic control-plane services (FAQ: AgentCore works with any model incl. Anthropic Claude). Official identity samples run on **Claude Haiku 4.5** on Bedrock — no Claude-specific caveats anywhere in the identity/policy docs.

### Verification of the fintech case's identity pattern
Slide claim: *"JWT travels with each agent so it only sees its own client's data."* What AgentCore actually supports:
- **Verified:** JWT validated at Runtime/Gateway per agent (each agent/gateway has its own authorizer incl. per-claim rules); user identity from the JWT is carried into outbound auth (token vault binding) and into Policy decisions (`AgentCore::OAuthUser` claims); the raw JWT *can* be delivered to agent code via the header allowlist; Memory access can be IAM-scoped per namespace/actor. So "each agent sees only its client's data" is **achievable and doc-supported — but it is an engineered composition** (authorizer + Policy conditions + scoped IAM + namespace design), not an automatic platform behavior.
- **Nuance:** naïvely forwarding the *same* user JWT from an orchestrator to every subagent leaks full privileges; AWS's own sample (auth0-multi-agent-obo, below) demonstrates the recommended pattern — **RFC 8693 token exchange** to mint attenuated, least-privilege tokens per subagent. The docs provide no native "auto-propagate JWT across agent-to-agent hops" primitive; each hop is a fresh inbound auth.

## Implementation patterns (samples repo)

- **Runtime inbound + outbound auth (Cognito)** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/03-AgentCore-identity/10-runtime-inbound-outbound-auth — Strands Agents + **Claude Haiku 4.5**, AgentCore CLI; Cognito `CUSTOM_JWT` inbound (401 without bearer), API-key credential provider outbound (key never in env/code). Our template for the first secured agent.
- **Identity workshop (13 modules)** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/03-AgentCore-identity — Python; inbound, outbound 2LO/3LO (Google, GitHub), ECS/Fargate 3LO, Okta three-tier end-to-end, Entra on-behalf-of with MCP runtime, gateway inbound+outbound. `02-how_it_works.md` is the best written explanation of the delegation model.
- **Identity-aware multi-agent financial assistant (Auth0 OBO)** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/05-authenticate-and-authorize/auth0-multi-agent-obo — coordinator/subagent system on Runtime where the coordinator performs **RFC 8693 token exchange** instead of forwarding the user JWT; financial-services vertical. **The closest published implementation of the summit fintech pattern — reuse this architecture for our AML/approval subagents.**
- **Auth feature samples** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-features/05-authenticate-and-authorize — inbound, outbound, m2m-3lo, certificate-based auth, Entra OBO MCP runtime, Okta three-tier demo (Python).
- **Policy workshop** — https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/06-workshops/08-AgentCore-policy — notebooks: getting started (policy engine + gateway), **natural-language policy authoring**, fine-grained access control on Gateway tools. Reuse for tool-level AML/limits policies (Cedar conditions on tool input parameters).

## Gaps vs. the summit slides

- **Platform-overview slide** listed Identity, Policy, Guardrails, AWS Agent Registry under "platform control." Verified: Identity GA and Policy GA (https://aws.amazon.com/about-aws/whats-new/2026/03/policy-amazon-bedrock-agentcore-generally-available/); **Agent Registry is still preview** (https://aws.amazon.com/bedrock/agentcore/faqs/); **"Guardrails" is not an AgentCore component** — it is Bedrock Guardrails integrated at model level or via Policy/Gateway (https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html, https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-agentcore-policy-guardrails-generally-available/). Treat the slide's "Guardrails" box as Bedrock Guardrails, not a new service.
- **Fintech case slide** — "JWT propagated per agent, each agent sees only its client's data": doc-supported but **not automatic**; requires per-agent JWT authorizers, header allowlisting if agent code needs claims, and Policy/IAM scoping; raw-JWT forwarding between agents is an anti-pattern per AWS's own auth0-multi-agent-obo sample (see verification section above; https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html).
- **Regional note:** Policy was absent from São Paulo at its March 2026 GA, but the [current regions page](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html) now shows it available in sa-east-1 — no LatAm gap for Policy anymore.

## Open questions for our build plan

- Hands-on: measure the full chain Cognito/Okta JWT → Runtime authorizer → `WorkloadAccessToken` header → outbound `GetResourceOauth2Token` latency per invocation (matters for our SLAs).
- Test RFC 8693 attenuation with **our** IdP (does Viamericas' IdP support token exchange? Auth0 does in the sample; Cognito's support needs verification).
- Policy: verify Cedar conditions on **tool input parameters** work through our Gateway with MCP tools generated from our internal OpenAPI specs (e.g., "forbid `create_payout` when `amount > X` unless claim `role=supervisor`").
- Confirm whether temporal (Dogwood) policies are GA in all Policy regions (São Paulo now has Policy per the regions page; per-feature parity within Policy is unverified).
- Audit-trail depth: confirm CloudTrail/CloudWatch capture of the (IAM principal ↔ user-id ↔ policy decision) chain satisfies our AML audit requirements end to end.
- Token vault encryption: CMK support and token retention/revocation semantics when a user is offboarded.

Last verified: 2026-08-11
