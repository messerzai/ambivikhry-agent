from .agent import AmbivikhryAgent
from .llm import MockLLM

def main():
    agent=AmbivikhryAgent(provider=MockLLM(),workdir="./ambivikhry_state")
    result=agent.run("Предложи безопасный первый шаг проекта, который должен приносить пользу людям.")
    print(result.answer)
    print(f"instance={result.instance_id} confidence={result.confidence:.2f} iterations={result.iterations}")

if __name__ == "__main__": main()
