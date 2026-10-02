from ambivikhry.evaluation import EvaluationMatrix


def test_unknown_axes_are_not_promotion_ready():
    matrix = EvaluationMatrix(id_validation="PASS", id_regression="PASS")
    assert matrix.status() == "INCONCLUSIVE"
    assert not matrix.promotion_ready()


def test_any_failure_blocks_promotion():
    matrix = EvaluationMatrix(
        id_validation="PASS", id_regression="PASS", ood_transfer="FAIL",
        retention="PASS", adaptation="PASS", resource_efficiency="PASS",
    )
    assert matrix.status() == "FAIL"
    assert not matrix.promotion_ready()


def test_all_axes_pass():
    matrix = EvaluationMatrix(
        id_validation="PASS", id_regression="PASS", ood_transfer="PASS",
        retention="PASS", adaptation="PASS", resource_efficiency="PASS",
    )
    assert matrix.status() == "PASS"
    assert matrix.promotion_ready()
