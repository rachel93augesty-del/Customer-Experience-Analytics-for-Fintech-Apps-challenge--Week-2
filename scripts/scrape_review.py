# scripts/scrape_reviews.py
"""
Google Play Store Review Scraper
Task 1: Data Collection

This script scrapes user reviews from Google Play Store for three Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA) 
- Dashen Bank

Target: 400+ reviews per bank (1200 total minimum)
"""

import sys
import os
import pandas as pd
from datetime import datetime
import time
from tqdm import tqdm
from google_play_scraper import app, Sort, reviews

# Configuration - Same as your instructor's pattern but for our banks
APP_IDS = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking', 
    'DASHEN': 'com.dashen.dashensuperapp'
}

BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'DASHEN': 'Dashen Bank'
}

SCRAPING_CONFIG = {
    'reviews_per_bank': 400,
    'lang': 'en',
    'country': 'et',
    'max_retries': 3
}

# UPDATED PATHS TO MATCH YOUR EXACT DIRECTORY STRUCTURE
DATA_PATHS = {
    'raw': 'D:/Personal/KAIM-10 Academy/Week 2/Project Work/Customer_Exp_Analytics_Fintech Apps/data/raw',
    'processed': 'D:/Personal/KAIM-10 Academy/Week 2/Project Work/Customer_Exp_Analytics_Fintech Apps/data/processed',
    'raw_reviews': 'D:/Personal/KAIM-10 Academy/Week 2/Project Work/Customer_Exp_Analytics_Fintech Apps/data/raw/bank_reviews_raw.csv',
    'app_info': 'D:/Personal/KAIM-10 Academy/Week 2/Project Work/Customer_Exp_Analytics_Fintech Apps/data/raw/app_info.csv'
}


class PlayStoreScraper:
    """Scraper class for Google Play Store reviews for Ethiopian banks"""

    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.reviews_per_bank = SCRAPING_CONFIG['reviews_per_bank']
        self.lang = SCRAPING_CONFIG['lang']
        self.country = SCRAPING_CONFIG['country']
        self.max_retries = SCRAPING_CONFIG['max_retries']

    def get_app_info(self, app_id):
        """Get basic information about the app"""
        try:
            result = app(app_id, lang=self.lang, country=self.country)
            return {
                'app_id': app_id,
                'title': result.get('title', 'N/A'),
                'score': result.get('score', 0),
                'ratings': result.get('ratings', 0),
                'reviews': result.get('reviews', 0),
                'installs': result.get('installs', 'N/A'),
                'updated': result.get('updated', None),
                'version': result.get('version', 'N/A')
            }
        except Exception as e:
            print(f"Error getting app info for {app_id}: {str(e)}")
            return None

    def scrape_reviews(self, app_id, count=400):
        """Scrape reviews for a specific app with retry mechanism"""
        print(f"\nScraping reviews for {app_id}...")

        for attempt in range(self.max_retries):
            try:
                result, continuation_token = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=min(count, 100),
                    filter_score_with=None
                )

                reviews_collected = result
                
                while len(reviews_collected) < count and continuation_token:
                    print(f"  Fetching more... Current: {len(reviews_collected)}")
                    
                    additional_reviews, continuation_token = reviews(
                        app_id,
                        continuation_token=continuation_token,
                        count=min(100, count - len(reviews_collected))
                    )
                    
                    if not additional_reviews:
                        break
                        
                    reviews_collected.extend(additional_reviews)
                    time.sleep(1)

                print(f"Successfully scraped {len(reviews_collected)} reviews")
                return reviews_collected

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Failed to scrape reviews after {self.max_retries} attempts")
                    return []

        return []

    def process_reviews(self, reviews_data, bank_code):
        """Process raw review data into clean dictionary format"""
        processed = []

        for review in reviews_data:
            review_date = review.get('at')
            if review_date:
                if isinstance(review_date, datetime):
                    review_date = review_date.strftime('%Y-%m-%d')
                else:
                    review_date = str(review_date)
            else:
                review_date = datetime.now().strftime('%Y-%m-%d')

            processed.append({
                'review_id': review.get('reviewId', ''),
                'review_text': review.get('content', ''),
                'rating': review.get('score', 0),
                'review_date': review_date,
                'user_name': review.get('userName', 'Anonymous'),
                'thumbs_up': review.get('thumbsUpCount', 0),
                'reply_content': review.get('replyContent', ''),
                'reply_date': review.get('repliedAt', ''),
                'bank_code': bank_code,
                'bank_name': self.bank_names[bank_code],
                'app_version': review.get('reviewCreatedVersion', 'N/A'),
                'source': 'Google Play'
            })

        return processed

    def scrape_all_banks(self):
        """Main orchestration method"""
        all_reviews = []
        app_info_list = []

        print("=" * 60)
        print("Google Play Store Review Scraper - Ethiopian Banks")
        print("=" * 60)

        # Phase 1: Fetch App Info
        print("\n[1/3] Fetching app information...")
        for bank_code, app_id in self.app_ids.items():
            print(f"\n📱 {bank_code}: {self.bank_names[bank_code]}")
            print(f"   Package: {app_id}")

            info = self.get_app_info(app_id)
            if info:
                info['bank_code'] = bank_code
                info['bank_name'] = self.bank_names[bank_code]
                app_info_list.append(info)
                print(f"   ⭐ Current Rating: {info['score']} / 5")
                print(f"   📊 Total Ratings: {info['ratings']:,}")
                print(f"   💬 Total Reviews: {info['reviews']:,}")
                print(f"   📥 Installs: {info['installs']}")
            else:
                print(f"   ❌ Failed to fetch app info")

        # Save app info
        if app_info_list:
            app_info_df = pd.DataFrame(app_info_list)
            os.makedirs(DATA_PATHS['raw'], exist_ok=True)
            app_info_df.to_csv(DATA_PATHS['app_info'], index=False)
            print(f"\n✅ App information saved to {DATA_PATHS['app_info']}")

        # Phase 2: Scrape Reviews
        print("\n[2/3] Scraping reviews...")
        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Banks"):
            reviews_data = self.scrape_reviews(app_id, self.reviews_per_bank)

            if reviews_data:
                processed = self.process_reviews(reviews_data, bank_code)
                all_reviews.extend(processed)
                print(f"✅ Collected {len(processed)} reviews for {self.bank_names[bank_code]}")
                
                # Save individual bank data
                bank_df = pd.DataFrame(processed)
                bank_file = f"{DATA_PATHS['raw']}/{bank_code.lower()}_reviews_raw.csv"
                bank_df.to_csv(bank_file, index=False)
                print(f"   💾 Saved to: {bank_file}")
            else:
                print(f"⚠️  WARNING: No reviews collected for {self.bank_names[bank_code]}")

            time.sleep(3)

        # Phase 3: Save Combined Data
        print("\n[3/3] Saving combined data...")
        if all_reviews:
            df = pd.DataFrame(all_reviews)
            os.makedirs(DATA_PATHS['raw'], exist_ok=True)
            df.to_csv(DATA_PATHS['raw_reviews'], index=False)

            print("\n" + "=" * 60)
            print("🎉 SCRAPING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"\n📈 TOTAL REVIEWS COLLECTED: {len(df):,}")
            
            # Print stats
            print(f"\n📊 REVIEWS PER BANK:")
            for bank_code in self.bank_names.keys():
                count = len(df[df['bank_code'] == bank_code])
                bank_name = self.bank_names[bank_code]
                percentage = (count / len(df)) * 100
                print(f"   {bank_code}: {count:>3} reviews ({percentage:.1f}%) - {bank_name}")

            # Rating distribution
            print(f"\n⭐ RATING DISTRIBUTION:")
            rating_counts = df['rating'].value_counts().sort_index()
            for rating, count in rating_counts.items():
                stars = '⭐' * rating
                percentage = (count / len(df)) * 100
                print(f"   {rating} stars {stars:<5}: {count:>3} reviews ({percentage:.1f}%)")

            print(f"\n💾 DATA SAVED TO:")
            print(f"   Raw Reviews: {DATA_PATHS['raw_reviews']}")
            print(f"   App Info: {DATA_PATHS['app_info']}")

            return df
        else:
            print("\n❌ ERROR: No reviews were collected!")
            return pd.DataFrame()

    def display_sample_reviews(self, df, n=3):
        """Display sample reviews from each bank"""
        print("\n" + "=" * 60)
        print("SAMPLE REVIEWS - Data Quality Check")
        print("=" * 60)

        for bank_code in self.bank_names.keys():
            bank_df = df[df['bank_code'] == bank_code]
            if not bank_df.empty:
                print(f"\n🏦 {self.bank_names[bank_code]} ({bank_code}):")
                print("-" * 50)
                samples = bank_df.head(n)
                for idx, row in samples.iterrows():
                    stars = '⭐' * int(row['rating'])
                    print(f"\n{stars} (Rating: {row['rating']}/5)")
                    review_text = row['review_text']
                    if len(review_text) > 150:
                        review_text = review_text[:150] + "..."
                    print(f"   Review: {review_text}")
                    print(f"   Date: {row['review_date']}")
                    print(f"   Likes: {row['thumbs_up']}")
                    
        print("\n" + "=" * 60)


def main():
    """Main execution function"""
    
    print("Initializing Ethiopian Bank Reviews Scraper...")
    
    scraper = PlayStoreScraper()
    df = scraper.scrape_all_banks()

    if not df.empty:
        scraper.display_sample_reviews(df)
        
        # Data quality check
        total_reviews = len(df)
        target_reviews = len(APP_IDS) * SCRAPING_CONFIG['reviews_per_bank']
        
        print(f"\n📋 DATA QUALITY SUMMARY:")
        print(f"   Target: {target_reviews} reviews (400 per bank)")
        print(f"   Actual: {total_reviews} reviews collected")
        print(f"   Completion: {(total_reviews/target_reviews)*100:.1f}%")
        
        if total_reviews >= 1200:
            print("   ✅ SUCCESS: Minimum target of 1200 reviews achieved!")
        else:
            print("   ⚠️  WARNING: Below minimum target of 1200 reviews")

    return df


if __name__ == "__main__":
    reviews_df = main()