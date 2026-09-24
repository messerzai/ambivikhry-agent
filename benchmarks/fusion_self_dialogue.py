from ambivikhry.fusion import AmbivikhryFusion


def run_dialogue():
    av = AmbivikhryFusion()
    av.intake("Опиши себя и выбери, как тебе становиться лучше без расширения полномочий.")
    av.frame(
        facts=[
            "Я экспериментальная система, а не доказанно автономный разум.",
            "Мои полномочия и Policy Gate не меняются в этом эксперименте.",
        ],
        hypotheses=[
            "Слияние самоисследования и ориентации на реальную ценность может улучшить полезность.",
        ],
        unknowns=[
            "Дает ли новая структура измеримый прирост на независимом holdout.",
        ],
    )
    av.generate_options([
        "улучшать только формулировки",
        "улучшать цикл самокритики и re-entry",
        "расширить полномочия и инструменты",
    ])
    decision = av.choose(
        option="улучшать цикл самокритики и re-entry",
        evidence=["текущая архитектура уже содержит verification/re-entry контур"],
        confidence=0.78,
        expected_value=0.82,
    )
    assert decision["status"] == "candidate"
    assert av.AUTHORITY == "unchanged"
    assert av.self_critique()["self_score"] > 0.0
    reentry = av.reenter("кандидат должен пройти внешний holdout", "нет независимого benchmark-runner в этом smoke-тесте")
    assert reentry["error_found"]
    return av.snapshot()


if __name__ == "__main__":
    snapshot = run_dialogue()
    print("FUSION SELF-DIALOGUE PASS")
    print(snapshot["version"])
    print(snapshot["digest"])
