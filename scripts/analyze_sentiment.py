import os
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns

def run_interim_analysis():
    input_file = "data/raw/cleaned_reviews.csv"
    if not os.path.exists(input_file):
        print(f"Error: Missing {input_file}. Please execute scrape_reviews.py first.")
        return

    print("Loading cleaned dataset...")
    df = pd.read_csv(input_file)
    
    print("Initialising fine-tuned DistilBERT transformer instance...")
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    review_strings = df['review'].fillna("").astype(str).tolist()
    labels, scores = [], []
    
    print("Analyzing text blocks in batch sequences...")
    batch_size = 32
    for i in range(0, len(review_strings), batch_size):
        chunk = review_strings[i:i+batch_size]
        predictions = classifier(chunk)
        for pred in predictions:
            labels.append(pred['label'])
            scores.append(pred['score'])
            
    df['sentiment_label'] = labels
    df['sentiment_score'] = scores
    
    # Generate the interim milestone graphic
    print("Plotting sentiment distributions across the client portfolio...")
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    sns.countplot(data=df, x='bank', hue='sentiment_label', palette='viridis')
    
    plt.title("Comparative Sentiment Matrix: Ethiopian FinTech Apps", fontsize=14, pad=15)
    plt.xlabel("Target Financial Institution", fontsize=11)
    plt.ylabel("Extracted Review Record Count", fontsize=11)
    plt.legend(title="Sentiment Class")
    
    plt.tight_layout()
    plt.savefig("interim_sentiment_matrix.png", dpi=300)
    print("Task 2 complete. Visualization exported as 'interim_sentiment_matrix.png'.")

if __name__ == "__main__":
    run_interim_analysis()