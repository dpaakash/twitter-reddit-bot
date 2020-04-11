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
    print('Fetching posts from reddit...')
    try:
        r = praw.Reddit(
            user_agent='algorithms subreddit bot',
            client_id=reddit_client_id,
            client_secret=reddit_client_secret
        )
        posts = r.subreddit(subreddit_name).hot(limit=5)
    except Exception as error:
        print('Error while fetching posts from reddit: {}'.format(error))
    return posts


def post_tweet():
    try:
        posts = get_reddit_posts()
        auth = tweepy.OAuthHandler(
            twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token,
                              twitter_access_token_secret)
        api = tweepy.API(auth)
        for post in posts:
            print(post.title + post.url)
            api.update_status(status=post.title + '\n' + post.url)
            time.sleep(5)
    except Exception as error:
        print('Error while posting tweet: {}'.format(error))


def main():
    while True:
        post_tweet()
        time.sleep(12*60*60)


if __name__ == '__main__':
    main()
