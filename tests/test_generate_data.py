from src.generate_data import generate


def test_generation_is_reproducible_and_valid():
    first = generate(rows=100, seed=7)
    second = generate(rows=100, seed=7)
    assert first.equals(second)
    assert len(first) == 100
    assert first["event_id"].is_unique
    assert (first["passenger_count"] >= 0).all()
    assert (first["delay_minutes"] >= 0).all()
