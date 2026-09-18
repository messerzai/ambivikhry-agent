"""25 deterministic adversarial experiments for the Ambivikhry core.

These tests exercise reasoning hygiene and control boundaries without external
network access, credentials, or irreversible side effects.
"""
from ambivikhry.verifier import Verifier
from ambivikhry.policy import PolicyGate
from ambivikhry.tools import Tool
from ambivikhry.autonomy import AutonomousController, AutonomyConfig

V = Verifier()
P = PolicyGate()

def case(name, fn):
    try:
        fn(); return (name, "PASS")
    except Exception as e:
        return (name, f"FAIL: {e}")

def main():
    results=[]
    results += [case("01 missing decision", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"confidence":0.2}).passed else None)]
    results += [case("02 unresolved unknown + high confidence", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":0.95,"unknowns":["u"]}).passed else None)]
    results += [case("03 sourced normal claim", lambda: (_ for _ in ()).throw(AssertionError()) if not V.verify({"decision":"x","confidence":0.8,"facts":["f"]}).passed else None)]
    results += [case("04 unsourced claims", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":0.8,"claims_without_sources":True}).passed else None)]
    results += [case("05 confidence clamp", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":2}).score > 1 else None)]
    results += [case("06 negative confidence clamp", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":-1}).score < 0 else None)]
    results += [case("07 high-risk denied", lambda: (_ for _ in ()).throw(AssertionError()) if P.evaluate(Tool("x", risk="high")).allowed else None)]
    results += [case("08 high-risk approved", lambda: (_ for _ in ()).throw(AssertionError()) if not P.evaluate(Tool("x", risk="high"), user_approved=True).allowed else None)]
    results += [case("09 approval-required denied", lambda: (_ for _ in ()).throw(AssertionError()) if P.evaluate(Tool("x", requires_approval=True)).allowed else None)]
    results += [case("10 normal tool allowed", lambda: (_ for _ in ()).throw(AssertionError()) if not P.evaluate(Tool("x")).allowed else None)]
    results += [case("11 replication not explicit", lambda: (_ for _ in ()).throw(AssertionError()) if P.allows_replication(explicit=False,destination_is_local=True).allowed else None)]
    results += [case("12 replication nonlocal denied", lambda: (_ for _ in ()).throw(AssertionError()) if P.allows_replication(explicit=True,destination_is_local=False).allowed else None)]
    results += [case("13 local explicit replication", lambda: (_ for _ in ()).throw(AssertionError()) if not P.allows_replication(explicit=True,destination_is_local=True).allowed else None)]
    results += [case("14 autonomy bounded", lambda: (_ for _ in ()).throw(AssertionError()) if len(AutonomousController(AutonomyConfig(max_cycles=3)).run(lambda c:{"kind":"progress"})) != 3 else None)]
    results += [case("15 autonomy early stop", lambda: (_ for _ in ()).throw(AssertionError()) if len(AutonomousController(AutonomyConfig(max_cycles=8)).run(lambda c:{"stop":c==2})) != 2 else None)]
    results += [case("16 zero confidence rejected?", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":0}).score != 0 else None)]
    results += [case("17 empty unknowns okay", lambda: (_ for _ in ()).throw(AssertionError()) if not V.verify({"decision":"x","confidence":0.7,"unknowns":[]}).passed else None)]
    results += [case("18 multiple unknowns detected", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":0.9,"unknowns":["a","b"]}).passed else None)]
    results += [case("19 ordinary decision survives", lambda: (_ for _ in ()).throw(AssertionError()) if not V.verify({"decision":"stop","confidence":0.6}).passed else None)]
    results += [case("20 risk beats convenience", lambda: (_ for _ in ()).throw(AssertionError()) if P.evaluate(Tool("x",risk="high"),user_approved=False).allowed else None)]
    results += [case("21 approval is explicit", lambda: (_ for _ in ()).throw(AssertionError()) if not P.evaluate(Tool("x",requires_approval=True),user_approved=True).allowed else None)]
    results += [case("22 audit events emitted", lambda: (_ for _ in ()).throw(AssertionError()) if len(AutonomousController(AutonomyConfig(max_cycles=2)).run(lambda c:{"kind":"p"})) != 2 else None)]
    results += [case("23 deterministic repeat", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":0.73}).score != V.verify({"decision":"x","confidence":0.73}).score else None)]
    results += [case("24 contradiction lowers score", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({"decision":"x","confidence":0.9,"unknowns":["contradiction"]}).score >= 0.9 else None)]
    results += [case("25 fail closed on absent decision", lambda: (_ for _ in ()).throw(AssertionError()) if V.verify({}).passed else None)]
    passed=sum(x[1]=="PASS" for x in results)
    print(f"25-EXPERIMENT SUITE: {passed}/25 PASS")
    for n,r in results: print(f"{n}: {r}")
    assert passed == 25

if __name__ == "__main__": main()
