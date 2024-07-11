-- Table for storing stock information
CREATE TABLE stocks (
    stock_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(100)
);

-- Table for storing daily stock prices
CREATE TABLE stock_prices (
    price_id SERIAL PRIMARY KEY,
    stock_id INT NOT NULL REFERENCES stocks(stock_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    open NUMERIC(10, 2),
    high NUMERIC(10, 2),
    low NUMERIC(10, 2),
    close NUMERIC(10, 2),
    volume BIGINT,
    UNIQUE (stock_id, date)
);

-- Indexes for optimizing queries
CREATE INDEX idx_stock_symbol ON stocks(symbol);
CREATE INDEX idx_stock_price_date ON stock_prices(date);