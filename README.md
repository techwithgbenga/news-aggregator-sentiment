# News Aggregator & Sentiment Analyzer

This project fetches news headlines from multiple sources, analyzes their sentiment using NLTK's VADER, logs the data, and sends email alerts if the overall sentiment drops below a specified threshold. It also generates a visual sentiment trend chart.

---

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
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Configure the Application:
Edit config.json to add your news sources, email credentials, and customize settings.
Note: Replace the example URLs and CSS selectors with real news websites and appropriate selectors. Also, secure your email credentials and consider using environment variables or a secrets manager in a production environment.
  
5. Run the Application:
```bash
python news_aggregator.py
```
---

## Future Improvements
- Add support for more dynamic scraping methods (handling JavaScript-loaded content).
- Implement a web dashboard to display real-time sentiment trends.
- Integrate additional notification channels (SMS, Slack).
- Pull requests and suggestions are welcome!

---

## Summary

This comprehensive project provides a powerful tool for aggregating news headlines, analyzing their sentiment, logging data, creating visual reports, and sending alerts when negative news sentiment is detected. It is built with extensibility in mind—making it perfect as an open-source contribution on GitHub for anyone interested in news analytics and data-driven insights.

Would you like to add any additional functionalities to this project (such as support for RSS feeds, more sophisticated natural language processing, or a web dashboard)?
