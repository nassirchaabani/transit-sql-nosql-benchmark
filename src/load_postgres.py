import argparse
import os
from pathlib import Path

import psycopg


def load(csv_path: str, dsn: str):
    schema = Path(__file__).parents[1] / "sql" / "schema.sql"
    with psycopg.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema.read_text(encoding="utf-8"))
            cursor.execute("TRUNCATE transit_events")
            with Path(csv_path).open("r", encoding="utf-8") as source:
                with cursor.copy("COPY transit_events FROM STDIN WITH (FORMAT CSV, HEADER TRUE)") as copy:
                    while chunk := source.read(1024 * 1024):
                        copy.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/events.csv")
    parser.add_argument("--dsn", default=os.getenv("POSTGRES_DSN", "postgresql://benchmark:benchmark@localhost:5432/benchmark"))
    args = parser.parse_args()
    load(args.csv, args.dsn)
