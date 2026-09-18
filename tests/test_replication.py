from ambivikhry.replication import Replicator

def test_local_replication(tmp_path):
    parent=tmp_path/"parent"; parent.mkdir(); child=tmp_path/"child"
    out=Replicator(parent).replicate(parent_manifest={"instance_id":"parent-1","replication_generation":0},destination=child,explicit_confirmation=True,mutation={"type":"proposal","summary":"one bounded improvement"})
    assert out["parent_instance_id"]=="parent-1"
    assert out["replication_generation"]==1
    assert out["autostart"] is False
