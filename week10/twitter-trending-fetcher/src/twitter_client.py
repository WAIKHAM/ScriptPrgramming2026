import requests
from typing import Optional, List, Dict, Any
from config.config import TwitterConfig

class TwitterClient:
    def __init__(self):
        self.bearer_token = TwitterConfig.BEARER_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
    
    def make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to Twitter API with error handling
        
        Args:
            url (str): API endpoint URL
            params (Dict, optional): Query parameters
            
        Returns:
            Dict: JSON response or None if error occurs
        """
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=15
            )
            
            # Check if request was successful
            if not response.ok:
                print(f"Twitter API request failed with status code: {response.status_code}")
                print(f"Error message: {response.text}")
                return None
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            return None
    
    def get_trending_hashtags(self, woeid: int = TwitterConfig.DEFAULT_WOEID,
                             limit: int = TwitterConfig.DEFAULT_LIMIT) -> Optional[List[Dict]]:
        """
        Get trending hashtags for a specific location
        
        Args:
            woeid (int): Where On Earth ID for location (1 = global)
            limit (int): Maximum number of trends to return
            
        Returns:
            List[Dict]: List of trending hashtags or None if error occurs
        """
        params = {
            "id": woeid
        }
        
        data = self.make_request(TwitterConfig.TRENDS_URL, params)
        
        if not data or not isinstance(data, list) or len(data) == 0:
            return None
            
        trends = data[0].get('trends', [])
        
        # Filter for hashtags only and apply limit
        hashtags = [trend for trend in trends if trend.get('name', '').startswith('#')]
        
        if limit and limit > 0:
            hashtags = hashtags[:limit]
            
        return hashtags
    
    def get_tweets_by_hashtag(self, hashtag: str, limit: int = 5) -> Optional[List[Dict]]:
        """
        Get recent tweets for a specific hashtag
        
        Args:
            hashtag (str): Hashtag to search for (with or without #)
            limit (int): Maximum number of tweets to return
            
        Returns:
            List[Dict]: List of tweets or None if error occurs
        """
        # Ensure hashtag starts with #
        if not hashtag.startswith('#'):
            hashtag = f"#{hashtag}"
            
        # Remove # for query
        query = hashtag.replace('#', '')
        
        params = {
            "query": f"#{query} -is:retweet",  # Exclude retweets
            "max_results": min(limit, 10),  # API limit is 10 for basic access
            "tweet.fields": "created_at,public_metrics,author_id",
            "expansions": "author_id",
            "user.fields": "name,username"
        }
        
        data = self.make_request(TwitterConfig.SEARCH_URL, params)
        
        if not data:
            return None
            
        tweets = data.get('data', [])
        users = {user['id']: user for user in data.get('includes', {}).get('users', [])}
        
        # Enrich tweets with user information
        for tweet in tweets:
            author_id = tweet.get('author_id')
            if author_id and author_id in users:
                tweet['author'] = users[author_id]
                
        return tweets
    
    def get_available_trend_locations(self) -> Optional[List[Dict]]:
        """
        Get available trend locations (WOEIDs)
        
        Returns:
            List[Dict]: List of available locations or None if error occurs
        """
        url = "https://api.twitter.com/1.1/trends/available.json"
        return self.make_request(url)