# scripts/setup_database.py
import os
import pandas as pd
import sqlite3
import psycopg2

DB_HOST = "localhost"
DB_NAME = "fintech_reviews"
DB_USER = "postgres"
DB_PASS = "postgres" 

def create_schema_and_ingest(conn, is_sqlite=False):
    """Executes identical relational schema generation on the active connection."""
    cur = conn.cursor()
    param = "?" if is_sqlite else "%s"
    
    # 1. Banks Dimension Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_banks (
            bank_id INTEGER PRIMARY KEY AUTOINCREMENT if is_sqlite else SERIAL PRIMARY KEY,
            bank_name VARCHAR(50) UNIQUE NOT NULL
        );
    """.replace("INTEGER PRIMARY KEY AUTOINCREMENT if is_sqlite else SERIAL PRIMARY KEY", 
                "INTEGER PRIMARY KEY AUTOINCREMENT" if is_sqlite else "SERIAL PRIMARY KEY"))
    
    # 2. Reviews Fact Table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS fact_reviews (
            review_id VARCHAR(100) PRIMARY KEY,
            review_text TEXT,
            rating INT,
            review_date DATE,
            sentiment_label VARCHAR(20),
            source VARCHAR(50),
            bank_id INT REFERENCES dim_banks(bank_id)
        );
    """)
    
    df = pd.read_csv("data/processed/analyzed_reviews.csv")
    
    # Populate Dimension Table
    for bank in df['bank'].unique():
        if is_sqlite:
            cur.execute("INSERT OR IGNORE INTO dim_banks (bank_name) VALUES (?);", (bank,))
        else:
            cur.execute("INSERT INTO dim_banks (bank_name) VALUES (%s) ON CONFLICT (bank_name) DO NOTHING;", (bank,))
            
    # Map Names to IDs
    cur.execute("SELECT bank_id, bank_name FROM dim_banks;")
    bank_map = {name: b_id for b_id, name in cur.fetchall()}
    
    # Populate Fact Table
    print(f"Ingesting structured records into relational engine (Fallback mode: {is_sqlite})...")
    for _, row in df.iterrows():
        try:
            cur.execute(f"""
                INSERT {'OR IGNORE' if is_sqlite else ''} INTO fact_reviews 
                (review_id, review_text, rating, review_date, sentiment_label, source, bank_id)
                VALUES ({param}, {param}, {param}, {param}, {param}, {param}, {param})
                {'ON CONFLICT (review_id) DO NOTHING' if not is_sqlite else ''};
            """, (
                row['review_id'], row['review'], int(row['rating']), 
                row['date'], row['sentiment_label'], row['source'], bank_map[row['bank']]
            ))
        except Exception as e:
            continue
            
    conn.commit()
    cur.close()
    print("Database processing execution succeeded!")

def main():
    input_file = "data/processed/analyzed_reviews.csv"
    if not os.path.exists(input_file):
        print(f"Error: Missing {input_file}. Run analyze_sentiment.py first.")
        return

    try:
        # Try local PostgreSQL production connection first
        print("Attempting connection to local PostgreSQL cluster instance...")
        conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database="postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {DB_NAME}")
        cur.close()
        conn.close()
        
        target_conn = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        create_schema_and_ingest(target_conn, is_sqlite=False)
        target_conn.close()
        
    except Exception as pg_error:
        # Fallback to local file-based relational system instantly if service is missing
        print(f"\n[Notice] PostgreSQL service offline. Bootstrapping SQLite file fallback layer...")
        sqlite_path = "data/processed/fintech_reviews.db"
        sqlite_conn = sqlite3.connect(sqlite_path)
        create_schema_and_ingest(sqlite_conn, is_sqlite=True)
        sqlite_conn.close()
        print(f"Relational metrics cleanly mirrored to: {sqlite_path}")

if __name__ == "__main__":
    main()