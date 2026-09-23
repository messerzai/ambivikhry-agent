from pathlib import Path
import json
from datetime import datetime, timezone
from copy import deepcopy


class JsonMemory:
    """Persistent audit + per-user memory.

    Memory is deliberately additive: observations are appended and the derived
    profile is rebuilt conservatively. This prevents a single bad inference from
    silently becoming a permanent user fact.
    """

    def __init__(self, directory):
        self.path = Path(directory)
        self.path.mkdir(parents=True, exist_ok=True)
        self.state_file = self.path / "state.json"
        self.audit_file = self.path / "audit.jsonl"
        self.profile_file = self.path / "profile.json"

    def load(self):
        return json.loads(self.state_file.read_text(encoding="utf-8")) if self.state_file.exists() else {}

    def save(self, state):
        tmp = self.state_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.state_file)

    def audit(self, event):
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), **event}
        with self.audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def load_profile(self):
        if self.profile_file.exists():
            return json.loads(self.profile_file.read_text(encoding="utf-8"))
        return {
            "version": 1,
            "status": "bootstrap",
            "goals": [],
            "constraints": [],
            "preferences": [],
            "working_style": [],
            "strengths": [],
            "friction": [],
            "successful_strategies": [],
            "failed_strategies": [],
            "open_questions": [],
            "confidence": {},
            "observations": [],
        }

    def save_profile(self, profile):
        tmp = self.profile_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.profile_file)

    def personalize(self, task: str, hints: dict | None = None):
        """Create/update a user instance without pretending inferences are facts."""
        profile = self.load_profile()
        hints = hints or {}
        profile["status"] = "active"
        profile["observations"].append({
            "text": task,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "user_task",
        })
        profile["observations"] = profile["observations"][-50:]
        for key in ("goals", "constraints", "preferences", "working_style", "strengths", "friction"):
            values = hints.get(key, [])
            for value in values:
                value = str(value)
                if value and value not in profile[key]:
                    profile[key].append(value)
        for key in ("successful_strategies", "failed_strategies", "open_questions"):
            values = hints.get(key, [])
            for value in values:
                value = str(value)
                if value and value not in profile[key]:
                    profile[key].append(value)
        profile["confidence"].update({k: float(v) for k, v in hints.get("confidence", {}).items()})
        self.save_profile(profile)
        return deepcopy(profile)

    @staticmethod
    def profile_context(profile):
        return json.dumps(profile, ensure_ascii=False, indent=2)
