import sys
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Function to retrieve article content from a given link and perform sentiment analysis
def get_sentiment_for_article(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_text = soup.find('div', class_='article-content').get_text()  # Extract article text
        sentiment_scores = perform_sentiment_analysis(article_text)
        return interpret_sentiment(sentiment_scores)
    else:
        print(f"Failed to fetch content from {article_url}")
        return None

# Perform sentiment analysis on article content
def perform_sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores

# Interpret sentiment scores
def interpret_sentiment(sentiment_scores):
    compound_score = sentiment_scores['compound']
    if compound_score > 0.05:
        return 'Positive'
    elif compound_score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sentiment_analysis_script.py <article_link>")
    else:
        article_link = sys.argv[1]
        sentiment = get_sentiment_for_article(article_link)
        print(sentiment)
