"""Deterministic validation for agent artifacts (briefs / handoff packets).

This is the "cheap code, not LLM calls" validate stage the reference architecture
calls for: schema validity + enum conformance + cross-reference consistency. It
returns two tiers:

  errors   — hard failures (schema-invalid). Must never reach a downstream agent.
  warnings — advisory consistency gaps against the operating model's Definition of
             Done (e.g. no owner among stakeholders). Non-blocking; surfaced so a
             human reviewer or the agent can address them.

Depends only on `jsonschema` + `referencing` (already used by the schema layer),
so it stays importable and testable without the MCP SDK.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from jsonschema import Draft7Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7

from . import repo


@dataclass
class ValidationResult:
    ok: bool
    agent: str
    schema: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _retrieve(uri: str) -> Resource:
    """Resolve a schema `$ref` URI to an on-disk repo file.

    The repo's schemas use `$id`s like
    ``https://data-ai-agents/shared/schemas/enums.json`` and relative refs that
    resolve against them. We map the URI path onto a repo-relative file so any
    schema under the repo is loadable without pre-registration.
    """
    path_part = urlsplit(uri).path.lstrip("/")
    candidate = (repo.REPO_ROOT / path_part).resolve()
    if not candidate.is_file():
        raise FileNotFoundError(f"cannot resolve schema $ref {uri!r} -> {candidate}")
    contents = json.loads(candidate.read_text(encoding="utf-8"))
    return Resource.from_contents(contents, default_specification=DRAFT7)


_registry: Registry = Registry(retrieve=_retrieve)


def _load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_artifact(agent_name: str, artifact: Any, kind: str = "output") -> ValidationResult:
    """Validate an artifact against an agent's JSON Schema plus consistency checks."""
    agent = repo.get_agent(agent_name)
    schema_path = agent.schema_path(kind)
    if not schema_path.is_file():
        raise ValueError(f"agent {agent_name!r} has no {kind} schema at {repo.rel(schema_path)}")

    schema = _load_schema(schema_path)
    validator = Draft7Validator(schema, registry=_registry)

    result = ValidationResult(ok=True, agent=agent_name, schema=repo.rel(schema_path))

    schema_errors = sorted(validator.iter_errors(artifact), key=lambda e: list(e.absolute_path))
    for err in schema_errors:
        location = "/".join(str(p) for p in err.absolute_path) or "(root)"
        result.errors.append(f"{location}: {err.message}")

    # Cross-reference / Definition-of-Done checks only make sense for the
    # Solution Architect brief and only when the shape is roughly right.
    if not result.errors and agent_name == "solution_architect" and kind == "output":
        result.warnings.extend(_brief_consistency_warnings(artifact))

    result.ok = not result.errors
    return result


def _brief_consistency_warnings(brief: dict[str, Any]) -> list[str]:
    """Advisory checks mirroring the operating model's 'what good looks like'."""
    warnings: list[str] = []

    # recommended_option must name one of the solution_options.
    option_names = {o.get("name") for o in brief.get("solution_options", [])}
    recommended = (brief.get("recommended_option") or {}).get("option_name")
    if recommended and recommended not in option_names:
        warnings.append(
            f"recommended_option.option_name {recommended!r} does not match any "
            "solution_options[].name"
        )

    # DoD: at least one accountable owner among stakeholders (or flagged as gap).
    stakeholders = brief.get("stakeholders", [])
    if stakeholders and not any(s.get("is_owner") for s in stakeholders):
        warnings.append(
            "no stakeholder is marked is_owner=true — the brief should name an "
            "accountable owner or flag the gap in risks/open_questions"
        )

    # DoD: non-measurable success metrics should surface an open question.
    non_measurable = [m for m in brief.get("success_metrics", []) if m.get("measurable") is False]
    if non_measurable and not brief.get("open_questions"):
        warnings.append(
            f"{len(non_measurable)} success metric(s) marked measurable=false but "
            "there are no open_questions to resolve them"
        )

    # Duplicate handoff targets suggest a modeling error.
    roles = [h.get("to_role") for h in brief.get("handoffs", [])]
    dupes = sorted({r for r in roles if roles.count(r) > 1 and r})
    if dupes:
        warnings.append(f"duplicate handoff to_role entries: {', '.join(dupes)}")

    # Handoff-first: a brief with delivery dependencies but no handoffs is suspect.
    if brief.get("delivery_dependencies") and not brief.get("handoffs"):
        warnings.append(
            "delivery_dependencies are present but there are no handoffs — "
            "downstream roles cannot start"
        )

    return warnings


def extract_handoffs(brief: dict[str, Any]) -> list[dict[str, Any]]:
    """Return handoff packets from a brief, each self-contained for its target role.

    This is the handoff contract in code: the output that a downstream agent's
    input consumes. Ordering is preserved from the brief.
    """
    handoffs = brief.get("handoffs")
    if not isinstance(handoffs, list):
        raise ValueError("brief has no 'handoffs' array")

    request_id = (brief.get("meta") or {}).get("request_id")
    packets: list[dict[str, Any]] = []
    for h in handoffs:
        packet = dict(h)
        if request_id and "request_id" not in packet:
            packet["request_id"] = request_id
        packets.append(packet)
    return packets
