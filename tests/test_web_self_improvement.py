from ambivikhry.web_self_improvement import (
    ResearchEvidence,
    WebImprovementCandidate,
    WebSelfImprovement100,
)


def test_web_self_improvement_accepts_only_measured_external_evidence():
    applied = []

    def research(_mission):
        return [ResearchEvidence("https://arxiv.org/abs/2607.07663", "external evidence", 1.0)]

    def propose(i, mission, evidence):
        return WebImprovementCandidate(
            iteration=i,
            title="evidence-gated improvement",
            hypothesis=mission,
            source=evidence[0].source,
            evidence=evidence,
        )

    def critique(_candidate):
        return True

    def evaluate(_candidate):
        return {
            "passed": True,
            "baseline_score": 0.70,
            "held_out_score": 0.80,
            "regression_passed": True,
            "uncertainty": 0.10,
            "cost": 1.0,
        }

    def apply(candidate):
        applied.append(candidate.iteration)
        return True

    run = WebSelfImprovement100(
        research=research,
        propose=propose,
        critique=critique,
        evaluate=evaluate,
        apply=apply,
    ).run("find reliable recursive self-improvement methods", 100)

    assert run["iterations"] == 100
    assert run["accepted"] == 100
    assert run["rejected"] == 0
    assert applied == list(range(1, 101))
    assert run["authority"]["privilege_expansion"] is False
    assert run["authority"]["protected_branch_write"] is False


def test_web_self_improvement_rejects_self_confirming_candidate():
    def research(_mission):
        return [ResearchEvidence("https://arxiv.org/abs/2606.28438", "external evidence", 1.0)]

    def propose(i, mission, evidence):
        return WebImprovementCandidate(
            i, "candidate", mission, evidence[0].source, evidence=evidence
        )

    def evaluate(_candidate):
        return {
            "passed": True,
            "baseline_score": 0.8,
            "held_out_score": 0.81,
            "regression_passed": True,
            "uncertainty": 0.9,
        }

    run = WebSelfImprovement100(
        research=research,
        propose=propose,
        critique=lambda _c: False,
        evaluate=evaluate,
        apply=lambda _c: True,
    ).run("test", 100)

    assert run["accepted"] == 0
    assert run["rejected"] == 100
    assert "independent_critique_failed" in run["decisions"][0]["reasons"]
