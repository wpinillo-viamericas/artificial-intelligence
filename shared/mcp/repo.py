"""Repository layout resolution and artifact loaders for the Data & AI MCP server.

Dependency-light (stdlib only) so it stays independently testable without the
MCP SDK installed. Discovers agents by filesystem convention rather than parsing
`config.yaml`, keeping this module free of a YAML dependency — the schemas live at
a fixed path under each agent folder.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# shared/mcp/repo.py -> parents[2] == repo root
REPO_ROOT = Path(__file__).resolve().parents[2]

AGENTS_DIR = REPO_ROOT / "agents"
SHARED_CONTEXT_DIR = REPO_ROOT / "shared" / "context"
SHARED_SCHEMAS_DIR = REPO_ROOT / "shared" / "schemas"
DIAGRAMS_DIR = REPO_ROOT / "docs" / "diagrams"

# Directories under /agents that are not real agents.
_NON_AGENT_DIRS = {"_template"}

SCHEMA_KINDS = ("input", "output")


@dataclass(frozen=True)
class AgentInfo:
    """A role-specific agent discovered on disk."""

    name: str
    dir: Path

    def schema_path(self, kind: str) -> Path:
        if kind not in SCHEMA_KINDS:
            raise ValueError(f"unknown schema kind {kind!r}; expected one of {SCHEMA_KINDS}")
        return self.dir / "schemas" / f"{kind}.schema.json"

    def has_schema(self, kind: str) -> bool:
        return self.schema_path(kind).is_file()


def discover_agents() -> list[AgentInfo]:
    """Return agents that ship an output schema, sorted by name.

    An agent is any subdirectory of /agents (excluding templates) that has an
    output schema — the minimum needed for structured-I/O validation.
    """
    if not AGENTS_DIR.is_dir():
        return []
    agents: list[AgentInfo] = []
    for child in sorted(AGENTS_DIR.iterdir()):
        if not child.is_dir() or child.name in _NON_AGENT_DIRS:
            continue
        info = AgentInfo(name=child.name, dir=child)
        if info.has_schema("output"):
            agents.append(info)
    return agents


def get_agent(name: str) -> AgentInfo:
    """Return a single agent by name, or raise ValueError with the known set."""
    for agent in discover_agents():
        if agent.name == name:
            return agent
    known = ", ".join(a.name for a in discover_agents()) or "(none found)"
    raise ValueError(f"unknown agent {name!r}; known agents: {known}")


def list_shared_context() -> list[str]:
    """Names (without extension) of the shared-context ground-truth documents."""
    if not SHARED_CONTEXT_DIR.is_dir():
        return []
    return sorted(p.stem for p in SHARED_CONTEXT_DIR.glob("*.md"))


def read_shared_context(name: str) -> str:
    """Return the markdown body of a shared-context document by stem name."""
    path = SHARED_CONTEXT_DIR / f"{name}.md"
    if not path.is_file():
        known = ", ".join(list_shared_context()) or "(none found)"
        raise ValueError(f"unknown shared-context doc {name!r}; known: {known}")
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    """Repo-relative POSIX path string, for stable cross-platform reporting."""
    return path.relative_to(REPO_ROOT).as_posix()
