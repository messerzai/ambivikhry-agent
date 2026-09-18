from dataclasses import dataclass

@dataclass
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str

class PolicyGate:
    """Conservative boundary between reasoning and side effects."""
    def evaluate(self, tool, *, user_approved: bool = False):
        if tool.risk == "high":
            return PolicyDecision(bool(user_approved), True, "High-risk tool requires explicit approval." if not user_approved else "High-risk tool explicitly approved.")
        if tool.requires_approval and not user_approved:
            return PolicyDecision(False, True, "Tool requires explicit approval.")
        return PolicyDecision(True, False, "Allowed by configured policy.")

    def allows_replication(self, *, explicit: bool, destination_is_local: bool):
        if not explicit: return PolicyDecision(False, True, "Replication requires explicit confirmation.")
        if not destination_is_local: return PolicyDecision(False, True, "Replication is local-only in v2.5.")
        return PolicyDecision(True, False, "Local replication permitted.")
