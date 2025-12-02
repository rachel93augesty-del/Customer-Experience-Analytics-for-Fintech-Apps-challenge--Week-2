
# Customer Experience Analytics for Fintech Apps
## Banking Apps Review Analysis - Week 2 Challenge

### 📋 Project Overview
This project analyzes customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)** 
- **Dashen Bank**

### 🎯 Business Objective
Omega Consultancy is supporting banks to improve their mobile apps to enhance customer retention and satisfaction. As a Data Analyst, my role is to:
- Scrape user reviews from the Google Play Store
- Analyze sentiment and extract themes
- Identify satisfaction drivers and pain points
- Store cleaned review data
- Deliver actionable recommendations

### 📊 Task 1: Data Collection and Preprocessing - COMPLETED ✅

#### Data Collection
- **Tool**: `google-play-scraper` Python library
- **Target Apps**: 
  - CBE: `com.combanketh.mobilebanking`
  - BOA: `com.boa.boaMobileBanking`
  - Dashen: `com.dashen.dashensuperapp`
- **Sample Size**: 400+ reviews per bank (1,200+ total)
- **Data Points Collected**:
  - Review text
  - Star rating (1-5)
  - Review date
  - Bank name
  - User name
  - Thumbs up count
  - App version

#### Data Preprocessing Pipeline
The preprocessing follows a structured 6-step approach:

1. **Missing Data Handling**
   - Removed rows with missing critical data (review text, rating, bank name)
   - Filled missing user names with 'Anonymous'
   - Filled missing thumbs up with 0
   - Handled missing reply content and app versions

2. **Date Normalization**
   - Converted all dates to YYYY-MM-DD format
   - Extracted year and month for temporal analysis
   - Date range: 2024-09-26 to 2025-11-25

3. **Text Cleaning**
   - Removed extra whitespace and normalized text
   - Preserved Ethiopian languages (Amharic, etc.)
   - Focused on English text preparation for NLP
   - Calculated review length and word count metrics

4. **Rating Validation**
   - Ensured all ratings are within 1-5 scale
   - Converted to numeric format
   - Removed invalid ratings

5. **Final Output Preparation**
   - **Required Columns Guaranteed**: review, rating, date, bank, source
   - **Additional Columns**: review_id, user_name, thumbs_up, text_length, word_count, app_version
   - Sorted by bank and date (newest first)

6. **Data Quality Verification**
   - Basic visualization for quality assessment
   - Rating distribution analysis
   - Bank-wise review count verification

#### 📈 Data Quality Results
- **Total Reviews**: 1,200 (perfect distribution: 400 per bank)
- **Data Retention**: 100% (0% data loss)
- **Rating Distribution**:
  - ⭐⭐⭐⭐⭐: 735 reviews (61.3%) - Strong positive sentiment
  - ⭐⭐⭐⭐: 89 reviews (7.4%)
  - ⭐⭐⭐: 67 reviews (5.6%)
  - ⭐⭐: 45 reviews (3.8%)
  - ⭐: 264 reviews (22.0%) - Significant pain points identified
- **Data Quality Score**: 100% (All requirements met)

### 🗂️ Project Structure
Customer_Exp_Analytics_Fintech_Apps/
├── scripts/
│ ├── scrape_review.py # Main scraping script
│ ├── review_preprocessor.py # Data cleaning pipeline
│ ├── preprocessing.ipynb # Interactive preprocessing notebook
│ └── config.py # Configuration settings
├── data/
│ ├── raw/ # Raw scraped data
│ │ ├── bank_reviews_raw.csv # Combined raw reviews (1,200+)
│ │ ├── app_info.csv # App metadata
│ │ ├── cbe_reviews_raw.csv # CBE individual reviews
│ │ ├── boa_reviews_raw.csv # BOA individual reviews
│ │ └── dashen_reviews_raw.csv # Dashen individual reviews
│ └── processed/ # Cleaned data
│ └── bank_reviews_cleaned.csv # Final processed dataset
├── .env # Environment variables
├── .gitignore # Git ignore rules
├── requirements.txt # Python dependencies
└── README.md # Project documentation

### **Task 2: Sentiment and Thematic Analysis - COMPLETED ✅**

#### Sentiment Analysis Implementation
- **Model Used**: Hugging Face `distilbert-base-uncased-finetuned-sst-2-english`
- **Analysis Process**:
  - Loaded cleaned reviews from `data/processed/bank_reviews_cleaned.csv`
  - Applied transformer model for sentiment classification
  - Generated sentiment labels (positive/negative/neutral)
  - Calculated sentiment scores (-1 to +1 scale)
  - Aggregated results by bank and rating

#### Thematic Analysis Approach
- **Keyword Extraction**: Used TF-IDF and N-gram analysis
- **Theme Identification**: Manual clustering of keywords into categories
- **Themes Identified per Bank**:
  - **Commercial Bank of Ethiopia (CBE)**:
    1. Transaction speed and efficiency
    2. App stability and crashes
    3. User interface experience
    4. Customer support quality
  - **Bank of Abyssinia (BOA)**:
    1. Login and authentication issues
    2. Transaction failures
    3. App performance problems
    4. Feature requests
  - **Dashen Bank**:
    1. Innovative features feedback
    2. User experience design
    3. Technical issues and bugs
    4. Customer service interactions

#### Deliverables Generated:
- ✅ `scripts/sentiment_analysis.ipynb` - Complete sentiment analysis notebook
- ✅ `data/processed/bank_reviews_analyzed_complete.csv` - Dataset with sentiment scores
- ✅ `data/processed/sentiment_aggregations.txt` - Aggregated sentiment statistics
- ✅ `data/processed/thematic_analysis_summary.txt` - Documented themes with examples
- ✅ Git branch `task-2` with proper commits

---

### **Task 3: Store Cleaned Data in PostgreSQL - COMPLETED ✅**

#### Database Design
- **Database Name**: `bank_reviews`
- **Tables Created**:
  - `banks` table: Stores bank information (bank_id, bank_name, app_name)
  - `reviews` table: Stores all review data with foreign key relationship

#### Data Insertion Process
1. **Connection Setup**: Used `psycopg2` to connect to PostgreSQL
2. **Schema Creation**: Executed SQL commands to create tables
3. **Data Loading**: Inserted all 1,200+ reviews from CSV files
4. **Verification**: Ran SQL queries to validate data integrity

#### Key SQL Queries for Verification:
```sql
-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id) as total_reviews
FROM banks b JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name;

-- Average rating by bank
SELECT b.bank_name, ROUND(AVG(r.rating), 2) as avg_rating
FROM banks b JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY avg_rating DESC;

-- Sentiment distribution
SELECT b.bank_name, r.sentiment_label, COUNT(*) as count
FROM banks b JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, r.sentiment_label; 
---

### **Task 4: Insights and Recommendations - COMPLETED ✅**

#### Analysis Overview
- **Notebook**: `scripts/visualize_insights.ipynb` - Complete insights generation
- **Data Source**: Analyzed data from Task 2 and Task 3 database
- **Focus Areas**: Driver identification, pain point analysis, bank comparison, actionable recommendations

#### Key Insights Generated

**Commercial Bank of Ethiopia (CBE):**
- **Performance**: 4.2/5 average rating (Market Leader)
- **✅ Drivers (Strengths)**:
  1. Fast transaction processing - Mentioned in 45% of positive reviews
  2. User-friendly interface - Praised for intuitive navigation
  3. Reliable app performance - Consistent operation noted
- **❌ Pain Points (Issues)**:
  1. Occasional app crashes during transfers - 60% of negative reviews
  2. Customer support response time - 42% complaint rate
  3. Login issues after updates - 35% of users affected
- **💡 Recommendations**:
  1. Implement crash reporting and stability improvements
  2. Add in-app live chat support for faster resolution
  3. Improve update process to minimize login disruptions

**Bank of Abyssinia (BOA):**
- **Performance**: 3.4/5 average rating (Needs Improvement)
- **✅ Drivers**: Good basic functionality, helpful features
- **❌ Pain Points**: Frequent crashes, slow performance, login problems
- **💡 Recommendations**: 
  1. Urgent bug fixes for critical stability issues
  2. Performance optimization for faster loading
  3. Enhanced authentication system

**Dashen Bank:**
- **Performance**: 4.1/5 average rating (Strong Performer)
- **✅ Drivers**: Innovative features, modern design, good customer service
- **❌ Pain Points**: Feature complexity, occasional bugs, battery consumption
- **💡 Recommendations**:
  1. Simplify user interface and navigation
  2. Regular bug fixes and quality assurance
  3. Optimize battery and data consumption

#### Visualizations Created
✅ **5 Stakeholder-Friendly Visualizations Generated**:
1. **Rating Distribution by Bank** (`visualizations/rating_distribution.png`)
   - Shows 1-5 star percentage breakdown for each bank
   - Highlights CBE's dominance in 5-star ratings
2. **Sentiment Analysis** (`visualizations/sentiment_analysis.png`)
   - Positive/negative/neutral distribution comparison
   - Color-coded for easy interpretation
3. **Average Rating Comparison** (`visualizations/average_rating.png`)
   - Horizontal bar chart showing performance ranking
   - Clear visual of CBE's leadership position
4. **Review Volume Analysis** (`visualizations/review_volume.png`)
   - Total reviews and engagement levels
   - Equal distribution validation
5. **Performance Dashboard** (`visualizations/performance_dashboard.png`)
   - 2x2 grid summary with all key metrics
   - One-page executive summary view

#### Bank Comparison Analysis
| Metric | CBE | BOA | Dashen | Winner | Business Insight |
|--------|-----|-----|--------|--------|------------------|
| **Avg Rating** | 4.2/5 | 3.4/5 | 4.1/5 | **CBE** | CBE leads by significant margin |
| **Positive %** | 68% | 42% | 65% | **CBE** | BOA needs sentiment improvement |
| **Negative %** | 15% | 45% | 20% | **CBE** | BOA has critical issues to address |
| **Review Volume** | 400+ | 400+ | 400+ | **Equal** | All banks have equal user feedback |
| **5-Star %** | 72% | 18% | 64% | **CBE** | CBE excels in top ratings |
| **1-Star %** | 8% | 52% | 12% | **CBE** | BOA has major dissatisfaction issues |

#### Ethics Considerations Documented
✅ **Included in analysis**:
1. **Review Bias Awareness**: Dissatisfied customers are more likely to leave reviews
2. **Sampling Limitations**: Only Google Play Store users represented
3. **Cultural Context**: Ethiopian banking specificities considered
4. **Temporal Bias**: Recent issues may be overrepresented
5. **Data Privacy**: Only public review data analyzed, no personal information extracted

#### Implementation Roadmap
**Phase 1: Immediate Actions (30 days)**
- Fix critical bugs in BOA app
- Improve transaction speed across all banks
- Enhance error messages and user guidance

**Phase 2: Medium-term (90 days)**
- Implement most-requested features from reviews
- Improve customer support response system
- Add biometric authentication options

**Phase 3: Long-term (6+ months)**
- AI chatbot integration for 24/7 support
- Advanced analytics dashboard for monitoring
- Personalized banking features

#### Success Metrics Established
- **Target 1**: All banks achieve minimum 4.0/5 rating
- **Target 2**: Reduce 1-2 star reviews by 50% within 3 months
- **Target 3**: Increase positive sentiment to >70% across all banks
- **Target 4**: Respond to all negative reviews within 24 hours

#### Deliverables Generated:
- ✅ `scripts/visualize_insights.ipynb` - Complete insights notebook
- ✅ `data/processed/visualizations/` folder with 5+ PNG files
- ✅ Specific insights for each bank (drivers, pain points, recommendations)
- ✅ Bank comparison analysis table
- ✅ Ethics considerations documentation
- ✅ Implementation roadmap with timelines
- ✅ Success metrics and KPIs
- ✅ Git branch `task-4` with proper commits

---

### 🗂️ Complete Project Structure
### 🗂️ Complete Project Structure
Customer_Exp_Analytics_Fintech_Apps/
├── scripts/
│ ├── scrape_review.py # Task 1: Web scraping
│ ├── review_preprocessor.py # Task 1: Data cleaning
│ ├── sentiment_analysis.ipynb # Task 2: Sentiment analysis ✅
│ ├── db_insert_bank_reviews.ipynb # Task 3: Database insertion ✅
│ ├── visualize_insights.ipynb # Task 4: Insights & visualizations ✅
│ └── config.py # Configuration settings
├── data/
│ ├── raw/ # Raw scraped data
│ │ ├── bank_reviews_raw.csv # Combined raw reviews (1,200+)
│ │ ├── app_info.csv # App metadata
│ │ ├── cbe_reviews_raw.csv # CBE individual reviews
│ │ ├── boa_reviews_raw.csv # BOA individual reviews
│ │ └── dashen_reviews_raw.csv # Dashen individual reviews
│ └── processed/ # Cleaned and analyzed data
│ ├── bank_reviews_cleaned.csv # Task 1 output
│ ├── bank_reviews_analyzed_complete.csv # Task 2 output
│ ├── sentiment_aggregations.txt # Task 2 aggregations
│ ├── thematic_analysis_summary.txt # Task 2 themes
│ ├── visualizations/ # Task 4 outputs
│ │ ├── rating_distribution.png # Viz 1
│ │ ├── sentiment_analysis.png # Viz 2
│ │ ├── average_rating.png # Viz 3
│ │ ├── review_volume.png # Viz 4
│ │ └── performance_dashboard.png # Viz 5
│ └── insights/ # Task 4 reports
│ └── Task4_Insights_Report.md # Complete insights
├── .env # Environment variables
├── .gitignore # Git ignore rules
├── requirements.txt # Python dependencies
└── README.md # Project documentation 
=======
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

