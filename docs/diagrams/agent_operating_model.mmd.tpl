%%{init: {"theme":"base","themeVariables":{"fontFamily":"Segoe UI, Helvetica, Arial, sans-serif"}}}%%
flowchart TB

  intake["Business / technical request"]:::intake
  sa["Solutions Architecture Agent<br/>Solution Architect | built v0.1"]:::built
  brief["Solution Architecture Brief<br/>handoff contract: output schema = downstream input"]:::artifact
  hitl(["Solution Architect review<br/>human-in-the-loop | owns and approves"]):::hitl

  intake --> sa --> brief --> hitl

  subgraph downstream["Downstream role agents (planned)"]
    direction TB
    de["Data Engineering Agent"]:::planned
    da["Digital Analytics Agent"]:::planned
    dg["Data Governance Agent"]:::planned
    dv["Data Visualization Agent"]:::planned
    ds["Data Science Agent"]:::planned
    dq["Data Assurance Agent"]:::planned
    va["Value Assurance Agent"]:::planned
    pm["Project Management Agent"]:::planned
  end

  hitl -->|handoff| de
  hitl -->|handoff| da
  hitl -->|handoff| dg
  hitl -->|handoff| dv
  hitl -->|handoff| ds
  hitl -->|handoff| dq
  hitl -->|handoff| va
  hitl -->|handoff| pm

  subgraph foundation["Shared foundation (/shared)"]
    direction LR
    ctx["context<br/>org and operating model"]:::foundation
    sch["schemas<br/>enums and contracts"]:::foundation
    prm["prompts<br/>base agent"]:::foundation
    utl["utils<br/>runner, validator, router"]:::foundation
  end

  foundation -.->|shared ground truth| sa
  foundation -.-> downstream

  head["Head of Data and Analytics<br/>strategy | prioritization | governance"]:::oversight
  head -.->|prioritize and oversee| sa
  brief -.->|portfolio view| head

  subgraph legend["Legend"]
    direction LR
    lbuilt["Built (v0.1)"]:::built
    lplanned["Planned"]:::planned
    lartifact["Artifact / contract"]:::artifact
    lfound["Shared foundation"]:::foundation
  end

  classDef intake fill:{{neutral_light}},stroke:{{neutral}},color:{{ink}},stroke-width:1px;
  classDef built fill:{{primary}},stroke:{{primary_dark}},color:{{on_primary}},stroke-width:2px,font-weight:bold;
  classDef artifact fill:{{accent}},stroke:{{accent_dark}},color:{{on_accent}},stroke-width:2px;
  classDef hitl fill:{{primary_light}},stroke:{{primary}},color:{{ink}},stroke-width:1px;
  classDef planned fill:{{surface}},stroke:{{neutral}},color:{{neutral}},stroke-width:1px,stroke-dasharray:5 4;
  classDef foundation fill:{{neutral_light}},stroke:{{neutral}},color:{{ink}},stroke-width:1px;
  classDef oversight fill:{{primary_light}},stroke:{{primary}},color:{{primary_dark}},stroke-width:2px;

  style downstream fill:{{surface}},stroke:{{neutral}},color:{{ink}}
  style foundation fill:{{surface}},stroke:{{neutral}},color:{{ink}}
  style legend fill:{{surface}},stroke:{{neutral_light}},color:{{ink}}
