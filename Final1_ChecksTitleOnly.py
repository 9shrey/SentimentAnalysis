from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def search_articles(influencer_name, api_key, custom_search_engine_id, num_results=50):
    service = build("customsearch", "v1", developerKey=api_key)

    article_data = []
    start_index = 1

    while len(article_data) < num_results:
        query = f"{influencer_name} articles"
        res = service.cse().list(q=query, cx=custom_search_engine_id, start=start_index).execute()

        if 'items' in res:
            for item in res['items']:
                article_data.append({'title': item['title'], 'link': item['link']})
                if len(article_data) >= num_results:
                    break

            start_index = res.get('queries', {}).get('nextPage', [])[0].get('startIndex', 1) + len(res['items'])
        else:
            print("No more articles found")
            break

    return article_data


def perform_sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores['compound']

    if compound_score > 0.05:
        return 'Positive'
    elif compound_score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'


# Take user input for influencer's name
influencer_name = input("Enter the influencer's name: ")

api_key = "AIzaSyCQWRvcTEE8OMnFvWL9mBr0HQmAx_CLJsQ"
custom_search_engine_id = "a5fb11949ff8c4865"

article_data = search_articles(influencer_name, api_key, custom_search_engine_id)

if article_data:
    article_sentiments = []
    for article in article_data:
        title = article['title']
        link = article['link']
        sentiment = perform_sentiment_analysis(title)
        article_sentiments.append(sentiment)
        print(f"Article Title: {title}")
        print(f"Article Sentiment: {sentiment}")
        print(f"Article Link: {link}")
        print("-" * 50)

    # Calculate the mean sentiment
    sentiments_count = {
        'Positive': article_sentiments.count('Positive'),
        'Neutral': article_sentiments.count('Neutral'),
        'Negative': article_sentiments.count('Negative')
    }

    if sentiments_count['Positive'] > sentiments_count['Negative']:
        print("\nOverall Sentiment: Positive")
    elif sentiments_count['Negative'] > sentiments_count['Positive']:
        print("\nOverall Sentiment: Negative")
    else:
        print("\nOverall Sentiment: Neutral")
else:
    print("No articles found")
