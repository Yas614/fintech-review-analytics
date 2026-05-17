# Fintech Review Analytics – Interim Submission

## Overview

This project analyzes Google Play Store reviews from Ethiopian mobile banking applications to uncover customer sentiment, recurring issues, and feature requests.

The banks included in this analysis are:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The project is being developed as part of the Omega Consultancy fintech analytics challenge.

---

# Task 1 Progress

## Data Collection

Reviews were scraped from the Google Play Store using the `google-play-scraper` Python library.

### Data Collected
- Review text
- Rating (1–5)
- Review date
- Bank/app name
- Source

### Current Status
- Review collection completed for all three banks
- Target: minimum 400 reviews per bank
- Data stored in CSV format

---

## Data Preprocessing

The following preprocessing steps were completed:

- Removed duplicate reviews
- Dropped rows with missing review text or ratings
- Standardized date format to YYYY-MM-DD
- Renamed columns into analysis-ready format

Final cleaned dataset columns:
- review
- rating
- date
- bank
- source

---

# Task 2 Progress

## Early Sentiment Analysis

Initial sentiment analysis has started using NLP techniques to classify reviews into:
- Positive
- Negative
- Neutral

Preliminary findings suggest that:
- Positive reviews are commonly associated with ease of use and convenience
- Negative reviews frequently mention login problems, slow transactions, and OTP issues

---

# Preliminary Insights

### Common Positive Themes
- Easy transfers
- Convenient mobile access
- Improved user interface

### Common Negative Themes
- Login failures
- Slow loading during transfers
- OTP delays
- App crashes

---

# Tools & Technologies

- Python
- pandas
- google-play-scraper
- scikit-learn
- spaCy
- transformers
- matplotlib
- PostgreSQL
- Git & GitHub

---

# Repository Structure

```text
fintech-review-analytics/
├── data/
├── notebooks/
├── src/
├── scripts/
├── tests/
├── requirements.txt
└── README.md