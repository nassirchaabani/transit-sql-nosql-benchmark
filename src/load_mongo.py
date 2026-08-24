import argparse
import os

import pandas as pd
from pymongo import ASCENDING, MongoClient


def load(csv_path: str, uri: str):
    frame = pd.read_csv(csv_path, parse_dates=["recorded_at"])
    client = MongoClient(uri)
    collection = client.benchmark.transit_events
    collection.delete_many({})
    records = frame.to_dict("records")
    for start in range(0, len(records), 5_000):
        collection.insert_many(records[start:start + 5_000])
    collection.create_index([("station_id", ASCENDING), ("recorded_at", ASCENDING)])
    collection.create_index([("line", ASCENDING)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/events.csv")
    parser.add_argument("--uri", default=os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    args = parser.parse_args()
    load(args.csv, args.uri)
