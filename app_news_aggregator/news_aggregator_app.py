import os
from flask import Blueprint, render_template, request, jsonify
# import feedparser # Uncomment when implementing feedparser
# import requests # Uncomment when implementing requests
# from dotenv import load_dotenv # Uncomment when using .env

# load_dotenv() # Load environment variables from .env

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
    """Placeholder for fetching news articles."""
    print(f"Compiling datastream from sources: {sources} with keywords: {keywords}")
    # TODO: Implement news fetching logic
    # Fetch from RSS feeds using feedparser
    # Fetch from News APIs using requests (handle API keys)
    # Combine and filter articles based on keywords/preferences
    # Implement caching

    # Mock data for now
    mock_articles = [
        {"title": "Corpo War Escalates in Heywood", "source": "NCPD Blotter", "date": "2077-08-15", "summary": "Recent clashes between Arasaka and Militech forces...", "link": "#"},
        {"title": "New Cyberware Clinic Opens in Westbrook", "source": "Night City Wire", "date": "2077-08-14", "summary": "Cutting-edge chrome available now...", "link": "#"},
        {"title": "Netrunner 'Ghost' Breaches Arasaka Network", "source": "Darknet Intel", "date": "2077-08-15", "summary": "Details on the recent high-profile breach...", "link": "#"},
    ]
    return {"status": "success", "message": "Datastream compiled.", "articles": mock_articles}

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