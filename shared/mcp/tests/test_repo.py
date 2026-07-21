"""Tests for repository discovery/loaders (no MCP SDK required)."""

from __future__ import annotations

import pytest

from shared.mcp import repo


def test_discovers_solution_architect_and_excludes_template():
    names = {a.name for a in repo.discover_agents()}
    assert "solution_architect" in names
    assert "_template" not in names


def test_get_agent_unknown_raises_with_known_list():
    with pytest.raises(ValueError) as exc:
        repo.get_agent("does_not_exist")
    assert "solution_architect" in str(exc.value)


def test_agent_schema_paths_exist():
    agent = repo.get_agent("solution_architect")
    assert agent.has_schema("output")
    assert agent.has_schema("input")
    assert agent.schema_path("output").is_file()


def test_shared_context_lists_and_reads():
    names = repo.list_shared_context()
    assert "org_structure" in names
    assert "data_ai_operating_model" in names
    body = repo.read_shared_context("org_structure")
    assert "Head of Data & Analytics" in body


def test_read_unknown_context_raises():
    with pytest.raises(ValueError):
        repo.read_shared_context("nope")
