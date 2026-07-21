"""Data & AI Agents MCP server (stdio transport).

Thin MCP layer over the dependency-light core in `repo.py` / `validation.py`.
Every tool here is read-mostly and low-risk (the one write, `render_diagram`,
only regenerates deterministic diagram artifacts) — matching the MVP posture in
the reference architecture's Tooling Layer.

Run:
    python -m shared.mcp.server            # from repo root
    # or via an MCP client config pointing at this module (see README).

Requires the MCP Python SDK:  pip install "mcp[cli]"
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError as exc:  # pragma: no cover - import-time guard
    raise SystemExit(
        "The MCP SDK is not installed. Install it with:\n"
        '    pip install "mcp[cli]"\n'
        "(The core modules shared.mcp.repo / shared.mcp.validation work without it.)"
    ) from exc

from . import repo, validation

mcp = FastMCP("data-ai-agents")

_REGISTRY_PATH = Path(__file__).resolve().parent / "registry.json"


# --------------------------------------------------------------------------- #
# Resources — schemas and shared context, addressable by URI.
# --------------------------------------------------------------------------- #

@mcp.resource("schema://{agent}/{kind}")
def schema_resource(agent: str, kind: str) -> str:
    """An agent's JSON Schema. `kind` is 'input' or 'output'."""
    path = repo.get_agent(agent).schema_path(kind)
    if not path.is_file():
        raise ValueError(f"agent {agent!r} has no {kind} schema")
    return path.read_text(encoding="utf-8")


@mcp.resource("context://{name}")
def context_resource(name: str) -> str:
    """A shared-context ground-truth document (e.g. 'org_structure')."""
    return repo.read_shared_context(name)


# --------------------------------------------------------------------------- #
# Tools
# --------------------------------------------------------------------------- #

@mcp.tool()
def validate_artifact(agent: str, artifact: dict[str, Any] | str, kind: str = "output") -> dict:
    """Validate an artifact against an agent's schema plus consistency checks.

    Returns {ok, agent, schema, errors[], warnings[]}. `errors` are hard schema
    failures; `warnings` are advisory Definition-of-Done gaps. `artifact` may be a
    JSON object or a JSON string.
    """
    if isinstance(artifact, str):
        artifact = json.loads(artifact)
    return validation.validate_artifact(agent, artifact, kind=kind).to_dict()


@mcp.tool()
def list_agents() -> dict:
    """List agents discovered on disk and the governance registry entries."""
    discovered = [
        {"name": a.name, "has_input": a.has_schema("input"), "has_output": a.has_schema("output")}
        for a in repo.discover_agents()
    ]
    registry = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {"discovered": discovered, "registry": registry}


@mcp.tool()
def list_schemas() -> dict:
    """List available schemas (agent input/output) and shared context docs."""
    agents = {
        a.name: [k for k in repo.SCHEMA_KINDS if a.has_schema(k)]
        for a in repo.discover_agents()
    }
    return {
        "agents": agents,
        "shared_context": repo.list_shared_context(),
        "shared_enums": repo.rel(repo.SHARED_SCHEMAS_DIR / "enums.json"),
    }


@mcp.tool()
def get_schema(agent: str, kind: str = "output") -> dict:
    """Return an agent's JSON Schema as a parsed object."""
    path = repo.get_agent(agent).schema_path(kind)
    if not path.is_file():
        raise ValueError(f"agent {agent!r} has no {kind} schema")
    return json.loads(path.read_text(encoding="utf-8"))


@mcp.tool()
def get_shared_context(name: str) -> str:
    """Return a shared-context ground-truth document by name (e.g. 'org_structure')."""
    return repo.read_shared_context(name)


@mcp.tool()
def extract_handoffs(brief: dict[str, Any] | str) -> dict:
    """Extract scoped handoff packets from a Solution Architecture Brief.

    Each packet is self-contained for its target downstream role — the handoff
    contract that a downstream agent's input consumes.
    """
    if isinstance(brief, str):
        brief = json.loads(brief)
    packets = validation.extract_handoffs(brief)
    return {"count": len(packets), "handoffs": packets}


@mcp.tool()
def render_diagram() -> dict:
    """Regenerate the operating-model diagram from palette + template (docs/diagrams).

    Medium-risk (writes generated files) but deterministic from the source of
    truth. Runs the existing docs/diagrams/render.py.
    """
    script = repo.DIAGRAMS_DIR / "render.py"
    if not script.is_file():
        raise ValueError(f"render script not found at {repo.rel(script)}")
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(repo.REPO_ROOT),
    )
    return {
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
