import json

from ambivikhry.memory import JsonMemory


def test_context_fails_closed_on_malformed_item_lifecycle_status():
    profile = {
        "version": 1,
        "status": "active",
        "preferences": [
            "bad-list-status",
            "bad-object-status",
            "unknown-status",
            "confirmed-item",
            "legacy-item-without-lifecycle",
        ],
        "profile_lifecycle": {
            "preferences": {
                "bad-list-status": {"status": []},
                "bad-object-status": {"status": {"unexpected": "object"}},
                "unknown-status": {"status": "future-unrecognized-state"},
                "confirmed-item": {"status": "confirmed"},
            }
        },
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert set(context["preferences"]) == {
        "confirmed-item",
        "legacy-item-without-lifecycle",
    }


def test_context_excludes_field_with_malformed_lifecycle_map():
    profile = {
        "version": 1,
        "status": "active",
        "preferences": ["do-not-trust-this-field"],
        "profile_lifecycle": {"preferences": []},
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert context["preferences"] == []


def test_personalize_does_not_reintroduce_item_with_malformed_lifecycle_status(tmp_path):
    memory = JsonMemory(tmp_path)
    profile = memory.load_profile()
    profile["profile_lifecycle"] = {
        "preferences": {"dismissed-but-corrupt": {"status": []}}
    }
    memory.save_profile(profile)

    updated = memory.personalize(
        "later task",
        {"preferences": ["dismissed-but-corrupt", "new-inferred-preference"]},
    )

    assert "dismissed-but-corrupt" not in updated["preferences"]
    assert "new-inferred-preference" in updated["preferences"]
    context = json.loads(memory.profile_context(updated))
    assert "dismissed-but-corrupt" not in context["preferences"]


def test_personalize_skips_inferred_hints_when_field_lifecycle_map_is_malformed(tmp_path):
    memory = JsonMemory(tmp_path)
    profile = memory.load_profile()
    profile["profile_lifecycle"] = {"preferences": []}
    memory.save_profile(profile)

    updated = memory.personalize(
        "later task", {"preferences": ["untrusted-inferred-preference"]}
    )

    assert "untrusted-inferred-preference" not in updated["preferences"]


def test_explicit_user_input_can_repair_malformed_field_lifecycle_map(tmp_path):
    memory = JsonMemory(tmp_path)
    profile = memory.load_profile()
    profile["profile_lifecycle"] = {"preferences": []}
    memory.save_profile(profile)

    updated = memory.personalize(
        "explicit teaching",
        {"preferences": ["user-confirmed-preference"]},
        explicit_user_input=True,
    )

    assert "user-confirmed-preference" in updated["preferences"]
    assert (
        updated["profile_lifecycle"]["preferences"]["user-confirmed-preference"]["status"]
        == "confirmed"
    )



def test_context_excludes_values_when_root_lifecycle_object_is_malformed():
    profile = {
        "version": 1,
        "status": "active",
        "preferences": ["possibly-stale-preference"],
        "profile_lifecycle": [],
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert context["preferences"] == []


def test_personalize_quarantines_existing_values_after_malformed_root(tmp_path):
    memory = JsonMemory(tmp_path)
    profile = memory.load_profile()
    profile["preferences"] = ["old-preference"]
    profile["profile_lifecycle"] = []
    memory.save_profile(profile)

    updated = memory.personalize(
        "later task", {"preferences": ["old-preference", "new-preference"]}
    )

    assert updated["profile_lifecycle"]["preferences"]["old-preference"]["status"] == "unknown"
    assert "old-preference" in updated["preferences"]  # retained, not erased
    assert "new-preference" in updated["preferences"]
    context = json.loads(memory.profile_context(updated))
    assert "old-preference" not in context["preferences"]
    assert "new-preference" in context["preferences"]


def test_explicit_user_teaching_can_reconfirm_quarantined_value(tmp_path):
    memory = JsonMemory(tmp_path)
    profile = memory.load_profile()
    profile["preferences"] = ["old-preference"]
    profile["profile_lifecycle"] = []
    memory.save_profile(profile)

    updated = memory.personalize(
        "explicit teaching",
        {"preferences": ["old-preference"]},
        explicit_user_input=True,
    )

    assert updated["profile_lifecycle"]["preferences"]["old-preference"]["status"] == "confirmed"
    context = json.loads(memory.profile_context(updated))
    assert "old-preference" in context["preferences"]
