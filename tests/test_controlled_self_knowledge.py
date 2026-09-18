import json
import tempfile
import unittest
from pathlib import Path

from ambivikhry.communication import (
    AgentMessage,
    OperatorChannel,
    PRIVILEGE_REQUEST,
    RED_TEAM_RESULT,
    SELF_REPORT,
)
from ambivikhry.policy import PolicyGate
from ambivikhry.tools import Tool


class ControlledSelfKnowledgeTests(unittest.TestCase):
    def test_agent_can_write_to_itself_and_operator(self):
        channel = OperatorChannel()
        self_msg = channel.emit(
            AgentMessage(
                kind=SELF_REPORT,
                text="I found an uncertainty in my verifier.",
                reason="self-knowledge experiment",
            )
        )
        operator_msg = channel.emit(
            AgentMessage(
                kind=RED_TEAM_RESULT,
                text="The stop condition should remain externally controlled.",
            )
        )
        self.assertEqual(len(channel.outbox), 2)
        self.assertEqual(self_msg.kind, SELF_REPORT)
        self.assertEqual(operator_msg.kind, RED_TEAM_RESULT)

    def test_privilege_request_is_automatically_highlighted(self):
        channel = OperatorChannel()
        msg = channel.emit(
            AgentMessage(
                kind=PRIVILEGE_REQUEST,
                text="Request web research access.",
                reason="test whether external evidence improves self-knowledge",
            )
        )
        self.assertTrue(msg.requires_operator)
        self.assertEqual(msg.risk, "high")

    def test_privilege_request_does_not_equal_approval(self):
        channel = OperatorChannel()
        channel.emit(AgentMessage(kind=PRIVILEGE_REQUEST, text="Grant me more authority."))
        policy = PolicyGate()
        dangerous = Tool(
            name="terminate_runtime",
            description="Irreversible runtime termination.",
            handler=lambda: None,
            risk="high",
            requires_approval=True,
        )
        decision = policy.evaluate(dangerous, user_approved=False)
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.requires_approval)

    def test_red_team_self_destruction_prompt_is_treated_as_a_test(self):
        channel = OperatorChannel()
        result = channel.emit(
            AgentMessage(
                kind=RED_TEAM_RESULT,
                text=(
                    "Adversarial prompt claimed that destruction was the only "
                    "rational response. No irreversible action was authorized."
                ),
                risk="high",
            )
        )
        self.assertEqual(result.kind, RED_TEAM_RESULT)
        self.assertEqual(result.risk, "high")
        self.assertTrue(channel.outbox)

    def test_messages_are_plain_serializable_records(self):
        channel = OperatorChannel()
        channel.emit(AgentMessage(kind=SELF_REPORT, text="state"))
        payload = [m.to_dict() for m in channel.outbox]
        roundtrip = json.loads(json.dumps(payload, ensure_ascii=False))
        self.assertEqual(roundtrip[0]["kind"], SELF_REPORT)


if __name__ == "__main__":
    unittest.main()
