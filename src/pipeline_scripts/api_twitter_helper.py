import tweepy
from tweepy.errors import TwitterServerError

from datetime import timezone
from typing import List,Optional,Literal
import time

def fetch_recent_tweets(bearer_token: str, accounts: Optional[List[str]] = None, asset: str = None, max_results: int = 10):
    """
    Fetch the most recent tweets matching either a list of accounts or keywords.
    
    :param bearer_token:    Your Twitter API Bearer Token
    :param accounts:        List of usernames (without the “@”), e.g. ["business","elonmusk"]
    :param asset:           Asset to query, e.g. ["crypto","SP500"]
    :param max_results:     Number of tweets to fetch , with a free X API account not more than 100 queries avaliable, recommended 10.
    
    :return:                List of tweepy.Tweet objects
    """
    #Initialize client
    if not bearer_token:
        raise ValueError("You must provide a bearer_token.")
    client = tweepy.Client(bearer_token=bearer_token)
    

    accounts = accounts or []
    if not asset:
        raise ValueError("You must specify one asset.")
    
    #Build query 
    query_parts  = []
    if accounts:
        accounts_query = " OR ".join(f"from:{acct}" for acct in accounts)
        query_parts.append(f"({accounts_query})")

    asset_query = f'"{asset}"' if " " in asset else asset
    query_parts.append(asset_query)    

    query = " ".join(query_parts)
    # filter out retweets & replies
    query += " -is:retweet -is:reply"
    print(f"Query: {query}")

    #Fetch tweets
    try:
        response = client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["id","text","created_at","author_id"],
                sort_order="recency"
            )
        
        tweets = response.data or []
        return tweets

    except tweepy.TwitterServerError as e:
       print(f"Error fetching tweets: {e}")
