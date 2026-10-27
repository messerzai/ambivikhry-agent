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
            "profile_lifecycle": {},
            "profile_history": [],
        }

    def save_profile(self, profile):
        tmp = self.profile_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.profile_file)

    PROFILE_LIST_FIELDS = (
        "goals", "constraints", "preferences", "working_style", "strengths",
        "friction", "successful_strategies", "failed_strategies", "open_questions",
    )

    # Prompt-path limits are deterministic safety/performance heuristics, not
    # claims about an optimal context size.
    MAX_PROFILE_ITEMS_PER_FIELD = 20
    MAX_PROFILE_ITEM_CHARS = 2000
    MAX_PROFILE_CONTEXT_CHARS = 20_000

    def revise_profile_item(
        self, field: str, value: str, action: str, *, replacement: str | None = None
    ):
        """Apply an explicit user-confirmed lifecycle action to one profile item.

        Supported actions are confirm, dismiss, and correct. A dismissed or
        superseded value is not silently re-added by later inferred hints.
        """
        if field not in self.PROFILE_LIST_FIELDS:
            raise ValueError("unsupported profile field")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("value must be a non-empty string")
        if not isinstance(action, str) or action not in {"confirm", "dismiss", "correct"}:
            raise ValueError("action must be confirm, dismiss, or correct")
        if action == "correct":
            if not isinstance(replacement, str) or not replacement.strip():
                raise ValueError("correct requires a non-empty replacement")
            if replacement == value:
                raise ValueError("replacement must differ from the original value")
        elif replacement is not None:
            raise ValueError("replacement is only valid for correct")

        profile = self.load_profile()
        lifecycle = profile.get("profile_lifecycle")
        if not isinstance(lifecycle, dict):
            lifecycle = {}
        history = profile.get("profile_history")
        if not isinstance(history, list):
            history = []
        profile["profile_lifecycle"] = lifecycle
        profile["profile_history"] = history

        items = profile.get(field, [])
        if not isinstance(items, list):
            raise ValueError("profile field must contain a list")
        profile[field] = items
        field_lifecycle = lifecycle.get(field)
        if not isinstance(field_lifecycle, dict):
            field_lifecycle = {}
        lifecycle[field] = field_lifecycle

        if action == "correct" and value not in items:
            raise ValueError("cannot correct a value that is not active")

        timestamp = datetime.now(timezone.utc).isoformat()
        events = []
        if action == "confirm":
            if value not in items:
                items.append(value)
            field_lifecycle[value] = {"status": "confirmed", "updated_at": timestamp}
            events.append({
                "timestamp": timestamp, "field": field, "value": value,
                "action": "confirmed", "source": "user_explicit",
            })
        elif action == "dismiss":
            profile[field] = [item for item in items if item != value]
            field_lifecycle[value] = {"status": "dismissed", "updated_at": timestamp}
            events.append({
                "timestamp": timestamp, "field": field, "value": value,
                "action": "dismissed", "source": "user_explicit",
            })
        else:
            profile[field] = [item for item in items if item != value]
            if replacement not in profile[field]:
                profile[field].append(replacement)
            field_lifecycle[value] = {
                "status": "superseded", "updated_at": timestamp,
                "replacement": replacement,
            }
            field_lifecycle[replacement] = {
                "status": "confirmed", "updated_at": timestamp,
            }
            events.extend([
                {
                    "timestamp": timestamp, "field": field, "value": value,
                    "action": "corrected", "replacement": replacement,
                    "source": "user_explicit",
                },
                {
                    "timestamp": timestamp, "field": field, "value": replacement,
                    "action": "confirmed", "source": "user_explicit",
                },
            ])

        # Keep a bounded event trail; lifecycle state persists separately so
        # a trimmed history does not reactivate dismissed or superseded values.
        profile["profile_history"] = (history + events)[-500:]
        self.save_profile(profile)
        # Audit metadata only; do not duplicate the profile text into audit.jsonl.
        self.audit({
            "event": "profile_item_lifecycle",
            "field": field,
            "action": action,
        })
        return deepcopy(profile)

    def personalize(
        self, task: str, hints: dict | None = None, *, explicit_user_input: bool = False
    ):
        """Create/update a user instance without pretending inferences are facts."""
        profile = self.load_profile()
        if not isinstance(explicit_user_input, bool):
            raise ValueError("explicit_user_input must be a boolean")
        if hints is None:
            hints = {}
        if not isinstance(hints, dict):
            raise ValueError("hints must be a dictionary")
        if not isinstance(profile.get("profile_lifecycle"), dict):
            profile["profile_lifecycle"] = {}
        if not isinstance(profile.get("profile_history"), list):
            profile["profile_history"] = []
        for field_name in self.PROFILE_LIST_FIELDS:
            if not isinstance(profile.get(field_name), list):
                profile[field_name] = []
        if not isinstance(profile.get("observations"), list):
            profile["observations"] = []
        if not isinstance(profile.get("confidence"), dict):
            profile["confidence"] = {}
        profile["status"] = "active"
        profile["observations"].append({
            "text": task,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "user_task",
        })
        profile["observations"] = profile["observations"][-50:]
        explicit_events = []
        explicit_timestamp = datetime.now(timezone.utc).isoformat()
        for key in ("goals", "constraints", "preferences", "working_style", "strengths", "friction",
                    "successful_strategies", "failed_strategies", "open_questions"):
            values = hints.get(key, [])
            for value in values:
                value = str(value)
                if not value:
                    continue
                field_lifecycle = profile["profile_lifecycle"].get(key, {})
                item_state = field_lifecycle.get(value, {}) if isinstance(field_lifecycle, dict) else {}
                is_blocked = (
                    isinstance(item_state, dict)
                    and item_state.get("status") in {"dismissed", "superseded"}
                )
                if is_blocked and not explicit_user_input:
                    continue
                if value not in profile[key]:
                    profile[key].append(value)
                if explicit_user_input:
                    if not isinstance(field_lifecycle, dict):
                        field_lifecycle = {}
                        profile["profile_lifecycle"][key] = field_lifecycle
                    field_lifecycle[value] = {
                        "status": "confirmed", "updated_at": explicit_timestamp,
                    }
                    explicit_events.append({
                        "timestamp": explicit_timestamp, "field": key, "value": value,
                        "action": "confirmed", "source": "user_explicit",
                    })
        if explicit_events:
            profile["profile_history"] = (profile["profile_history"] + explicit_events)[-500:]
        profile["confidence"].update({k: float(v) for k, v in hints.get("confidence", {}).items()})
        self.save_profile(profile)
        return deepcopy(profile)

    @staticmethod
    def profile_context(profile):
        """Build a bounded, model-visible projection of active profile items.

        Persisted lifecycle/history and raw observations remain available for
        user review and audit, but are excluded from prompts. The projection
        applies per-item, per-field, and total serialized-size limits. Within
        each field, the newest retained items are preferred; selection proceeds
        round-robin across fields so one large field cannot consume the budget.
        """
        if not isinstance(profile, dict):
            raise ValueError("profile must be a dictionary")

        raw_version = profile.get("version", 1)
        version = (
            raw_version
            if isinstance(raw_version, int) and not isinstance(raw_version, bool) and raw_version >= 1
            else 1
        )
        # Status is control metadata, not free-form profile text. Allow only
        # values currently emitted by the runtime; unknown legacy values fail closed.
        allowed_statuses = {"bootstrap", "active", "unknown"}
        raw_status = profile.get("status", "unknown")
        status = raw_status if isinstance(raw_status, str) and raw_status in allowed_statuses else "unknown"
        context = {"version": version, "status": status}
        lifecycle = profile.get("profile_lifecycle", {})
        if not isinstance(lifecycle, dict):
            lifecycle = {}

        candidates_by_field = {}
        selected_by_field = {}
        blocked_fields = set()
        for field_name in JsonMemory.PROFILE_LIST_FIELDS:
            items = profile.get(field_name, [])
            if not isinstance(items, list):
                items = []
            field_lifecycle = lifecycle.get(field_name, {})
            if not isinstance(field_lifecycle, dict):
                field_lifecycle = {}
            active_items = []
            for item in items:
                # Persisted legacy/corrupt profiles may contain arbitrary JSON
                # objects. Only non-empty strings within the item limit are eligible.
                if (
                    not isinstance(item, str)
                    or not item.strip()
                    or len(item) > JsonMemory.MAX_PROFILE_ITEM_CHARS
                ):
                    continue
                item_state = field_lifecycle.get(item, {})
                if (
                    isinstance(item_state, dict)
                    and item_state.get("status") in {"dismissed", "superseded"}
                ):
                    continue
                active_items.append(item)

            candidates_by_field[field_name] = active_items[-JsonMemory.MAX_PROFILE_ITEMS_PER_FIELD:]
            selected_by_field[field_name] = []
            context[field_name] = []

        # Prefer each field's newest value before admitting older values from
        # any field. This bounds prompt size while reducing field-order bias.
        depth = 1
        while True:
            made_progress = False
            for field_name in JsonMemory.PROFILE_LIST_FIELDS:
                candidates = candidates_by_field[field_name]
                if field_name in blocked_fields or depth > len(candidates):
                    continue

                item = candidates[-depth]
                tentative = deepcopy(context)
                tentative[field_name] = list(reversed(selected_by_field[field_name] + [item]))
                serialized = json.dumps(tentative, ensure_ascii=False, indent=2)
                if len(serialized) > JsonMemory.MAX_PROFILE_CONTEXT_CHARS:
                    # Keep the newest values already selected for this field;
                    # do not skip a newer value to admit an older one.
                    blocked_fields.add(field_name)
                    continue

                selected_by_field[field_name].append(item)
                context[field_name] = list(reversed(selected_by_field[field_name]))
                made_progress = True

            if not made_progress:
                break
            depth += 1

        # Deliberately do not pass raw observations, lifecycle keys, event
        # history, confidence internals, or unknown extension fields to the LLM.
        return json.dumps(context, ensure_ascii=False, indent=2)
