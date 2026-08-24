CREATE TABLE IF NOT EXISTS transit_events (
    event_id BIGINT PRIMARY KEY,
    station_id VARCHAR(8) NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    passenger_count INTEGER NOT NULL CHECK (passenger_count >= 0),
    delay_minutes DOUBLE PRECISION NOT NULL CHECK (delay_minutes >= 0),
    line VARCHAR(4) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_station_time ON transit_events (station_id, recorded_at);
CREATE INDEX IF NOT EXISTS idx_events_line ON transit_events (line);
