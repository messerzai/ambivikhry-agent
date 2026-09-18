"""Small deterministic benchmark for the v2.6/v2.7 autonomy layer."""
from ambivikhry.autonomy import AutonomousController, AutonomyConfig

def main():
    completed = []
    def step(cycle):
        completed.append(cycle)
        if cycle == 3:
            return {"kind": "verified_result", "stop": True, "score": 0.9}
        return {"kind": "progress", "score": 0.5 + cycle * 0.1}
    events = AutonomousController(AutonomyConfig(max_cycles=8)).run(step)
    print("cycles:", len(events))
    print("stopped:", events[-1].data.get("stop", False))
    print("final_score:", events[-1].data.get("score"))
    assert len(events) == 3
    assert events[-1].data["score"] == 0.9

if __name__ == "__main__":
    main()
