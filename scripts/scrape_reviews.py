import os
import sys
from google_play_scraper import Sort, reviews

# Append root directory to path to ensure clean internal src imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_preprocessing import clean_reviews_dataframe

# Production package identifiers for target Ethiopian banks
BANKS = {
    "CBE": "com.cbe.cbebirr",       
    "BOA": "com.boamobile.prod",        
    "Dashen": "com.dashen.amole"        
}

def execute_scraping_pipeline():
    print("Initializing Google Play data extraction pipeline...")
    scraped_records = []
    
    for bank_name, app_id in BANKS.items():
        try:
            print(f"Extracting review feeds for: {bank_name}")
            # Target 450 items to safely guarantee the 400 minimum KPI count per bank
            fetched_batch, _ = reviews(
                app_id,
                lang='en', 
                country='us', 
                sort=Sort.NEWEST, 
                count=450
            )
            
            for item in fetched_batch:
                scraped_records.append({
                    'review_id': item['reviewId'],
                    'review': item['content'],
                    'rating': item['score'],
                    'date': item['at'],
                    'bank': bank_name,
                    'source': 'Google Play'
                })
        except Exception as e:
            print(f"Warning: Failed to fetch data for {bank_name} due to: {e}")
            
    # Process through our src cleaning package
    cleaned_df = clean_reviews_dataframe(scraped_records)
    
    # Build exact folder output layout required by prompt
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/cleaned_reviews.csv"
    cleaned_df.to_csv(output_path, index=False)
    
    print(f"\nPipeline Success! Collected {len(cleaned_df)} entries.")
    print(f"Cleaned output structurally saved to: {output_path}")

if __name__ == "__main__":
    execute_scraping_pipeline()