from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json, uuid
from datetime import datetime, timezone

@dataclass
class ReplicationPolicy:
    explicit_confirmation_required: bool = True
    local_only: bool = True
    auto_start_child: bool = False
    allow_network_propagation: bool = False
    allow_privilege_escalation: bool = False

class Replicator:
    """Controlled local child creation; no auto-start or network propagation."""
    def __init__(self, root, policy=None): self.root=Path(root); self.policy=policy or ReplicationPolicy()
    def replicate(self, *, parent_manifest, destination, explicit_confirmation=False, mutation=None):
        if self.policy.explicit_confirmation_required and not explicit_confirmation: raise PermissionError("Replication requires explicit confirmation.")
        dest=Path(destination).resolve()
        if self.policy.local_only and dest == self.root.resolve(): raise ValueError("Child destination must differ from parent.")
        dest.mkdir(parents=True, exist_ok=False)
        manifest=dict(parent_manifest); manifest.update({
            "instance_id":"av-"+uuid.uuid4().hex[:12],
            "parent_instance_id":parent_manifest.get("instance_id"),
            "replication_generation":int(parent_manifest.get("replication_generation",0))+1,
            "created_at":datetime.now(timezone.utc).isoformat(),
            "mutation":mutation or {"type":"none"}, "autostart":False})
        (dest/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
        (dest/"REPLICATION_NOTICE.txt").write_text("Child created locally; not auto-started.\n",encoding="utf-8")
        return manifest
