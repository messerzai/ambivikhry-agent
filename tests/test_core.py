from ambivikhry.core import AmbivikhryCore

def test_score():
    c=AmbivikhryCore(); assert 0 <= c.score(relevance=.9,reliability=.9,verifiability=.9,usefulness=.9) <= 1

def test_stop():
    c=AmbivikhryCore(); assert c.should_stop(.9,0,1,4); assert c.should_stop(.1,0,4,4)
