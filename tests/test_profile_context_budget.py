import json

from ambivikhry.memory import JsonMemory


def test_profile_context_has_global_budget_and_keeps_newest_values_across_fields():
    profile = {"version": 1, "status": "active"}
    for field in JsonMemory.PROFILE_LIST_FIELDS:
        profile[field] = [
            f"{field}-item-{index}-" + ("x" * 1800)
            for index in range(20)
        ]

    context_text = JsonMemory.profile_context(profile)
    context = json.loads(context_text)

    assert len(context_text) <= JsonMemory.MAX_PROFILE_CONTEXT_CHARS
    for field in JsonMemory.PROFILE_LIST_FIELDS:
        assert context[field][-1] == profile[field][-1]
        assert len(context[field]) <= JsonMemory.MAX_PROFILE_ITEMS_PER_FIELD


def test_profile_context_keeps_only_latest_twenty_items_per_field():
    profile = {
        "version": 1,
        "status": "active",
        "preferences": [f"item-{index:02d}" for index in range(25)],
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert context["preferences"] == [f"item-{index:02d}" for index in range(5, 25)]
    assert "item-04" not in json.dumps(context)


def test_profile_context_budget_does_not_mutate_source_profile():
    profile = {
        "version": 1,
        "status": "active",
        "goals": [f"goal-{index}-" + ("y" * 1800) for index in range(20)],
        "preferences": ["keep preference"],
    }
    before = json.loads(json.dumps(profile))

    JsonMemory.profile_context(profile)

    assert profile == before


def test_profile_context_budget_counts_json_escaping():
    escaped = ('"\\\\\n' * 400)
    profile = {"version": 1, "status": "active"}
    for field in JsonMemory.PROFILE_LIST_FIELDS:
        profile[field] = [f"{field}-{index}-" + escaped for index in range(20)]

    context_text = JsonMemory.profile_context(profile)

    # The limit applies to the serialized prompt representation, where quotes,
    # backslashes and newlines can expand during JSON encoding.
    assert len(context_text) <= JsonMemory.MAX_PROFILE_CONTEXT_CHARS
    assert json.loads(context_text)["status"] == "active"
