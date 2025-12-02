-- scripts/schema.sql
-- PostgreSQL Database Schema for Bank Reviews (Task 3)

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

-- Create banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200)
);

-- Create reviews table (linked to banks)
CREATE TABLE reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50),
    user_name VARCHAR(200),
    thumbs_up INTEGER,
    text_length INTEGER,
    word_count INTEGER,
    app_version VARCHAR(50)
);

-- Insert the three banks
INSERT INTO banks (bank_name) VALUES 
    ('Bank of Abyssinia'),
    ('Commercial Bank of Ethiopia'),
    ('Dashen Bank')
ON CONFLICT (bank_name) DO NOTHING;

-- Sample verification queries (uncomment to run)
/*
-- Check total reviews
SELECT COUNT(*) as total_reviews FROM reviews;

-- Check reviews per bank with average rating
SELECT 
    b.bank_name,
    COUNT(r.review_id) as review_count,
    AVG(r.rating) as avg_rating,
    MIN(r.review_date) as earliest_review,
    MAX(r.review_date) as latest_review
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY avg_rating DESC;
*/