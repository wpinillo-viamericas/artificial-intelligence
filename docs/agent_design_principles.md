# Agent Design Principles

These principles apply to **every** agent in this repository. They exist so that the tenth agent is as clean as the first, and so that agents interoperate through their outputs.

## 1. One role, one agent, one job

Each agent maps to exactly one role in the Data & AI org. Its job is the structured, repeatable thinking that role does — not everything that role does. If you find an agent reaching into another role's depth, that is a signal to produce a **handoff** instead.

## 2. Structured I/O is the contract

- Every agent defines an **input schema** and an **output schema** (JSON Schema).
- The structured output is the source of truth; any prose/markdown the agent emits is a *rendering* of that structure.
- Downstream agents consume the structured output, not the prose.
- Schemas that are useful across agents live in `/shared/schemas` and are referenced.

## 3. Surface the unknown; never fabricate

Agents work from real requests that are usually incomplete. The correct behavior when information is missing is to:

- Mark the field as `unknown` / `not_provided`, and
- Add an entry to `open_questions` or `assumptions` (assumptions must be flagged as assumptions),

rather than inventing plausible detail. A confidently wrong brief is worse than an honestly incomplete one.

## 4. Handoff-first outputs

Outputs are designed to be consumed by the *next* role. Each agent produces **handoff packets** addressed to specific downstream roles, each self-contained enough that the receiving role (or its future agent) can start work. This is what makes the system compose.

## 5. Risk is a first-class output

Every agent must be able to say what could go wrong within its domain. Risks carry a **category**, **severity**, **likelihood**, **impact**, and either an **owner** or an explicit **gap** flag. "No known risks" is a valid but rare answer that should be justified.

## 6. Shared ground truth

Facts about the organization, operating model, platforms, and standards live once, in `/shared/context`, and are injected into agent prompts. When the org changes, we update one file. Agents never hardcode org facts in their own prompt.

## 7. Deterministic where it matters

- Classification, enums, and required fields are constrained by schema.
- Model temperature is kept low for architecture reasoning (see each agent's `config.yaml`).
- Anything that must be consistent run-to-run (categories, severities, handoff role names) is drawn from shared enums.

## 8. Testable and evaluable

Every agent ships:

- `examples/` — at least one worked request → output pair.
- `tests/` — golden cases plus an evaluation rubric (what a good output must contain).

A change to a prompt or schema should be validated against these before shipping.

## 9. Versioned and observable

- Each agent's `config.yaml` carries a `version`.
- Prompts change deliberately; breaking output-schema changes bump a major version.
- Outputs carry metadata (agent name, version, timestamp, input reference) so any artifact can be traced back to the run that produced it.

## 10. Human-in-the-loop by default

Agents recommend; roles decide. Outputs are drafts and analyses to be reviewed, edited, and owned by the human in the role. Nothing an agent produces is auto-approved into a system of record.

## Anatomy of an agent folder

```
/agents/<role_name>/
  prompt.md          # System prompt. Composed from /shared/prompts blocks + role logic.
  config.yaml        # Model, params, schema paths, shared-context includes, version.
  schemas/
    input.schema.json
    output.schema.json
  examples/          # request_*.json  +  output_*.json (or .md renderings)
  tests/
    cases.md         # Golden cases + evaluation rubric
  README.md          # What this agent is, how to run it, its contract
```

To create a new agent, copy `/agents/_template/` and fill it in. See [`docs/roadmap.md`](roadmap.md).
