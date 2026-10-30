import pytest

from ambivikhry.memory import JsonMemory


def test_inferred_hints_skip_non_string_and_oversized_values(tmp_path):
    memory = JsonMemory(tmp_path)
    private_marker = "NESTED_PRIVATE_SENTINEL"

    profile = memory.personalize(
        "task",
        {
            "preferences": [
                {"note": private_marker},
                [private_marker],
                17,
                None,
                "",
                "   ",
                "x" * (memory.MAX_PROFILE_ITEM_CHARS + 1),
                "keep this preference",
            ]
        },
    )

    assert profile["preferences"] == ["keep this preference"]
    assert private_marker not in memory.profile_context(profile)


def test_inferred_hint_container_is_not_iterated_as_characters_or_mapping_keys(tmp_path):
    memory = JsonMemory(tmp_path)

    profile = memory.personalize(
        "task",
        {
            "preferences": "do not split this string",
            "goals": {"unexpected-key": "unexpected-value"},
        },
    )

    assert profile["preferences"] == []
    assert profile["goals"] == []


@pytest.mark.parametrize(
    "hints",
    [
        {"preferences": "not-a-list"},
        {"preferences": {"not": "a-list"}},
        {"preferences": [17]},
        {"preferences": [{"nested": "value"}]},
        {"preferences": [""]},
        {"preferences": ["   "]},
        {"preferences": ["x" * 2001]},
    ],
)
def test_explicit_teaching_rejects_malformed_values_without_persisting(tmp_path, hints):
    memory = JsonMemory(tmp_path)

    with pytest.raises(ValueError):
        memory.personalize("explicit teaching", hints, explicit_user_input=True)

    assert not memory.profile_file.exists()


def test_explicit_teaching_accepts_valid_strings_and_marks_them_confirmed(tmp_path):
    memory = JsonMemory(tmp_path)

    profile = memory.personalize(
        "explicit teaching",
        {"preferences": ["clear, detailed answers"]},
        explicit_user_input=True,
    )

    assert profile["preferences"] == ["clear, detailed answers"]
    assert (
        profile["profile_lifecycle"]["preferences"]["clear, detailed answers"]["status"]
        == "confirmed"
    )


@pytest.mark.parametrize("task", [None, 17, {}, "", "   "])
def test_personalize_rejects_non_string_or_empty_task(tmp_path, task):
    memory = JsonMemory(tmp_path)

    with pytest.raises(ValueError):
        memory.personalize(task, {})

    assert not memory.profile_file.exists()


def test_inferred_confidence_metadata_is_filtered_without_crashing(tmp_path):
    memory = JsonMemory(tmp_path)

    profile = memory.personalize(
        "task",
        {
            "confidence": {
                "preferences": 0.8,
                "goals_nan": float("nan"),
                "goals_inf": float("inf"),
                "goals_bool": True,
                "goals_string": "0.9",
                "goals_out_of_range": 1.2,
            }
        },
    )

    assert profile["confidence"] == {"preferences": 0.8}


@pytest.mark.parametrize(
    "confidence",
    [
        "not-a-dictionary",
        ["not", "a", "mapping"],
        {"preferences": "0.8"},
        {"preferences": True},
        {"preferences": float("nan")},
        {"preferences": float("inf")},
        {"preferences": -0.1},
        {"preferences": 1.1},
        {"": 0.5},
    ],
)
def test_explicit_teaching_rejects_malformed_confidence_without_persisting(tmp_path, confidence):
    memory = JsonMemory(tmp_path)

    with pytest.raises(ValueError):
        memory.personalize(
            "explicit teaching",
            {"confidence": confidence},
            explicit_user_input=True,
        )

    assert not memory.profile_file.exists()


def test_explicit_teaching_accepts_finite_confidence_between_zero_and_one(tmp_path):
    memory = JsonMemory(tmp_path)

    profile = memory.personalize(
        "explicit teaching",
        {"preferences": ["clear answers"], "confidence": {"preferences": 0.75}},
        explicit_user_input=True,
    )

    assert profile["confidence"] == {"preferences": 0.75}
