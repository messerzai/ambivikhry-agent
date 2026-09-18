from pathlib import Path
import json
from datetime import datetime, timezone

class JsonMemory:
    def __init__(self, directory):
        self.path = Path(directory); self.path.mkdir(parents=True, exist_ok=True)
        self.state_file = self.path / "state.json"; self.audit_file = self.path / "audit.jsonl"
    def load(self):
        return json.loads(self.state_file.read_text(encoding="utf-8")) if self.state_file.exists() else {}
    def save(self, state):
        tmp = self.state_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"); tmp.replace(self.state_file)
    def audit(self, event):
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), **event}
        with self.audit_file.open("a", encoding="utf-8") as f: f.write(json.dumps(record, ensure_ascii=False) + "\n")
