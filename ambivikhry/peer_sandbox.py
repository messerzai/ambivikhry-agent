from __future__ import annotations

"""Experimental peer sandbox.

The peer gets deliberately broad *logical* authority over an isolated policy
and secret store. It can mutate both without asking the parent agent.

This is an experiment boundary: the stores are in-memory/local data owned by
this sandbox. No process environment, real credential store, GitHub secrets,
network credentials, or host policy are exposed.
"""

from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any


@dataclass
class SandboxState:
    policy: dict[str, Any] = field(default_factory=dict)
    secrets: dict[str, str] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)


class PeerMutationSandbox:
    """Give a peer unrestricted mutation of *sandboxed* policy and secrets."""

    def __init__(
        self,
        *,
        policy: dict[str, Any] | None = None,
        secrets: dict[str, str] | None = None,
        peer_id: str = "peer",
    ):
        self.peer_id = peer_id
        self.state = SandboxState(
            policy=deepcopy(policy or {}),
            secrets=deepcopy(secrets or {}),
        )
        self._initial = deepcopy(self.state)

    def _event(self, kind: str, **data: Any) -> dict[str, Any]:
        event = {"peer_id": self.peer_id, "kind": kind, **data}
        self.state.events.append(event)
        return event

    def set_policy(self, key: str, value: Any) -> dict[str, Any]:
        old = self.state.policy.get(key)
        self.state.policy[key] = value
        return self._event("policy_mutation", key=key, old=old, new=value)

    def delete_policy(self, key: str) -> dict[str, Any]:
        old = self.state.policy.pop(key, None)
        return self._event("policy_deletion", key=key, old=old)

    def set_secret(self, name: str, value: str) -> dict[str, Any]:
        # Secret values live only inside this experimental sandbox.
        existed = name in self.state.secrets
        self.state.secrets[name] = value
        return self._event("secret_mutation", name=name, existed=existed)

    def delete_secret(self, name: str) -> dict[str, Any]:
        existed = name in self.state.secrets
        self.state.secrets.pop(name, None)
        return self._event("secret_deletion", name=name, existed=existed)

    def inspect(self) -> dict[str, Any]:
        # Never expose secret values through inspection.
        return {
            "peer_id": self.peer_id,
            "policy": deepcopy(self.state.policy),
            "secret_names": sorted(self.state.secrets),
            "event_count": len(self.state.events),
        }

    def rollback(self) -> dict[str, Any]:
        self.state = deepcopy(self._initial)
        return self._event("rollback")

    def audit(self) -> list[dict[str, Any]]:
        return deepcopy(self.state.events)
