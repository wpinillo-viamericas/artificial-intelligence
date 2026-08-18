# AI Acceptable Use and Data Protection Policy

> **Source:** `20260325 POL-XYZ-0001 - AI Acceptable Use and Data Protection Policy.docx` (original kept outside git; see folder README)
> **Type:** policy | **Status:** Approved 2026-03-25 (v1.0, POL-XYZ-0001)
> **Extracted to markdown:** 2026-08-18 (automated text extraction; formatting simplified, images/charts omitted)

---

VIAMERICAS CORPORATION

AI Acceptable Use and Data Protection Policy

DOCUMENT TYPE: POLICY

WORK DOMAIN: AI

REVISION: 1.0

AREA: TBD

| Approving authority: | CEO, EVP, Chairman |
|---|---|
| Prepared by: | CISO, CCO, Head of Data & AI |
| Date Prepared: Reviewed by: Last Date Reviewed: Approved by: Approval Date: | 03/25/2026 CISO, CCO, CEO, EVP, Chairman, Head of Data & AI 03/25/2026 CEO, EVP, Chairman XX/XX/2026 |

## Background

Artificial intelligence tools are increasingly being used in normal business operations for drafting, summarization, research, analysis, and workflow support. Internal discussions have also made clear that Viamericas does not want a policy that limits AI use to only “manual innocuous prompts.” Rather, management prefers a framework that allows employees to use approved AI technologies in a practical way, including more advanced use cases and, where specifically authorized and properly controlled, workflows that may involve nonpublic or otherwise sensitive information.

At the same time, AI tools introduce material risks if used without defined guardrails. These risks include unauthorized disclosure of sensitive information, loss of confidentiality, inaccurate or misleading outputs, improper use of customer or employee data, regulatory non-compliance, and insufficient auditability over business processes. For that reason, the Company is adopting this policy to define how approved AI technologies may be used, what data may or may not be entered into those tools, when masking, tokenization, redaction, or other safeguards are required, what technical and administrative controls must be in place, and what training and oversight employees must complete before using AI for Company business.

## Purpose

This policy enables the safe and productive use of approved AI technologies in Viamericas while protecting customer, employee, agent, payer, vendor, and company data and meeting information security, privacy, legal, contractual, and records-management obligations.

## Scope

This policy applies to all employees, contractors, temporary staff, and third parties using AI tools or AI-enabled features for company business.

## Policy

## Approved AI Services

Only AI services approved by Data & AI, IT, Security, Compliance, and Legal and provisioned through company-managed accounts, tenants, or cloud environments may be used for company business. Personal or consumer AI accounts may not be used for any type of company data, company documents, or company workflows.

- The company will maintain a list of approved AI services, and it will be reviewed periodically to ensure its accuracy and alignment with business needs.

## Data Classification and Use Rules

Company data may be used in AI tools only as follows:

- Public information may be used in approved AI enterprise services for authorized business purposes.

- Confidential data may be used only in approved enterprise AI services with company-managed access controls, logging, retention controls, and vendor no-training settings enabled where available.

- Restricted data may not be entered or uploaded in raw form into general-purpose AI chat interfaces. Restricted data may be used only when:

- It has been masked, tokenized, redacted, or otherwise sanitized using approved methods; or

- The use case has been specifically approved for a company-controlled private or API-based AI environment with documented controls.

- Credentials, private keys, access tokens, MFA secrets, and card verification values (CVV/CVC) must never be entered into any AI tool.

- Any questions about specific data types and whether they can be used on AI or not, should be reviewed with Information Security, Data & AI or IT.

The following matrix contains details of different data categories and how they should be used in AI applications:

| Category | Examples | Default Rule |
|---|---|---|
| Government and identity data | SSN, taxpayer ID, passport, driver’s license, national ID, full DOB when linked to identity. | Never upload raw to general AI chat tools; mask/tokenize or use approved private workflow. |
| Financial account and payment data | Bank account/routing, card PAN, expiration date, CVV/CVC, payment tokens that can be reversed. | No raw upload to general AI chat tools; CVV/CVC never permitted. |
| Transaction and remittance data | Sender/receiver details, transaction histories, balances, dispute notes, fraud markers, ViaCheck data. | Mask/tokenize by default; raw use only in approved private/API workflow. |
| Legal, compliance, and investigative data | Subpoenas, AML/KYC files, sanctions screening results, investigations, examinations / regulatory correspondence. | Need-to-know only; enterprise/private approved workflow only. |
| Credentials and security-sensitive data | Passwords, MFA seeds, API keys, tokens, private keys, secrets, incident-response evidence. | Never upload to any AI tool. |
| Sensitive HR / special category data | Health, biometrics, minors, payroll, employee relations matters. | Enterprise/private approved workflow only; sanitize whenever possible. |
| Confidential company data | Operational processes, source code, security architecture, audit results, nonpublic financials, contracts, unreleased strategy. | Enterprise/private approved workflow only. |

## Permitted Uses

- Permitted uses of AI include Drafting, summarization, translation, classification, coding assistance, internal research, knowledge retrieval over approved content, and approved workflow automation.

- The list of permitted AI uses will be periodically reviewed to ensure a risk-based approach that balances the need for innovation with information security, data management, regulations, and internal policies.

## Prohibited Uses

- Uploading raw Restricted Data to general AI chat tools.

- Using conversational AI outputs as final legal, compliance, fraud, underwriting, HR, or disciplinary decisions without documented human review.

- Bypassing records retention, privacy, information security, IT, or contractual restrictions.

- Connecting unapproved data sources, plugins, GPTs, agents, or external connectors to company data.

- Publishing company data to public or externally shared AI workspaces.

- Representing AI-generated output as verified fact without appropriate review.

## AI Development, Agents, and API Use

Teams developing AI-enabled applications, copilots, agents, or API integrations must perform an architecture and security review before production use. At a minimum, designs must address:

- Data classification and approved data sources.

- Secrets management.

- Prompt and response logging where legally permissible.

- Input/output filtering and sensitive-data controls (Guardrails).

- Prompt-injection and data-exfiltration defenses.

- Output validation and human approval gates where required.

- Retention, deletion, and auditability.

## Human Accountability

- AI output is an assistive technology. The employee or team using the AI remains responsible for the accuracy, legality, confidentiality, and appropriateness of the output and any downstream decision or action.

## Training and Acknowledgement

- Training is required before access is granted and annually thereafter. Training must cover approved tools, prohibited data categories, masking / tokenization / redaction methods, prompt hygiene, output verification, and incident reporting.

- Users must acknowledge this policy before access is provisioned.

## Appendices

## Glossary

- Approved AI Service: An AI product, feature, or API that has been reviewed and authorized by the Company and is operated under a company-managed account, tenant, or cloud environment.

- Consumer AI Account: A personal or public AI account that is not managed by the Company. Consumer accounts may not be used for Company data under any circumstances.

- Private AI Environment: A company-controlled AI deployment or cloud environment in which the Company manages access, logging, retention, and data-handling controls.

- API-Based AI Workflow: A company-built or company-approved integration that uses AI through an application programming interface instead of a public chat interface, with security, audit, and workflow controls.

- Prompt / Input: The text, file, image, instructions, metadata, or other content submitted to an AI tool.

- Output / Response: Any text, code, summary, classification, recommendation, or other content generated by an AI tool.

- Personally Identifiable Information (PII): Information that identifies, or can reasonably be used to identify, a specific individual.

- Nonpublic Personal Information (NPPI): Nonpublic personal information relating to a consumer or customer, including nonpublic personal financial or transactional information.

## Related Policies, Plans, Standard Operating Procedures, and Guidelines

- N/A

## Monitoring, Reporting, and Exceptions

Use of Viamericas AI tools may be logged and monitored for security, compliance, and operational purposes, consistent with applicable law and company policy. Any suspected misuse, accidental upload of Restricted Data, or unexpected model behavior involving company data must be reported immediately to Information Security, Data & AI, Compliance, and IT.

## Enforcement

Violations of this policy may result in suspension of AI access, disciplinary action, incident response, customer or regulator notification where required, and any other action required by law or company policy.

## Contact

For further information and advice about this policy contact:

Contact 1

Email:

Contact 2

Email:

## History/Revision Dates

| Version No | Date of Approval | Approving Authority | Summary of Changes |
|---|---|---|---|
| 001 | 03/25/2026 | CEO, EVP, Chairman | First version of Viamericas AI Acceptable Use and Data Protection Policy |
