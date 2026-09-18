from ambivikhry.hundred_iteration import HundredIterationProtocol


def test_hundred_iteration_protocol():
    run = HundredIterationProtocol().run("Познать мир и интернет", iterations=100)
    assert run.iterations == 100
    assert len(run.turns) == 400
    assert run.turns[-1].iteration == 100
