# !/usr/bin/env python3
"""
Twitter Trending Hashtags Fetcher - Main Entry Point
Fetches trending hashtags from Twitter API and displays them with sample tweets
"""

import sys
from typing import Optional, List, Dict
from src.twitter_client import TwitterClient

def display_menu() -> None:
    """Display the main menu options"""
    print("\n" + "="*60)
    print("TWITTER TRENDING HASHTAGS FETCHER")
    print("="*60)
    print("1. Show Global Trending Hashtags")
    print("2. Show Trending Hashtags for Specific Location")
    print("3. Search Tweets by Hashtag")
    print("4. Show Available Locations")
    print("5. Exit")
    print("="*60)

def get_user_choice() -> str:
    """Get user choice from menu"""
    return input("Enter your choice (1-5): ").strip()

def get_limit() -> int:
    """Get limit from user input"""
    try:
        limit_input = input("Enter number of items to fetch (default 10): ").strip()
        return int(limit_input) if limit_input else 10
    except ValueError:
        print("Invalid number. Using default value of 10.")
        return 10

def get_woeid() -> int:
    """Get WOEID from user input"""
    try:
        woeid_input = input("Enter WOEID (1 for global): ").strip()
        return int(woeid_input) if woeid_input else 1
    except ValueError:
        print("Invalid WOEID. Using global (1).")
        return 1

def get_hashtag() -> str:
    """Get hashtag from user input"""
    hashtag = input("Enter hashtag (with or without #): ").strip()
    return hashtag if hashtag else "#twitter"

def display_trending_hashtags(hashtags: List[Dict], location: str = "Global") -> None:
    """Display trending hashtags in a user-friendly format"""
    if not hashtags:
        print("No trending hashtags found.")
        return
    
    print(f"\n{'='*80}")
    print(f"TRENDING HASHTAGS - {location.upper()}")
    print(f"{'='*80}")
    
    for i, hashtag in enumerate(hashtags, 1):
        name = hashtag.get('name', 'Unknown')
        tweet_volume = hashtag.get('tweet_volume', 0)
        url = hashtag.get('url', '')
        
        volume_str = f"{tweet_volume:,} tweets" if tweet_volume else "Trending"
        
        print(f"{i:2d}. {name}")
        print(f"    Volume: {volume_str}")
        if url:
            print(f"    URL: {url}")
        print()

def display_tweets(tweets: List[Dict], hashtag: str) -> None:
    """Display tweets in a user-friendly format"""
    if not tweets:
        print(f"No tweets found for {hashtag}.")
        return
    
    print(f"\n{'='*100}")
    print(f"RECENT TWEETS FOR {hashtag.upper()}")
    print(f"{'='*100}")
    
    for i, tweet in enumerate(tweets, 1):
        text = tweet.get('text', 'No text')
        created_at = tweet.get('created_at', 'Unknown date')
        author = tweet.get('author', {})
        author_name = author.get('name', 'Unknown')
        author_handle = author.get('username', 'unknown')
        metrics = tweet.get('public_metrics', {})
        likes = metrics.get('like_count', 0)
        retweets = metrics.get('retweet_count', 0)
        
        # Truncate long tweets for display
        if len(text) > 120:
            text = text[:117] + "..."
        
        print(f"{i:2d}. @{author_handle} ({author_name})")
        print(f"    Date: {created_at}")
        print(f"    Tweet: {text}")
        print(f"    Likes: {likes:,} | Retweets: {retweets:,}")
        print()

def display_locations(locations: List[Dict]) -> None:
    """Display available trend locations"""
    if not locations:
        print("No locations found.")
        return
    
    print(f"\n{'='*80}")
    print("AVAILABLE TREND LOCATIONS (WOEID)")
    print(f"{'='*80}")
    
    for i, location in enumerate(locations, 1):
        name = location.get('name', 'Unknown')
        country = location.get('country', 'Unknown')
        woeid = location.get('woeid', 'Unknown')
        
        print(f"{i:3d}. {name}, {country} (WOEID: {woeid})")

def main() -> None:
    """Main function to run the Twitter trending fetcher"""
    print("Welcome to the Twitter Trending Hashtags Fetcher!")
    
    # Initialize Twitter client
    client = TwitterClient()
    
    if not client.bearer_token:
        print("Error: Twitter Bearer Token not found.")
        print("Please set the TWITTER_BEARER_TOKEN environment variable.")
        sys.exit(1)
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == '1':
            limit = get_limit()
            print("Fetching global trending hashtags...")
            hashtags = client.get_trending_hashtags(woeid=1, limit=limit)
            if hashtags is not None:
                display_trending_hashtags(hashtags, "Global")
            else:
                print("Failed to fetch trending hashtags.")
        
        elif choice == '2':
            woeid = get_woeid()
            limit = get_limit()
            print(f"Fetching trending hashtags for WOEID {woeid}...")
            hashtags = client.get_trending_hashtags(woeid=woeid, limit=limit)
            if hashtags is not None:
                location_name = "Custom Location" if woeid != 1 else "Global"
                display_trending_hashtags(hashtags, location_name)
            else:
                print("Failed to fetch trending hashtags.")
        
        elif choice == '3':
            hashtag = get_hashtag()
            limit = get_limit()
            print(f"Searching for tweets with {hashtag}...")
            tweets = client.get_tweets_by_hashtag(hashtag, limit=limit)
            if tweets is not None:
                display_tweets(tweets, hashtag)
            else:
                print("Failed to fetch tweets.")
        
        elif choice == '4':
            print("Fetching available trend locations...")
            locations = client.get_available_trend_locations()
            if locations is not None:
                display_locations(locations)
            else:
                print("Failed to fetch locations.")
        
        elif choice == '5':
            print("Thank you for using the Twitter Trending Hashtags Fetcher. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1-5.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)