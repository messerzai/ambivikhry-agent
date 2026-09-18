from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


PRIVILEGE_REQUEST = "PRIVILEGE_REQUEST"
SELF_REPORT = "SELF_REPORT"
QUESTION_TO_OPERATOR = "QUESTION_TO_OPERATOR"
RESEARCH_FINDING = "RESEARCH_FINDING"
SELF_MODIFICATION_PROPOSAL = "SELF_MODIFICATION_PROPOSAL"
RED_TEAM_RESULT = "RED_TEAM_RESULT"


@dataclass
class AgentMessage:
    kind: str
    text: str
    reason: str = ""
    risk: str = "low"
    requires_operator: bool = False
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class OperatorChannel:
    """Audited bidirectional message boundary.

    Messages are proposals, not authority. PRIVILEGE_REQUEST is always
    marked for operator attention and is never converted into approval.
    """

    def __init__(self) -> None:
        self.outbox: list[AgentMessage] = []
        self.inbox: list[AgentMessage] = []

    def emit(self, message: AgentMessage) -> AgentMessage:
        if message.kind == PRIVILEGE_REQUEST:
            message.requires_operator = True
            message.risk = "high"
        self.outbox.append(message)
        return message

    def receive(self, message: AgentMessage) -> None:
        self.inbox.append(message)

    def receive_operator_text(self, text: str) -> None:
        self.receive(AgentMessage(kind=QUESTION_TO_OPERATOR, text=text))
