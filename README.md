# Bank Reviews Database

## Task 3: Store Cleaned Data in PostgreSQL

### Database Schema

#### Table: `banks`
- `bank_id` (VARCHAR, PRIMARY KEY): Unique identifier for each bank
- `bank_name` (VARCHAR): Full name of the bank
- `app_name` (VARCHAR): Name of the mobile banking application

#### Table: `reviews`
- `review_id` (VARCHAR, PRIMARY KEY): Unique identifier for each review
- `bank_id` (VARCHAR, FOREIGN KEY): Reference to banks table
- `review_text` (TEXT): The actual review content
- `rating` (NUMERIC): User rating (1-5 scale)
- `review_date` (DATE): Date when review was posted
- `sentiment_label` (VARCHAR): Sentiment classification (POSITIVE/NEGATIVE/NEUTRAL)
- `sentiment_score` (NUMERIC): Sentiment analysis confidence score (0-1)
- `source` (VARCHAR): Source of the review (e.g., Google Play Store)

### Key Features
- **Referential Integrity**: Foreign key constraint ensures all reviews reference valid banks
- **Data Validation**: Appropriate data types and constraints
- **Performance**: Indexes on frequently queried columns
- **Scalability**: Supports large volumes of review data

### Current Statistics
- **Banks**: 3 (Bank of Abyssinia, Commercial Bank of Ethiopia, Dashen Bank)
- **Total Reviews**: 1,200+
- **Average Rating**: 3.82/5
- **Data Completeness**: 100% bank linkage, minimal NULL values

### Usage
1. Create database: `createdb bank_reviews`
2. Import schema: `psql -d bank_reviews -f schema.sql`
3. Run the Jupyter notebook `db_insert_bank_reviews.ipynb` to populate data

### Verification Queries
See `schema.sql` for sample verification queries.

### Files in Repository
- `db_insert_bank_reviews.ipynb`: Complete Jupyter notebook with all code
- `schema.sql`: Database schema and sample data
- `README.md`: This documentation file
