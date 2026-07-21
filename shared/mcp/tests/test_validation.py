"""Tests for the artifact validation core (no MCP SDK required)."""

from __future__ import annotations

import copy
import json

from shared.mcp import repo, validation

EXAMPLE = (
    repo.AGENTS_DIR / "solution_architect" / "examples" / "output_ga4_funnel.json"
)


def _load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_brief_is_schema_valid_with_no_warnings():
    result = validation.validate_artifact("solution_architect", _load_example())
    assert result.ok, result.errors
    assert result.errors == []
    # The shipped example is a clean golden case: it should trip no advisory checks.
    assert result.warnings == [], result.warnings


def test_missing_required_field_is_an_error():
    brief = _load_example()
    del brief["objective"]
    result = validation.validate_artifact("solution_architect", brief)
    assert not result.ok
    assert any("objective" in e or "required" in e for e in result.errors)


def test_invalid_enum_is_an_error():
    brief = _load_example()
    brief["risks"][0]["severity"] = "catastrophic"  # not in severity enum
    result = validation.validate_artifact("solution_architect", brief)
    assert not result.ok
    assert any("severity" in e for e in result.errors)


def test_recommended_option_mismatch_is_a_warning():
    brief = _load_example()
    brief["recommended_option"]["option_name"] = "Something not offered"
    result = validation.validate_artifact("solution_architect", brief)
    assert result.ok  # schema still valid
    assert any("recommended_option" in w for w in result.warnings)


def test_no_owner_stakeholder_is_a_warning():
    brief = _load_example()
    for s in brief["stakeholders"]:
        s["is_owner"] = False
    result = validation.validate_artifact("solution_architect", brief)
    assert result.ok
    assert any("is_owner" in w for w in result.warnings)


def test_duplicate_handoff_role_is_a_warning():
    brief = _load_example()
    brief["handoffs"].append(copy.deepcopy(brief["handoffs"][0]))
    result = validation.validate_artifact("solution_architect", brief)
    assert result.ok
    assert any("duplicate handoff" in w for w in result.warnings)


def test_extract_handoffs_returns_all_packets_with_request_id():
    brief = _load_example()
    packets = validation.extract_handoffs(brief)
    assert len(packets) == len(brief["handoffs"])
    assert all(p["request_id"] == "REQ-2026-0142" for p in packets)
    assert {p["to_role"] for p in packets} == {
        "digital_analytics",
        "data_governance",
        "data_visualization",
        "project_management",
    }
