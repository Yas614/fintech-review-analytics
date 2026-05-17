import pytest
import pandas as pd
from datetime import datetime
from src.data_preprocessing import clean_reviews_dataframe

def test_clean_reviews_dataframe_removes_duplicates():
    mock_raw_data = [
        {'review_id': '101', 'review': 'Excellent App', 'rating': 5, 'date': datetime(2026, 5, 1), 'bank': 'CBE', 'source': 'Google Play'},
        {'review_id': '101', 'review': 'Excellent App', 'rating': 5, 'date': datetime(2026, 5, 1), 'bank': 'CBE', 'source': 'Google Play'},
    ]
    cleaned_df = clean_reviews_dataframe(mock_raw_data)
    assert len(cleaned_df) == 1

def test_clean_reviews_dataframe_drops_missing_fields():
    mock_raw_data = [
        {'review_id': '102', 'review': None, 'rating': 4, 'date': datetime(2026, 5, 2), 'bank': 'BOA', 'source': 'Google Play'},
        {'review_id': '103', 'review': 'Solid layout', 'rating': 4, 'date': datetime(2026, 5, 4), 'bank': 'BOA', 'source': 'Google Play'}
    ]
    cleaned_df = clean_reviews_dataframe(mock_raw_data)
    assert len(cleaned_df) == 1