import pandas as pd

from src.generate_data import generate, write_csv


def test_generation_is_reproducible_and_valid():
    first = generate(rows=100, seed=7)
    second = generate(rows=100, seed=7)
    assert first.equals(second)
    assert len(first) == 100
    assert first["event_id"].is_unique
    assert (first["passenger_count"] >= 0).all()
    assert (first["delay_minutes"] >= 0).all()
    assert set(first["line"]).issubset({"A", "B", "C", "D", "E"})


def test_write_csv_creates_parent_directory(tmp_path):
    output = tmp_path / "nested" / "events.csv"

    written = write_csv(str(output), rows=25)
    frame = pd.read_csv(written)

    assert written == output
    assert output.exists()
    assert len(frame) == 25
    assert list(frame.columns) == [
        "event_id",
        "station_id",
        "recorded_at",
        "passenger_count",
        "delay_minutes",
        "line",
    ]
