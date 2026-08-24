import argparse
import os
import statistics
import time

import psycopg
from pymongo import MongoClient


SQL = {
    "line_summary": "SELECT line, AVG(delay_minutes) FROM transit_events GROUP BY line",
    "station_window": "SELECT AVG(passenger_count) FROM transit_events WHERE station_id='S010' AND recorded_at >= '2025-02-01' AND recorded_at < '2025-03-01'",
}

MONGO = {
    "line_summary": [{"$group": {"_id": "$line", "average_delay": {"$avg": "$delay_minutes"}}}],
    "station_window": [
        {"$match": {"station_id": "S010", "recorded_at": {"$gte": __import__("datetime").datetime(2025, 2, 1), "$lt": __import__("datetime").datetime(2025, 3, 1)}}},
        {"$group": {"_id": None, "average_passengers": {"$avg": "$passenger_count"}}},
    ],
}


def median_time(callable_, repetitions=7):
    callable_()  # warm-up
    samples = []
    for _ in range(repetitions):
        start = time.perf_counter()
        list(callable_())
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def run(postgres_dsn: str, mongo_uri: str, repetitions: int = 7):
    mongo = MongoClient(mongo_uri).benchmark.transit_events
    results = []
    with psycopg.connect(postgres_dsn) as connection:
        for name in SQL:
            def sql_call(query=SQL[name]):
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
            results.append((name, "PostgreSQL", median_time(sql_call, repetitions)))
            results.append((name, "MongoDB", median_time(lambda pipeline=MONGO[name]: mongo.aggregate(pipeline), repetitions)))
    for row in results:
        print(f"{row[0]:16} {row[1]:10} median={row[2]:.3f} ms")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repetitions", type=int, default=7)
    args = parser.parse_args()
    run(os.getenv("POSTGRES_DSN", "postgresql://benchmark:benchmark@localhost:5432/benchmark"), os.getenv("MONGO_URI", "mongodb://localhost:27017"), args.repetitions)
