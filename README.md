# News Aggregator & Sentiment Analyzer

This project fetches news headlines from multiple sources, analyzes their sentiment using NLTK's VADER, logs the data, and sends email alerts if the overall sentiment drops below a specified threshold. It also generates a visual sentiment trend chart.

## Features

- **Headline Scraping:** Pulls headlines from configurable news sites using BeautifulSoup.
- **Sentiment Analysis:** Uses NLTK's VADER to score each headline.
- **Data Logging:** Saves headlines and sentiment scores in a CSV file.
- **Alerting:** Sends email notifications when negative sentiment is detected.
- **Visualization:** Creates a plot of sentiment trends over time.
- **Scheduling:** Runs the process at regular intervals (default every 30 minutes).

## Setup

1. **Clone the repository:**
```bash
   git clone https://github.com/techwithgbenga/news-aggregator-sentiment.git
   cd news-aggregator-sentiment
```
