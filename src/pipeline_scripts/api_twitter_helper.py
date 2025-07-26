import tweepy
from datetime import timezone
from typing import List,Optional

def fetch_recent_tweets(bearer_token: str, accounts: Optional[List[str]] = None, keywords: Optional[List[str]] = None, max_results: int = 10):
    """
    Fetch the most recent tweets matching either a list of accounts or keywords.
    
    :param bearer_token:    Your Twitter API Bearer Token
    :param accounts:        List of usernames (without the “@”), e.g. ["business","elonmusk"]
    :param keywords:        List of keywords, e.g. ["crypto","SP500"]
    :param max_results:     Number of tweets to fetch , with a free X API account not more than 100 queries avaliable, recommended 10.
    
    :return:                List of tweepy.Tweet objects
    """
    #Initialize client
    client = tweepy.Client(bearer_token=bearer_token)
    
    accounts = accounts or []
    keywords = keywords or []
    if not accounts and not keywords:
        raise ValueError("You must specify at least one account or keyword.")
    
    #Build your query string
    parts = []
    if accounts:
        parts.append(" OR ".join(f"from:{acct}" for acct in accounts))
    if keywords:
        parts.append(" OR ".join(keywords))
    query = " OR ".join(f"({p})" for p in parts)
    # filter out retweets & replies
    query += " -is:retweet -is:reply"
    
    #Call the recent search endpoint
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,                 
        tweet_fields=["id", "text", "created_at", "author_id"],
        sort_order="recency"
    )
    
    # Pull out a plain list 
    tweets = response.data or []
    next_token = response.meta.get("next_token")
    if next_token:
        resp2 = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["id","text","created_at","author_id"],
            sort_order="recency",
            next_token=next_token
        )
        tweets.extend(resp2.data or [])
    
    return tweets
