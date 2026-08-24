import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate(rows: int = 50_000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    stations = np.array([f"S{i:03d}" for i in range(100)])
    timestamps = pd.date_range("2025-01-01", periods=24 * 90, freq="h")
    return pd.DataFrame({
        "event_id": np.arange(1, rows + 1),
        "station_id": rng.choice(stations, rows),
        "recorded_at": rng.choice(timestamps, rows),
        "passenger_count": rng.poisson(35, rows),
        "delay_minutes": np.maximum(0, rng.normal(5, 7, rows)).round(2),
        "line": rng.choice(["A", "B", "C", "D", "E"], rows),
    }).sort_values("event_id").reset_index(drop=True)


def write_csv(output: str = "data/events.csv", rows: int = 50_000) -> Path:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    generate(rows=rows).to_csv(destination, index=False)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=50_000)
    parser.add_argument("--output", default="data/events.csv")
    args = parser.parse_args()
    print(write_csv(args.output, args.rows))
