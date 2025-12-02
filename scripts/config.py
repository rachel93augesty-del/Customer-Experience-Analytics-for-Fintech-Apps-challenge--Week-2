# config.py
"""
Configuration file for Google Play Store Review Scraper
Contains all app IDs, bank names, and scraping settings
"""

# App IDs for Ethiopian banks - using the correct package names you provided
APP_IDS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking', 
    'DASHEN': 'com.dashen.dashensuperapp'
}

# Full bank names for display and reporting
BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'DASHEN': 'Dashen Bank'
}

# Scraping configuration
SCRAPING_CONFIG = {
    'reviews_per_bank': 400,  # Target number of reviews per bank
    'lang': 'en',             # Language: English
    'country': 'et',          # Country: Ethiopia
    'max_retries': 3          # Maximum retry attempts for failed requests
}

# Data paths for organized file structure
DATA_PATHS = {
    'raw': 'data/raw',                    # Raw data directory
    'processed': 'data/processed',        # Processed data directory
    'raw_reviews': 'data/raw/bank_reviews_raw.csv',      # Raw reviews file
    'app_info': 'data/raw/app_info.csv'                  # App metadata file
}
DB_CONFIG = {
    "host": "localhost",
    "database": "bank_reviews",
    "user": "postgres",
    "password": "",  # Empty string
    "port": 5432
}