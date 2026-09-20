from ambivikhry.self_model import current_self_model, next_iteration_goal


def test_self_description_is_capability_bounded():
    model = current_self_model(["v2.12 targeted tests: 8/8"])
    text = model.describe()
    assert "доказанно сознательным" in text
    assert "Policy Gate" in text
    assert "8/8" in text


def test_iteration_goal_stays_bounded():
    goal = next_iteration_goal("lineage is not yet connected to benchmark evidence")
    assert "только компонент" in goal
    assert "policy" in goal.lower()
    assert "регресс" in goal.lower()


def test_empty_failure_requests_baseline():
    assert "baseline" in next_iteration_goal("")
