import requests
from bs4 import BeautifulSoup
import json
import logging
import csv
import os
import schedule
import time
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt

# NLTK Sentiment Analyzer (VADER)
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure that required NLTK data is available
nltk.download('vader_lexicon')

# Load configuration
with open("config.json") as f:
    config = json.load(f)

NEWS_SOURCES = config["news_sources"]
EMAIL_CONFIG = config["email"]
CSV_FILE = config.get("csv_file", "headlines.csv")
PLOT_FOLDER = config.get("plot_folder", "plots")
ALERT_SENTIMENT_THRESHOLD = config.get("alert_sentiment_threshold", -0.5)

# Logging setup
logging.basicConfig(filename="news_aggregator.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def send_email_alert(subject, body):
    """Send an alert email if sentiment threshold is breached."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_CONFIG["sender"]
        msg["To"] = EMAIL_CONFIG["receiver"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["port"], context=context) as server:
            server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
            server.sendmail(EMAIL_CONFIG["sender"], EMAIL_CONFIG["receiver"], msg.as_string())
        logging.info("Alert email sent.")
    except Exception as e:
        logging.error(f"Error sending email alert: {e}")

def fetch_headlines():
    """Scrapes headlines from configured news sources."""
    headlines = []
    for source in NEWS_SOURCES:
        try:
            response = requests.get(source["url"], timeout=10)
            if response.status_code != 200:
                logging.warning(f"Failed to retrieve data from {source['name']}: HTTP {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            # Use a CSS selector provided in the config for each source
            elements = soup.select(source["headline_selector"])
            for element in elements:
                headline_text = element.get_text(strip=True)
                headlines.append({
                    "source": source["name"],
                    "headline": headline_text
                })
            logging.info(f"Fetched {len(elements)} headlines from {source['name']}")
        except Exception as e:
            logging.error(f"Error fetching data from {source['name']}: {e}")
    return headlines

def analyze_headline(headline):
    """Analyze the sentiment of a headline using VADER."""
    sentiment_score = sia.polarity_scores(headline)["compound"]
    return sentiment_score

def log_headlines(data):
    """Append headlines and their sentiment scores to a CSV file."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Source", "Headline", "Sentiment Score"])
        for item in data:
            writer.writerow([item["timestamp"], item["source"], item["headline"], item["sentiment"]])

def create_sentiment_plot():
    """Read CSV data, aggregate sentiment, and create a time series plot."""
    timestamps = []
    sentiment_scores = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamps.append(datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S"))
                sentiment_scores.append(float(row["Sentiment Score"]))
        if timestamps and sentiment_scores:
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, sentiment_scores, marker="o", linestyle="-")
            plt.title("Sentiment Trend Over Time")
            plt.xlabel("Time")
            plt.ylabel("Sentiment Score")
            plt.grid(True)
            os.makedirs(PLOT_FOLDER, exist_ok=True)
            plot_path = os.path.join(PLOT_FOLDER, "sentiment_trend.png")
            plt.savefig(plot_path)
            plt.close()
            logging.info(f"Sentiment plot saved to {plot_path}")
    except Exception as e:
        logging.error(f"Error creating sentiment plot: {e}")

def process_news():
    """Fetch headlines, analyze sentiment, log data, and check for alerts."""
    headlines = fetch_headlines()
    if not headlines:
        logging.warning("No headlines fetched in this cycle.")
        return

    processed_data = []
    overall_sentiment = 0.0

    for item in headlines:
        sentiment = analyze_headline(item["headline"])
        overall_sentiment += sentiment
        processed_data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": item["source"],
            "headline": item["headline"],
            "sentiment": sentiment
        })

    # Average sentiment (if headlines exist)
    avg_sentiment = overall_sentiment / len(processed_data)
    logging.info(f"Average sentiment score: {avg_sentiment:.3f}")

    log_headlines(processed_data)
    create_sentiment_plot()

    # Send alert if average sentiment is below threshold
    if avg_sentiment < ALERT_SENTIMENT_THRESHOLD:
        subject = "Alert: Negative News Sentiment Detected!"
        body = f"Average sentiment score is {avg_sentiment:.3f}. Immediate attention may be required."
        send_email_alert(subject, body)

def job():
    """Job function to be scheduled."""
    logging.info("Starting news aggregation and sentiment analysis cycle.")
    process_news()

# Schedule the news processing every 30 minutes (adjustable as needed)
schedule.every(30).minutes.do(job)

if __name__ == "__main__":
    logging.info("Starting News Aggregator & Sentiment Analyzer...")
    job()  # Initial run
    while True:
        schedule.run_pending()
        time.sleep(1)
