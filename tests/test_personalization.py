from ambivikhry.agent import AmbivikhryAgent
from ambivikhry.llm import MockLLM


def test_personal_profile_is_isolated_and_persistent(tmp_path):
    first = AmbivikhryAgent(provider=MockLLM(), workdir=str(tmp_path / "a"))
    second = AmbivikhryAgent(provider=MockLLM(), workdir=str(tmp_path / "b"))

    first.teach(
        goals=["build a useful product"],
        preferences=["concise answers"],
        working_style=["experiments first"],
    )
    first.run("Find the smallest useful next experiment.")

    profile_a = first.memory.load_profile()
    profile_b = second.memory.load_profile()

    assert "build a useful product" in profile_a["goals"]
    assert "concise answers" in profile_a["preferences"]
    assert profile_b["goals"] == []
    assert profile_b["preferences"] == []
    assert len(profile_a["observations"]) >= 2


def test_personalization_is_reported_in_result(tmp_path):
    agent = AmbivikhryAgent(provider=MockLLM(), workdir=str(tmp_path))
    result = agent.run("Choose a safe first step for my project.")
    assert result.status == "completed"
    assert 0.0 <= result.personalization_score <= 1.0
    assert (tmp_path / "profile.json").exists()
