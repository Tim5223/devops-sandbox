-- Runs automatically on first `docker compose up`
-- Add your schema here as the project grows

CREATE TABLE IF NOT EXISTS healthcheck (
    id      SERIAL PRIMARY KEY,
    checked_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO healthcheck DEFAULT VALUES;