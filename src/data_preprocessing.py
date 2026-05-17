import pandas as pd

def clean_reviews_dataframe(raw_data_list):
    """
    Cleans raw scraped Google Play Store data.
    - Drops duplicates on review_id
    - Enforces missing value removal on text or ratings
    - Standardizes dates to YYYY-MM-DD
    """
    if not raw_data_list:
        return pd.DataFrame(columns=['review_id', 'review', 'rating', 'date', 'bank', 'source'])
        
    df = pd.DataFrame(raw_data_list)
    
    # Drop rows missing critical fields
    df.dropna(subset=['review', 'rating'], inplace=True)
    
    # Drop duplicate reviews based on ID
    df.drop_duplicates(subset=['review_id'], inplace=True)
    
    # Standardize dates
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    return df