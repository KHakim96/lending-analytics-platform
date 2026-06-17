DROP TABLE IF EXISTS pipeline_runs;

CREATE TABLE pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    process_name VARCHAR(100),
    status VARCHAR(20),
    row_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);