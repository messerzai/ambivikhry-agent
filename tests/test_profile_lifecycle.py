import json

import pytest

from ambivikhry.memory import JsonMemory


def test_corrected_item_is_replaced_and_recorded(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.personalize("initial", {"preferences": ["short answers"]})

    profile = memory.revise_profile_item(
        "preferences", "short answers", "correct", replacement="detailed answers"
    )

    assert profile["preferences"] == ["detailed answers"]
    assert profile["profile_lifecycle"]["preferences"]["short answers"]["status"] == "superseded"
    assert profile["profile_lifecycle"]["preferences"]["detailed answers"]["status"] == "confirmed"
    assert profile["profile_history"][-2]["action"] == "corrected"
    assert profile["profile_history"][-2]["replacement"] == "detailed answers"
    assert profile["profile_history"][-1]["action"] == "confirmed"


def test_superseded_item_is_not_reintroduced_by_later_hints(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.personalize("initial", {"preferences": ["short answers"]})
    memory.revise_profile_item(
        "preferences", "short answers", "correct", replacement="detailed answers"
    )

    profile = memory.personalize("later task", {"preferences": ["short answers"]})

    assert profile["preferences"] == ["detailed answers"]


def test_dismissed_item_is_not_reintroduced_by_later_hints(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.personalize("initial", {"goals": ["become a public speaker"]})
    memory.revise_profile_item("goals", "become a public speaker", "dismiss")

    profile = memory.personalize("later task", {"goals": ["become a public speaker"]})

    assert "become a public speaker" not in profile["goals"]
    assert profile["profile_lifecycle"]["goals"]["become a public speaker"]["status"] == "dismissed"


def test_explicit_confirmation_can_reactivate_a_dismissed_item(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.revise_profile_item("preferences", "short answers", "dismiss")
    memory.personalize("later task", {"preferences": ["short answers"]})
    assert "short answers" not in memory.load_profile()["preferences"]

    profile = memory.revise_profile_item("preferences", "short answers", "confirm")
    assert "short answers" in profile["preferences"]
    assert profile["profile_lifecycle"]["preferences"]["short answers"]["status"] == "confirmed"


def test_legacy_profile_without_lifecycle_fields_is_supported(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.profile_file.write_text(json.dumps({
        "version": 1,
        "status": "active",
        "preferences": ["concise"],
    }), encoding="utf-8")

    profile = memory.revise_profile_item("preferences", "concise", "dismiss")

    assert profile["preferences"] == []
    assert profile["profile_lifecycle"]["preferences"]["concise"]["status"] == "dismissed"
    assert isinstance(profile["profile_history"], list)


def test_audit_records_action_without_profile_text(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.personalize("initial", {"preferences": ["secret preference A"]})
    memory.revise_profile_item(
        "preferences", "secret preference A", "correct", replacement="secret preference B"
    )

    audit_text = memory.audit_file.read_text(encoding="utf-8")
    assert "profile_item_lifecycle" in audit_text
    assert '"field": "preferences"' in audit_text
    assert "secret preference A" not in audit_text
    assert "secret preference B" not in audit_text


@pytest.mark.parametrize(
    "field,value,action,replacement",
    [
        ("confidence", "0.8", "confirm", None),
        ("preferences", "", "confirm", None),
        ("preferences", "x", "unknown", None),
        ("preferences", "x", "correct", None),
        ("preferences", "x", "correct", "x"),
    ],
)
def test_invalid_lifecycle_operations_are_rejected(tmp_path, field, value, action, replacement):
    memory = JsonMemory(tmp_path)
    with pytest.raises(ValueError):
        memory.revise_profile_item(field, value, action, replacement=replacement)


def test_explicit_teach_can_reactivate_a_dismissed_item(tmp_path):
    from ambivikhry.agent import AmbivikhryAgent
    from ambivikhry.llm import MockLLM

    memory = JsonMemory(tmp_path)
    memory.revise_profile_item("preferences", "concise", "dismiss")
    agent = AmbivikhryAgent(provider=MockLLM(), workdir=str(tmp_path))

    profile = agent.teach(preferences=["concise"])

    assert "concise" in profile["preferences"]
    assert profile["profile_lifecycle"]["preferences"]["concise"]["status"] == "confirmed"


def test_missing_legacy_list_field_can_be_confirmed(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.profile_file.write_text(json.dumps({
        "version": 1, "status": "active", "preferences": [],
    }), encoding="utf-8")

    profile = memory.revise_profile_item("open_questions", "clarify goal", "confirm")

    assert profile["open_questions"] == ["clarify goal"]


def test_personalize_migrates_missing_legacy_profile_fields(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.profile_file.write_text(json.dumps({
        "version": 1, "status": "active", "preferences": [],
    }), encoding="utf-8")

    profile = memory.personalize("legacy profile", {"preferences": ["concise"]})

    assert profile["preferences"] == ["concise"]
    assert profile["goals"] == []
    assert profile["observations"][-1]["text"] == "legacy profile"


def test_explicit_user_input_flag_must_be_boolean(tmp_path):
    memory = JsonMemory(tmp_path)
    with pytest.raises(ValueError):
        memory.personalize("task", {"preferences": ["x"]}, explicit_user_input="yes")


def test_unhashable_action_fails_closed(tmp_path):
    memory = JsonMemory(tmp_path)
    with pytest.raises(ValueError):
        memory.revise_profile_item("preferences", "x", [], replacement=None)


def test_correction_requires_an_active_original_value(tmp_path):
    memory = JsonMemory(tmp_path)
    with pytest.raises(ValueError):
        memory.revise_profile_item(
            "preferences", "not active", "correct", replacement="replacement"
        )


def test_profile_history_is_bounded_without_losing_lifecycle_state(tmp_path):
    memory = JsonMemory(tmp_path)
    for index in range(510):
        memory.revise_profile_item("open_questions", f"question {index}", "dismiss")

    profile = memory.load_profile()
    assert len(profile["profile_history"]) == 500
    assert profile["profile_lifecycle"]["open_questions"]["question 0"]["status"] == "dismissed"
    assert profile["profile_lifecycle"]["open_questions"]["question 509"]["status"] == "dismissed"



def test_model_context_excludes_dismissed_and_superseded_values(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.personalize(
        "private observation mentions concise answers and coffee",
        {"preferences": ["concise answers", "coffee"], "working_style": ["iterative"]},
    )
    memory.revise_profile_item("preferences", "concise answers", "dismiss")
    memory.revise_profile_item("preferences", "coffee", "correct", replacement="tea")

    persisted = memory.load_profile()
    context = memory.profile_context(persisted)

    assert "concise answers" not in context
    assert "coffee" not in context
    assert "tea" in context
    assert "iterative" in context
    assert "profile_lifecycle" not in context
    assert "profile_history" not in context
    assert "observations" not in context
    assert "private observation" not in context


def test_model_context_projection_does_not_mutate_persisted_profile(tmp_path):
    memory = JsonMemory(tmp_path)
    memory.personalize("initial", {"preferences": ["brief"]})
    memory.revise_profile_item("preferences", "brief", "dismiss")
    before = memory.load_profile()

    memory.profile_context(before)
    after = memory.load_profile()

    assert before == after
    assert after["profile_lifecycle"]["preferences"]["brief"]["status"] == "dismissed"
    assert after["profile_history"]


def test_model_context_handles_malformed_lifecycle_metadata_fail_closed(tmp_path):
    memory = JsonMemory(tmp_path)
    profile = {
        "version": 1,
        "status": "active",
        "preferences": ["keep"],
        "profile_lifecycle": ["malformed"],
        "profile_history": [{"value": "do not expose"}],
        "observations": [{"text": "do not expose"}],
    }

    context = memory.profile_context(profile)

    # A malformed lifecycle root quarantines profile values instead of
    # treating an unknown state as active. Raw history/observations stay hidden.
    assert json.loads(context)["preferences"] == []
    assert "do not expose" not in context
    assert "profile_history" not in context
    assert "observations" not in context



def test_model_context_filters_stale_items_even_if_legacy_list_still_contains_them():
    profile = {
        "version": 1,
        "status": "active",
        "preferences": ["dismissed preference", "superseded preference", "current preference"],
        "profile_lifecycle": {
            "preferences": {
                "dismissed preference": {"status": "dismissed"},
                "superseded preference": {"status": "superseded"},
            }
        },
        "profile_history": [],
        "observations": [],
    }

    context = JsonMemory.profile_context(profile)

    assert "dismissed preference" not in context
    assert "superseded preference" not in context
    assert "current preference" in context
