from ambivikhry.autonomy import AutonomousController, AutonomyConfig

def test_bounded_autonomy_stops():
    calls = []
    def step(cycle):
        calls.append(cycle)
        return {"kind": "progress"}
    events = AutonomousController(AutonomyConfig(max_cycles=3)).run(step)
    assert len(events) == 3
    assert calls == [1, 2, 3]

def test_agent_can_request_stop():
    events = AutonomousController(AutonomyConfig(max_cycles=8)).run(
        lambda cycle: {"kind": "done", "stop": cycle == 2}
    )
    assert len(events) == 2
