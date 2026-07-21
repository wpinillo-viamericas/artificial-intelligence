%%{init: {"theme":"base","themeVariables":{"fontFamily":"Segoe UI, Helvetica, Arial, sans-serif"}}}%%
flowchart TB

  subgraph optA["Option A — Claude Code sub-agent (tactical | built v0.1)"]
    direction TB
    devA["Developer<br/>Claude Code CLI"]:::intake
    cca["glue-job-monitor<br/>sub-agent | shell tool"]:::built
    creds["set-aws-credentials.ps1<br/>SSO temp credentials (manual)"]:::artifact
    cliA["AWS CLI — Athena<br/>start / poll / get-results"]:::built
    devA --> cca --> creds --> cliA
  end

  subgraph optB["Option B — Amazon Bedrock Agent (target | planned)"]
    direction TB
    devB["Users<br/>Slack / Teams / Chat"]:::intake
    apigw["API Gateway + entry Lambda<br/>phase 2"]:::planned
    agent["Bedrock Agent<br/>Claude model + system prompt"]:::planned
    ag["Action Group<br/>OpenAPI: summary / failures / history"]:::planned
    lam["Lambda (Python)<br/>boto3 Athena client"]:::planned
    kb["Knowledge Base<br/>job docs (optional)"]:::planned
    devB --> apigw --> agent --> ag --> lam
    agent -.->|context| kb
  end

  subgraph data["Shared data layer — AWS us-east-1 (read-only, SELECT)"]
    direction LR
    athena["Athena<br/>query engine"]:::foundation
    tbl["db_iceberg_monitoring.glue_job_runs<br/>Iceberg table on S3"]:::foundation
    s3["S3 athena-results/<br/>query output"]:::foundation
    athena --> tbl
    athena --> s3
  end

  cliA -->|SELECT| athena
  lam -->|SELECT| athena

  iam["IAM role<br/>Athena + S3 + Glue catalog (read)"]:::oversight
  iam -.->|scoped permissions| lam

  report["Report<br/>daily summary + failures + recommendations"]:::artifact
  cliA -.-> report
  lam -.-> report

  subgraph legend["Legend"]
    direction LR
    lbuilt["Built (v0.1)"]:::built
    lplanned["Planned / target"]:::planned
    lartifact["Artifact / credential / output"]:::artifact
    lfound["Shared data layer"]:::foundation
    lgov["Governance / IAM"]:::oversight
  end

  classDef intake fill:{{neutral_light}},stroke:{{neutral}},color:{{ink}},stroke-width:1px;
  classDef built fill:{{primary}},stroke:{{primary_dark}},color:{{on_primary}},stroke-width:2px,font-weight:bold;
  classDef artifact fill:{{accent}},stroke:{{accent_dark}},color:{{on_accent}},stroke-width:2px;
  classDef planned fill:{{surface}},stroke:{{neutral}},color:{{neutral}},stroke-width:1px,stroke-dasharray:5 4;
  classDef foundation fill:{{neutral_light}},stroke:{{neutral}},color:{{ink}},stroke-width:1px;
  classDef oversight fill:{{primary_light}},stroke:{{primary}},color:{{primary_dark}},stroke-width:2px;

  style optA fill:{{surface}},stroke:{{primary}},color:{{ink}}
  style optB fill:{{surface}},stroke:{{neutral}},color:{{ink}}
  style data fill:{{surface}},stroke:{{neutral}},color:{{ink}}
  style legend fill:{{surface}},stroke:{{neutral_light}},color:{{ink}}
