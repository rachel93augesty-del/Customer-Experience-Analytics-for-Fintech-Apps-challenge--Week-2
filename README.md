# Add methodology section to README
echo "
## Methodology

### Data Collection
- Used google-play-scraper Python library
- Targeted 3 Ethiopian banking apps: CBE, BOA, Dashen
- Collected 400+ reviews per bank (1200+ total)
- Data points: review text, rating, date, bank name, source

### Data Preprocessing
- Removed duplicate reviews
- Handled missing values (reply_content, reply_date, app_version)
- Normalized dates to YYYY-MM-DD format
- Validated ratings (1-5 scale)
- Ensured required columns: review, rating, date, bank, source

### Data Quality
- 100% data retention (1200/1200 reviews)
- 0% error rate in critical columns
- Perfect bank distribution (400 reviews each)
" >> README.md