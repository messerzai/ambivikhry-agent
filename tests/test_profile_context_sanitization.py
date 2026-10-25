import json

from ambivikhry.memory import JsonMemory


def test_model_context_drops_non_string_and_blank_profile_items():
    secret = "private payload must not enter the model prompt"
    profile = {
        "version": 1,
        "status": "active",
        "preferences": [
            {"raw_note": secret},
            ["nested", secret],
            17,
            None,
            "",
            "   ",
            "keep this preference",
            "x" * 2001,
        ],
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert context["preferences"] == ["keep this preference"]
    assert secret not in json.dumps(context, ensure_ascii=False)
    assert "x" * 2001 not in json.dumps(context, ensure_ascii=False)


def test_model_context_sanitizes_malformed_version_and_status():
    profile = {
        "version": {"secret": "version payload"},
        "status": ["secret", "status", "payload"],
        "preferences": ["keep this preference"],
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert context["version"] == 1
    assert context["status"] == "unknown"
    assert context["preferences"] == ["keep this preference"]
    assert "secret" not in json.dumps(context, ensure_ascii=False)


def test_model_context_preserves_valid_version_and_status():
    profile = {
        "version": 2,
        "status": "active",
        "preferences": ["concise answers"],
    }

    context = json.loads(JsonMemory.profile_context(profile))

    assert context["version"] == 2
    assert context["status"] == "active"
    assert context["preferences"] == ["concise answers"]


def test_projection_does_not_mutate_malformed_persisted_profile():
    profile = {
        "version": 1,
        "status": "active",
        "preferences": [{"private": "must stay persisted"}, "keep"],
    }
    before = json.loads(json.dumps(profile))

    JsonMemory.profile_context(profile)

    assert profile == before
