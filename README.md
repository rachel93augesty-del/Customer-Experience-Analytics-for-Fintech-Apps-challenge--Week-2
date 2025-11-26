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