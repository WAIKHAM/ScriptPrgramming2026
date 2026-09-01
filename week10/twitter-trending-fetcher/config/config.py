import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TwitterConfig:
    # Twitter API v2 credentials
    BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    API_KEY = os.getenv('TWITTER_API_KEY')
    API_SECRET = os.getenv('TWITTER_API_SECRET')
    ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # API endpoints
    BASE_URL = "https://api.twitter.com/2"
    TRENDS_URL = f"{BASE_URL}/trends/place.json"
    SEARCH_URL = f"{BASE_URL}/tweets/search/recent"
    
    # Default parameters
    DEFAULT_WOEID = 1  # Worldwide trends (1 = global)
    DEFAULT_LIMIT = 10