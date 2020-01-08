from ai.search.local.hill_climbing import search

EPSILON = 1e-6


def test_hill_climbing(convex):
    state, value = search(convex)
    assert 1.6 - EPSILON <= state <= 1.6 + EPSILON
    assert 0.9995736030415051 - EPSILON <= value <= 0.9995736030415051 + EPSILON


def test_hill_climbing_plateau(convex_flat_negative):
    state, value = search(convex_flat_negative, sideways_moves=True)
    assert 1.6 - EPSILON <= state <= 1.6 + EPSILON
    assert 0.9995736030415051 - EPSILON <= value <= 0.9995736030415051 + EPSILON
