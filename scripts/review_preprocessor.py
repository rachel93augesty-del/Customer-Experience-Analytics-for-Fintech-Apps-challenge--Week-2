# scripts/review_preprocessor.py
"""
Data Preprocessing Script
Task 1: Data Preprocessing

This script cleans and preprocesses the scraped reviews data for Ethiopian banks:
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA) 
- Dashen Bank

REQUIRED COLUMNS (from instructor): review, rating, date, bank, source
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import re

# Add parent directory to path to allow importing modules from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import DATA_PATHS dictionary from the local config module
from config import DATA_PATHS


class ReviewPreprocessor:
    """Preprocessor class for Ethiopian bank review data"""

    def __init__(self, input_path=None, output_path=None):
        """
        Initialize preprocessor

        Args:
            input_path (str): Path to raw reviews CSV
            output_path (str): Path to save processed reviews
        """
        # Use your existing DATA_PATHS structure - FIXED
        self.input_path = input_path or DATA_PATHS['raw_reviews']
        
        # FIXED: Construct output path properly using your config
        if output_path:
            self.output_path = output_path
        else:
            # Use the 'processed' directory from your config and add the filename
            processed_dir = DATA_PATHS['processed']
            self.output_path = os.path.join(processed_dir, 'bank_reviews_cleaned.csv')
        
        # Initialize an empty DataFrame attribute to hold our data
        self.df = None
        # Initialize a dictionary to keep track of processing statistics (counts, errors, etc.)
        self.stats = {}

    def load_data(self):
        """Load raw reviews data"""
        # Print a message indicating that data loading has started
        print("Loading raw data...")
        try:
            # Read the CSV file at self.input_path into a pandas DataFrame
            self.df = pd.read_csv(self.input_path)
            # Print the number of records loaded
            print(f"Loaded {len(self.df)} reviews")
            # Record the initial number of records in our stats dictionary
            self.stats['original_count'] = len(self.df)
            # Return True to indicate success
            return True
        except FileNotFoundError:
            # Handle the specific error where the file does not exist
            print(f"ERROR: File not found: {self.input_path}")
            return False
        except Exception as e:
            # Handle any other general errors that occur during loading
            print(f"ERROR: Failed to load data: {str(e)}")
            return False

    def check_missing_data(self):
        """Check for missing data"""
        # Print a header for this step [1/6]
        print("\n[1/6] Checking for missing data...")

        # Calculate the count of missing (null) values for each column
        missing = self.df.isnull().sum()
        # Calculate the percentage of missing values for each column
        missing_pct = (missing / len(self.df)) * 100

        # Print the section header
        print("\nMissing values:")
        # Loop through each column name in the index of the 'missing' series
        for col in missing.index:
            # If the column has at least one missing value
            if missing[col] > 0:
                # Print the column name, count of missing values, and percentage
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.2f}%)")

        # Store the dictionary of missing counts in our stats for reporting later
        self.stats['missing_before'] = missing.to_dict()

        # Define a list of columns that are absolutely required for our analysis
        critical_cols = ['review_text', 'rating', 'bank_name']
        # Calculate missing values just for these critical columns
        missing_critical = self.df[critical_cols].isnull().sum()

        # If there are any missing values in critical columns
        if missing_critical.sum() > 0:
            # Print a warning message
            print("\nWARNING: Missing values in critical columns:")
            # Print the counts of missing values for the critical columns that have them
            print(missing_critical[missing_critical > 0])

    def handle_missing_values(self):
        """Handle missing values"""
        # Print a header for this step [2/6]
        print("\n[2/6] Handling missing values...")

        # Define the critical columns again
        critical_cols = ['review_text', 'rating', 'bank_name']
        # Store the count before dropping rows
        before_count = len(self.df)
        # Drop any rows that have missing values (NaN) in the critical columns
        self.df = self.df.dropna(subset=critical_cols)
        # Calculate how many rows were removed
        removed = before_count - len(self.df)

        # If any rows were removed, print a message
        if removed > 0:
            print(f"Removed {removed} rows with missing critical values")

        # For the 'user_name' column, fill missing values with the string 'Anonymous'
        self.df['user_name'] = self.df['user_name'].fillna('Anonymous')
        # For the 'thumbs_up' column, fill missing values with 0
        self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)
        # For the 'reply_content' column, fill missing values with an empty string
        self.df['reply_content'] = self.df['reply_content'].fillna('')
        # For the 'app_version' column, fill missing values with 'Unknown'
        self.df['app_version'] = self.df['app_version'].fillna('Unknown')

        # Record the number of rows removed due to missing critical data
        self.stats['rows_removed_missing'] = removed
        # Record the new total count in stats
        self.stats['count_after_missing'] = len(self.df)

    def normalize_dates(self):
        """Normalize date formats to YYYY-MM-DD"""
        # Print a header for this step [3/6]
        print("\n[3/6] Normalizing dates...")

        try:
            # Convert the 'review_date' column to pandas datetime objects
            # This handles various string formats automatically
            self.df['review_date'] = pd.to_datetime(self.df['review_date'], errors='coerce')

            # Convert the datetime objects to just date objects (YYYY-MM-DD), removing time info
            self.df['review_date'] = self.df['review_date'].dt.date

            # Extract the year from the date and create a new 'review_year' column
            self.df['review_year'] = pd.to_datetime(self.df['review_date']).dt.year
            # Extract the month from the date and create a new 'review_month' column
            self.df['review_month'] = pd.to_datetime(self.df['review_date']).dt.month

            # Print the range of dates found in the data (minimum and maximum)
            print(f"Date range: {self.df['review_date'].min()} to {self.df['review_date'].max()}")

        except Exception as e:
            # Handle errors if date conversion fails
            print(f"WARNING: Error normalizing dates: {str(e)}")

    def clean_text(self):
        """Clean review text with focus on English text preparation"""
        # Print a header for this step [4/6]
        print("\n[4/6] Cleaning text...")

        def clean_review_text(text):
            """Clean individual review text strings with English focus"""
            # If the text is NaN (missing) or empty string, return empty string
            if pd.isna(text) or text == '':
                return ''

            # Convert the input to a string type (safety check)
            text = str(text)

            # Use regex to replace multiple whitespace characters (spaces, tabs, newlines) with a single space
            text = re.sub(r'\s+', ' ', text)

            # Remove leading and trailing whitespace from the string
            text = text.strip()

            # Return the cleaned text
            return text

        # Apply the 'clean_review_text' function to every element in the 'review_text' column
        self.df['review_text_clean'] = self.df['review_text'].apply(clean_review_text)

        # Store the count before removing empty reviews
        before_count = len(self.df)
        # Keep only rows where the length of 'review_text_clean' is greater than 0
        self.df = self.df[self.df['review_text_clean'].str.len() > 0]
        # Calculate how many empty reviews were removed
        removed = before_count - len(self.df)

        # If rows were removed, print a message
        if removed > 0:
            print(f"Removed {removed} reviews with empty text")

        # Create a new column 'text_length' containing the character count of the review text
        self.df['text_length'] = self.df['review_text_clean'].str.len()
        # Create a new column 'word_count' containing the word count of the review text
        self.df['word_count'] = self.df['review_text_clean'].str.split().str.len()

        # Record statistics about text cleaning
        self.stats['empty_reviews_removed'] = removed
        self.stats['count_after_cleaning'] = len(self.df)

    def validate_ratings(self):
        """Validate rating values (should be 1-5)"""
        # Print a header for this step [5/6]
        print("\n[5/6] Validating ratings...")

        # Convert to numeric and handle errors
        self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce')
        
        # Find rows where 'rating' is less than 1 OR greater than 5 OR is NaN
        invalid = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5) | (self.df['rating'].isna())]

        # If there are any invalid ratings
        if len(invalid) > 0:
            # Print a warning with the count of invalid ratings
            print(f"WARNING: Found {len(invalid)} reviews with invalid ratings")
            # Filter the DataFrame to keep only rows where rating is between 1 and 5 (inclusive)
            self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 5)]
        else:
            # If all ratings are valid, print a confirmation
            print("All ratings are valid (1-5)")

        # Record the number of invalid ratings removed
        self.stats['invalid_ratings_removed'] = len(invalid)

    def prepare_final_output(self):
        """Prepare final output format - ENSURING REQUIRED COLUMNS ARE PRESENT"""
        # Print a header for this step [6/6]
        print("\n[6/6] Preparing final output...")

        # REQUIRED COLUMNS (from instructor)
        REQUIRED_COLUMNS = {
            'review': 'review_text_clean',  # Use cleaned text for 'review'
            'rating': 'rating',             # Keep as is
            'date': 'review_date',          # Use normalized date
            'bank': 'bank_name',            # Use bank_name for 'bank'
            'source': 'source'              # Keep as is
        }

        # ADDITIONAL COLUMNS (optional but useful for analysis)
        ADDITIONAL_COLUMNS = [
            'review_id',
            'review_text',           # Original text
            'review_year',
            'review_month', 
            'bank_code',
            'user_name',
            'thumbs_up',
            'text_length',
            'word_count',
            'app_version'
        ]

        # Step 1: Ensure required columns exist and create them if needed
        print("Ensuring required columns are present...")
        
        # Create required columns mapping
        final_columns = {}
        
        for required_name, source_column in REQUIRED_COLUMNS.items():
            if source_column in self.df.columns:
                final_columns[required_name] = self.df[source_column]
                print(f"  ✅ {required_name} <- {source_column}")
            else:
                # Create placeholder if column doesn't exist
                print(f"  ⚠️  {required_name}: Creating placeholder (source {source_column} not found)")
                if required_name == 'source':
                    final_columns[required_name] = 'Google Play'  # Default value
                else:
                    final_columns[required_name] = ''  # Empty placeholder
        
        # Step 2: Add additional columns that exist in the dataframe
        for additional_col in ADDITIONAL_COLUMNS:
            if additional_col in self.df.columns:
                final_columns[additional_col] = self.df[additional_col]
                print(f"  📊 {additional_col} (additional)")

        # Step 3: Create final DataFrame with guaranteed required columns
        self.df = pd.DataFrame(final_columns)

        # Step 4: Sort the DataFrame by bank and date (newest first)
        self.df = self.df.sort_values(['bank', 'date'], ascending=[True, False])

        # Step 5: Reset index
        self.df = self.df.reset_index(drop=True)

        # Print final column verification
        print(f"\n✅ FINAL COLUMNS GUARANTEED:")
        required_present = all(col in self.df.columns for col in REQUIRED_COLUMNS.keys())
        if required_present:
            for col in REQUIRED_COLUMNS.keys():
                print(f"   {col}: ✓ PRESENT")
        else:
            missing = [col for col in REQUIRED_COLUMNS.keys() if col not in self.df.columns]
            print(f"   ❌ MISSING REQUIRED COLUMNS: {missing}")

        print(f"Final dataset: {len(self.df)} reviews with {len(self.df.columns)} columns")

    def save_data(self):
        """Save processed data"""
        # Print a message indicating saving has started
        print("\nSaving processed data...")

        try:
            # Create the directory for the output file if it doesn't already exist
            # os.path.dirname gets the folder part of the file path
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

            # Write the DataFrame to a CSV file at self.output_path
            # index=False prevents writing the row numbers (0, 1, 2...) to the file
            self.df.to_csv(self.output_path, index=False)
            # Print a confirmation message with the path
            print(f"Data saved to: {self.output_path}")

            # Record the final count in stats
            self.stats['final_count'] = len(self.df)
            # Return True to indicate success
            return True

        except Exception as e:
            # Handle any errors during saving
            print(f"ERROR: Failed to save data: {str(e)}")
            # Return False to indicate failure
            return False

    def generate_report(self):
        """Generate preprocessing report"""
        # Print a separator line
        print("\n" + "=" * 60)
        # Print the report title
        print("ETHIOPIAN BANKS - PREPROCESSING REPORT")
        # Print a separator line
        print("=" * 60)

        # Print various statistics gathered during the process using .get() to avoid errors if key is missing
        print(f"\nOriginal records: {self.stats.get('original_count', 0)}")
        print(f"Records with missing critical data: {self.stats.get('rows_removed_missing', 0)}")
        print(f"Empty reviews removed: {self.stats.get('empty_reviews_removed', 0)}")
        print(f"Invalid ratings removed: {self.stats.get('invalid_ratings_removed', 0)}")
        print(f"Final records: {self.stats.get('final_count', 0)}")

        # Calculate data quality percentage metrics
        if self.stats.get('original_count', 0) > 0:
            # Retention rate = (Final / Original) * 100
            retention_rate = (self.stats.get('final_count', 0) / self.stats.get('original_count', 1)) * 100
            # Error rate is the inverse of retention rate
            error_rate = 100 - retention_rate
            print(f"\nData retention rate: {retention_rate:.2f}%")
            print(f"Data error rate: {error_rate:.2f}%")

            # Assess quality based on error rate thresholds
            if error_rate < 5:
                print("✓ Data quality: EXCELLENT (<5% errors)")
            elif error_rate < 10:
                print("✓ Data quality: GOOD (<10% errors)")
            else:
                print("⚠ Data quality: NEEDS ATTENTION (>10% errors)")

        # Print statistics about the reviews per bank
        if self.df is not None:
            print("\n📊 REQUIRED COLUMNS VERIFICATION:")
            required_columns = ['review', 'rating', 'date', 'bank', 'source']
            for col in required_columns:
                if col in self.df.columns:
                    non_empty = self.df[col].notna().sum() if col != 'review' else (self.df[col].str.len() > 0).sum()
                    print(f"  {col}: ✓ PRESENT ({non_empty} non-empty values)")
                else:
                    print(f"  {col}: ❌ MISSING")

            print("\nReviews per bank:")
            # Count occurrences of each unique value in 'bank'
            bank_counts = self.df['bank'].value_counts()
            # Loop through the results and print them
            for bank, count in bank_counts.items():
                percentage = (count / len(self.df)) * 100
                print(f"  {bank}: {count} reviews ({percentage:.1f}%)")

            # Print statistics about rating distribution
            print("\nRating distribution:")
            # Count occurrences of each rating, and sort by rating (5 down to 1)
            rating_counts = self.df['rating'].value_counts().sort_index(ascending=False)
            for rating, count in rating_counts.items():
                # Calculate percentage for this rating
                pct = (count / len(self.df)) * 100
                # Print star representation, count, and percentage
                print(f"  {'⭐' * int(rating)}: {count} ({pct:.1f}%)")

            # Print the full date range of the data
            print(f"\nDate range: {self.df['date'].min()} to {self.df['date'].max()}")

    def process(self):
        """Run complete preprocessing pipeline"""
        # Print start header
        print("=" * 60)
        print("STARTING ETHIOPIAN BANKS DATA PREPROCESSING")
        print("=" * 60)
        print("REQUIRED COLUMNS: review, rating, date, bank, source")
        print("=" * 60)

        # Attempt to load data. If it fails, return False immediately.
        if not self.load_data():
            return False

        # Run each step of the pipeline in sequence
        self.check_missing_data()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()
        self.validate_ratings()
        self.prepare_final_output()

        # Attempt to save the data. If successful, generate the report.
        if self.save_data():
            self.generate_report()
            return True

        # If saving failed, return False
        return False


def main():
    """Main execution function"""
    # Create an instance of the ReviewPreprocessor class
    preprocessor = ReviewPreprocessor()
    # Run the processing pipeline
    success = preprocessor.process()

    # Check if the process was successful
    if success:
        print("\n✓ Data preprocessing completed successfully!")
        print("✓ REQUIRED COLUMNS GUARANTEED: review, rating, date, bank, source")
        # Return the processed DataFrame
        return preprocessor.df
    else:
        print("\n✗ Preprocessing failed!")
        # Return None to indicate failure
        return None


# Standard Python check to see if this file is being run directly (not imported)
if __name__ == "__main__":
    # If run directly, execute the main function
    processed_df = main()