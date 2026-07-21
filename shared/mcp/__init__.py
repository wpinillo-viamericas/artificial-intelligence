"""Internal Data & AI Agents MCP server.

Exposes the repo's structured substrate — schemas, shared context, artifact
validation, handoff extraction, the governance registry, and diagram rendering —
as MCP tools and resources reusable across every agent and IDE surface.

The core modules (`repo`, `validation`) depend only on stdlib + jsonschema and
are importable/testable without the MCP SDK. `server` adds the thin MCP layer.
"""

__all__ = ["repo", "validation"]
