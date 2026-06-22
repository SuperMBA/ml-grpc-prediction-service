from server.simple_model import SimpleModel


def test_simple_model_probability_range():
    prob = SimpleModel().predict_proba([1.0, 2.0, 3.0])
    assert 0.0 <= prob <= 1.0


def test_simple_model_is_deterministic():
    model = SimpleModel()
    assert model.predict_proba([1.0, 2.0, 3.0]) == model.predict_proba([1.0, 2.0, 3.0])
