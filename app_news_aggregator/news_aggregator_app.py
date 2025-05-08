import os
from flask import Blueprint, render_template, request, jsonify
# import feedparser # Uncomment when implementing feedparser
import requests # Uncomment when implementing requests
from dotenv import load_dotenv # Uncomment when using .env

load_dotenv() # Load environment variables from .env

# Initialize a Blueprint for the news aggregator module
# The url_prefix will be set when registering with the main app
news_aggregator_bp = Blueprint('news_aggregator', __name__,
                               template_folder='templates',
                               static_folder='static')

# Note: Secret key is configured in the main app, not here for a Blueprint

# --- News Fetching and Processing (Placeholders) ---
# TODO: Implement actual news fetching from RSS and News APIs
# Use feedparser for RSS, requests for APIs (like NewsAPI.org)
# Handle API key securely (.env)
# Implement content processing and filtering (keywords, optional NLP)
# Implement caching to respect API limits

def fetch_news(sources, keywords):
    """Fetches news articles from NewsAPI.org based on keywords."""
    print(f"Compiling datastream with keywords: {keywords}")

    newsapi_key = os.getenv('NEWSAPI_KEY')
    if not newsapi_key:
        return {"status": "error", "message": "News API key not found in environment variables."}

    all_articles = []
    for keyword in keywords:
        url = f'https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={newsapi_key}'
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if data['status'] == 'ok':
                for article in data['articles']:
                    all_articles.append({
                        "title": article.get('title'),
                        "source": article.get('source', {}).get('name'),
                        "date": article.get('publishedAt'),
                        "summary": article.get('description'),
                        "link": article.get('url')
                    })
            else:
                print(f"Error fetching news for keyword '{keyword}': {data.get('message', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news for keyword '{keyword}': {e}")

    return {"status": "success", "message": "Datastream compiled.", "articles": all_articles}

# --- Routes ---
@news_aggregator_bp.route('/')
def index():
    """
    Renders the main HTML page for the news aggregator application (to be embedded in iframe).
    This route is relative to the blueprint's url_prefix ('/news_aggregator').
    """
    return render_template('news_aggregator_index.html')

@news_aggregator_bp.route('/fetch', methods=['POST'])
def fetch():
    """
    Handles request to fetch news articles.
    """
    criteria = request.get_json()
    sources = criteria.get('sources', [])
    keywords = criteria.get('keywords', [])
    # TODO: Use criteria to fetch news
    result = fetch_news(sources, keywords)
    return jsonify(result)

# This __main__ block is removed as the module will be run via the main app.