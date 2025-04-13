CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR NOT NULL,
    oauth_consumer_key VARCHAR,
    lis_result_sourcedid VARCHAR,
    lis_outcome_service_url VARCHAR,
    is_correct VARCHAR(1),  -- Например, "1"/"0" или Null
    attempt_type VARCHAR(6), -- Например, "run"/"submit"
    created_at TIMESTAMP
);