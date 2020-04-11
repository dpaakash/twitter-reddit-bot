from os import environ
import time

import praw
import tweepy

# API keys and tokens
twitter_access_token = environ['twitter_access_token']
twitter_access_token_secret = environ['twitter_access_token_secret']
twitter_consumer_key = environ['twitter_consumer_key']
twitter_consumer_secret = environ['twitter_consumer_secret']
reddit_client_id = environ['reddit_client_id']
reddit_client_secret = environ['reddit_client_secret']

# subreddit to fetch posts from
subreddit_name = 'algorithms'

def get_reddit_posts():
    print ('Fetching posts from reddit...')
    try:
        r = praw.Reddit(
            user_agent='algorithms subreddit bot',
            client_id=reddit_client_id,
            client_secret=reddit_client_secret
        )
        posts = r.subreddit(subreddit_name).hot(limit=5)
    except Error:
        print('Error while fetching posts from reddit')
    return posts

def generate_tweet():
    posts = get_reddit_posts()
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    api = tweepy.API(auth)
    for post in posts:
        print(post.title + post.url)
        api.update_status(status=post.title + '\n' + post.url)
        time.sleep(30)

def main():
    generate_tweet()

if __name__ == '__main__':
    main()
