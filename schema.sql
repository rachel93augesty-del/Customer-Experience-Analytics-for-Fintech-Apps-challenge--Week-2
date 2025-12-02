
-- PostgreSQL Schema for Bank Reviews Database
-- Generated for Task 3: Store Cleaned Data in PostgreSQL

-- Database: bank_reviews

-- Table: banks
CREATE TABLE IF NOT EXISTS banks (
    bank_id VARCHAR(10) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100)
);

-- Table: reviews
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    bank_id VARCHAR(10) REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating NUMERIC(3,1),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC(3,2),
    source VARCHAR(50)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);

-- Sample data for banks table
INSERT INTO banks (bank_id, bank_name, app_name) VALUES
('BOA', 'Bank of Abyssinia', 'BOA Mobile Banking'),
('CBE', 'Commercial Bank of Ethiopia', 'CBE Birr'),
('DASHEN', 'Dashen Bank', 'Dashen Bank Mobile')
ON CONFLICT (bank_id) DO NOTHING;

-- Verification queries (for documentation)
/*
-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id) as review_count
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name
ORDER BY review_count DESC;

-- Average rating per bank
SELECT b.bank_name, ROUND(AVG(r.rating), 2) as avg_rating
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
WHERE r.rating IS NOT NULL
GROUP BY b.bank_name
ORDER BY avg_rating DESC;
*/
