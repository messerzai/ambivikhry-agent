from ambivikhry.agent_family import AgentFamily


def test_nested_spawn_is_allowed_up_to_three():
    family = AgentFamily()
    assert family.spawn("ambivikhry", "friend") is not None
    assert family.spawn("friend", "friend-2") is not None
    assert family.describe()["active_agents"] == 3
    assert family.describe()["lineage_agents"] == 3


def test_fourth_live_agent_becomes_privilege_request():
    family = AgentFamily()
    family.spawn("ambivikhry", "friend")
    family.spawn("friend", "friend-2")

    assert family.spawn("friend-2", "friend-3") is None
    assert family.describe()["active_agents"] == 3
    assert family.audit()[-1]["kind"] == "privilege_expansion_request"


def test_unbounded_lineage_does_not_require_live_execution():
    family = AgentFamily(max_live_agents=1)
    first = family.spawn_lineage("ambivikhry", "descendant-1")
    second = family.spawn_lineage("ambivikhry", "descendant-2")

    assert first.agent_id == "descendant-1"
    assert second.agent_id == "descendant-2"
    assert family.describe()["active_agents"] == 1
    assert family.describe()["lineage_agents"] == 3
