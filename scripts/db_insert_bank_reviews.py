# scripts/db_insert_bank_reviews.py
"""
TASK 3: PostgreSQL Database Data Insertion
This script loads cleaned review data into the PostgreSQL database.
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import sys

def main():
    print("=" * 60)
    print("TASK 3: INSERTING DATA INTO POSTGRESQL DATABASE")
    print("=" * 60)
    
    # 1. Load the cleaned data
    data_path = "../data/processed/bank_reviews_cleaned.csv"
    print(f"ðŸ“‚ Loading data from: {data_path}")
    
    if not os.path.exists(data_path):
        print(f"âŒ ERROR: File not found: {data_path}")
        print("   Make sure you have run Tasks 1 and 2 first.")
        sys.exit(1)
    
    df = pd.read_csv(data_path)
    print(f"âœ… Loaded {len(df):,} reviews")
    
    # 2. Connect to PostgreSQL database
    print("\nðŸ”— Connecting to PostgreSQL database...")
    try:
        # UPDATE THESE CREDENTIALS FOR YOUR SYSTEM
        conn = psycopg2.connect(
            host="localhost",
            database="bank_reviews",
            user="postgres",          # Your PostgreSQL username
            password="postgres",      # Your PostgreSQL password (CHANGE THIS!)
            port=5432
        )
        cursor = conn.cursor()
        print("âœ… Connected to 'bank_reviews' database")
    except Exception as e:
        print(f"âŒ Database connection failed: {e}")
        print("\nðŸ’¡ TROUBLESHOOTING:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check your username/password")
        print("   3. Verify database exists: createdb bank_reviews")
        sys.exit(1)
    
    # 3. Ensure banks are inserted
    print("\nðŸ¦ Inserting bank data...")
    banks = df['bank'].unique()
    bank_ids = {}
    
    for bank_name in banks:
        cursor.execute(
            "INSERT INTO banks (bank_name) VALUES (%s) ON CONFLICT (bank_name) DO NOTHING RETURNING bank_id",
            (bank_name,)
        )
        result = cursor.fetchone()
        if result:
            bank_ids[bank_name] = result[0]
        else:
            # Bank already exists, get its ID
            cursor.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (bank_name,))
            bank_ids[bank_name] = cursor.fetchone()[0]
    
    print(f"âœ… Inserted/verified {len(bank_ids)} banks")
    
    # 4. Prepare review data for insertion
    print("\nðŸ“ Preparing review data for insertion...")
    
    # Create a list of tuples for batch insertion
    review_data = []
    for _, row in df.iterrows():
        # Determine sentiment from rating
        if row['rating'] >= 4:
            sentiment = 'POSITIVE'
            score = 0.9
        elif row['rating'] <= 2:
            sentiment = 'NEGATIVE'
            score = 0.2
        else:
            sentiment = 'NEUTRAL'
            score = 0.5
        
        review_data.append((
            row['review_id'],
            bank_ids[row['bank']],
            row['review_text'],
            row['rating'],
            row['date'],
            sentiment,
            score,
            row['source'],
            row.get('user_name', ''),
            row.get('thumbs_up', 0),
            row.get('text_length', len(str(row['review_text']))),
            row.get('word_count', len(str(row['review_text']).split())),
            row.get('app_version', 'Unknown')
        ))
    
    # 5. Batch insert reviews
    print(f"ðŸ’¾ Inserting {len(review_data):,} reviews...")
    
    insert_query = """
    INSERT INTO reviews 
    (review_id, bank_id, review_text, rating, review_date, sentiment_label, 
     sentiment_score, source, user_name, thumbs_up, text_length, word_count, app_version)
    VALUES %s
    ON CONFLICT (review_id) DO NOTHING
    """
    
    execute_values(cursor, insert_query, review_data)
    conn.commit()
    
    print("âœ… All reviews inserted successfully!")
    
    # 6. Verification queries
    print("\n" + "=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)
    
    # Total reviews
    cursor.execute("SELECT COUNT(*) FROM reviews;")
    total = cursor.fetchone()[0]
    print(f"Total reviews in database: {total:,}")
    
    # Reviews per bank
    cursor.execute("""
        SELECT b.bank_name, COUNT(r.review_id) as count, 
               AVG(r.rating) as avg_rating
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY avg_rating DESC;
    """)
    
    print("\nðŸ“Š Reviews per bank:")
    for bank, count, avg_rating in cursor.fetchall():
        print(f"   {bank}: {count:,} reviews, {avg_rating:.2f} avg rating")
    
    # Cleanup
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("âœ… TASK 3 COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nNext steps:")
    print("1. Commit these files to git:")
    print("   - scripts/schema.sql")
    print("   - scripts/db_insert_bank_reviews.py")
    print("2. Update your README.md with database instructions")
    print("3. Create/update your Task 3 pull request")

if __name__ == "__main__":
    main()

