CREATE TABLE earnings (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    report_date DATE,
    eps_actual FLOAT,
    eps_estimate FLOAT,
    revenue_actual FLOAT,
    revenue_estimate FLOAT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);