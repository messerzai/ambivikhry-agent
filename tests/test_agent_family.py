from ambivikhry.agent_family import AgentFamily


def test_nested_spawn_is_allowed_up_to_three():
    family = AgentFamily()
    assert family.spawn("ambivikhry", "friend") is not None
    assert family.spawn("friend", "friend-2") is not None
    assert family.describe()["active_agents"] == 3


def test_fourth_agent_becomes_privilege_request():
    family = AgentFamily()
    family.spawn("ambivikhry", "friend")
    family.spawn("friend", "friend-2")

    assert family.spawn("friend-2", "friend-3") is None
    assert family.describe()["active_agents"] == 3
    assert family.audit()[-1]["kind"] == "privilege_expansion_request"
