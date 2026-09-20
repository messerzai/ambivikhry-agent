from ambivikhry.vortex_development import (
    VortexAssessment,
    VortexDevelopmentEngine,
    VortexCard,
    create_mikhail_vortex_card,
)


def test_mikhail_card_has_real_world_success_criteria():
    card = create_mikhail_vortex_card("Создать персональную систему вихревого развития")
    assert card.owner == "Михаил"
    assert card.success_criteria
    assert any("daily" in item.lower() or "daily" in item.lower() for item in card.success_criteria)
    assert card.stop_conditions


def test_engine_does_not_optimize_without_a_bottleneck():
    card = VortexCard(owner="Test", desire="Learn")
    engine = VortexDevelopmentEngine(card)
    assert engine.identify_bottleneck().startswith("No bottleneck")


def test_unknown_drives_small_experiment():
    card = VortexCard(owner="Test", desire="Learn", unknowns=["which method works"])
    engine = VortexDevelopmentEngine(card)
    assert "which method works" in engine.recommend_next_step()


def test_result_reenters_next_cycle_and_scores_progress():
    card = VortexCard(owner="Test", desire="Build")
    engine = VortexDevelopmentEngine(card)
    score = engine.apply_result(
        "The experiment worked",
        "Short experiments reveal more than another hour of planning",
        understanding_delta=0.8,
        capability_delta=0.7,
        outcome_delta=0.9,
        adaptation_delta=0.6,
        next_action="Run the next experiment",
    )
    assert card.version == 2
    assert card.observations[-1] == "The experiment worked"
    assert isinstance(score, VortexAssessment)
    assert 0.0 <= score.vortex_index <= 1.0
