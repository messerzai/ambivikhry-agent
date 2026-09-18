from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import uuid
from .core import AmbivikhryCore
from .llm import LLMProvider
from .memory import JsonMemory
from .policy import PolicyGate
from .tools import ToolRegistry, DryRunAdapter

@dataclass
class AgentConfig:
    max_iterations: int = 4
    confidence_stop: float = 0.85
    humanitarian_objective: str = "Increase useful, truthful, safe, human-beneficial outcomes; avoid coercion, deception, hidden propagation, and irreversible action without approval."

@dataclass
class AgentResult:
    instance_id: str; task: str; status: str; answer: str; confidence: float; iterations: int
    audit: list[dict[str, Any]] = field(default_factory=list)

class AmbivikhryAgent:
    def __init__(self, *, provider: LLMProvider, workdir: str, config=None, tools=None, tool_adapter=None, instance_id=None):
        self.provider=provider; self.config=config or AgentConfig(); self.core=AmbivikhryCore(); self.memory=JsonMemory(workdir); self.policy=PolicyGate(); self.tools=tools or ToolRegistry(); self.adapter=tool_adapter or DryRunAdapter(); self.instance_id=instance_id or "av-"+uuid.uuid4().hex[:12]; self.audit=[]
    def _log(self,event):
        event={"instance_id":self.instance_id,**event}; self.audit.append(event); self.memory.audit(event)
    def run(self, task: str) -> AgentResult:
        state=self.core.intake(task); self._log({"event":"intake","task":task}); answer=""; confidence=0.0
        for iteration in range(1,self.config.max_iterations+1):
            prompt=(f"Task: {state.task}\nHuman-benefit constraint: {self.config.humanitarian_objective}\nKnown facts: {state.facts}\nHypotheses: {state.hypotheses}\nUnknowns: {state.unknowns}\nVerified: {state.verification}\nPrevious observations: {state.observations}\nReturn structured JSON with decision, tool_calls, confidence, stop, unknowns, verification_plan, reason.")
            proposal=self.provider.generate([{"role":"system","content":"Operate the Ambivikhry protocol."},{"role":"user","content":prompt}],{"type":"object"})
            confidence=float(proposal.get("confidence",0)); answer=str(proposal.get("decision",""))
            for unknown in proposal.get("unknowns",[]):
                if unknown not in state.unknowns: state.unknowns.append(str(unknown))
            for call in proposal.get("tool_calls",[]):
                name=call.get("name")
                if name not in [x["name"] for x in self.tools.describe()]: self._log({"event":"tool_rejected","reason":"unknown_tool","name":name}); continue
                tool=self.tools.get(name); decision=self.policy.evaluate(tool,user_approved=False)
                if not decision.allowed: self._log({"event":"tool_blocked","tool":name,"reason":decision.reason}); continue
                self._log({"event":"tool_dry_run","result":self.adapter.execute(tool,call.get("args",{}))})
            self._log({"event":"cycle","iteration":iteration,"confidence":confidence,"answer":answer,"unknowns":state.unknowns,"verification_plan":proposal.get("verification_plan",[])})
            if proposal.get("stop") or self.core.should_stop(confidence,len(state.unknowns),iteration,self.config.max_iterations):
                self.core.reenter(state,{"observation":"bounded cycle completed","what_changed":"structured proposal evaluated","error_found":"","next_adjustment":"verify critical external claims when a real verifier is connected"}); self._log({"event":"reentry","state":state.reentry}); break
        self.memory.save({"instance_id":self.instance_id,"task":task,"last_answer":answer,"confidence":confidence,"reentry":state.reentry})
        return AgentResult(self.instance_id,task,"completed",answer,confidence,iteration,self.audit)
