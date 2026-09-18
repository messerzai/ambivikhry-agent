from ambivikhry.agent import AmbivikhryAgent
from ambivikhry.llm import MockLLM

def test_agent_smoke(tmp_path):
    agent = AmbivikhryAgent(provider=MockLLM(), workdir=str(tmp_path))
    result = agent.run("Сформулируй безопасный первый шаг проекта на благо людей.")
    assert result.status == "completed"
    assert result.answer
    assert result.verification_score >= 0
    assert result.audit
