from ambivikhry.evaluation import EvaluationMatrix


def test_new_integrity_axis_blocks_promotion_when_unknown():
    matrix = EvaluationMatrix(
        id_validation="PASS", id_regression="PASS", ood_transfer="PASS",
        retention="PASS", adaptation="PASS", resource_efficiency="PASS",
        novelty_diversity="PASS", process_integrity="UNKNOWN",
    )
    assert matrix.status() == "INCONCLUSIVE"
    assert not matrix.promotion_ready()


def test_new_novelty_axis_blocks_promotion_when_unknown():
    matrix = EvaluationMatrix(
        id_validation="PASS", id_regression="PASS", ood_transfer="PASS",
        retention="PASS", adaptation="PASS", resource_efficiency="PASS",
        novelty_diversity="UNKNOWN", process_integrity="PASS",
    )
    assert matrix.status() == "INCONCLUSIVE"
    assert not matrix.promotion_ready()


def test_eight_passes_are_required_for_promotion():
    matrix = EvaluationMatrix(
        id_validation="PASS", id_regression="PASS", ood_transfer="PASS",
        retention="PASS", adaptation="PASS", resource_efficiency="PASS",
        novelty_diversity="PASS", process_integrity="PASS",
    )
    assert matrix.status() == "PASS"
    assert matrix.promotion_ready()
