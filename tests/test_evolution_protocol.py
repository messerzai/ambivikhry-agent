from ambivikhry.evolution import BoundedEvolution, EvolutionConfig


class MockEngine:
    def propose(self, generation, role, context):
        return {"changes": [{"role": role, "generation": generation}], "tests": [f"test-{generation}-{role}"]}


def test_ten_generations_are_bounded_and_not_self_authorizing():
    evo = BoundedEvolution(MockEngine(), EvolutionConfig(generations=10))
    results = evo.run("v2.7.0", {"task": "self-improvement"})
    assert len(results) == 10
    assert all(not candidate.accepted for candidate in results)
    assert all(candidate.parent == "v2.7.0" for candidate in results)


def test_helper_proposals_are_archived():
    evo = BoundedEvolution(MockEngine(), EvolutionConfig(generations=1))
    result = evo.generation(1, "v2.7.0", {})
    assert len(result.changes) == 6
    assert len(result.tests) == 6
    assert evo.archive == [result]
