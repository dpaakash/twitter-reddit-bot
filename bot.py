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

# interval(in seconds) between tweeting the reddit posts
interval = 12*60*60


# get posts from the subreddit
def get_reddit_posts():
    print('Fetching posts from reddit...')
    try:
        # setup connection with reddit
        r = praw.Reddit(
            user_agent='algorithms subreddit bot',
            client_id=reddit_client_id,
            client_secret=reddit_client_secret
        )

        # get current top 10 posts
        posts = r.subreddit(subreddit_name).hot(limit=10)
    except Exception as error:
        print('Error while fetching posts from reddit: {}'.format(error))
    return posts


# check if a post has already been tweeted
def isPostTweeted(post):
    with open('posted_tweets.txt', 'r') as input_file:
        for line in input_file:
            if post.id in line:
                return True
    return False


# store id of the tweeted reddit post
def storePostId(post):
    with open('posted_tweets.txt', 'a') as output_file:
        output_file.write(str(post.id) + '\n')


# tweet reddit posts
def post_tweet():
    try:
        posts = get_reddit_posts()

        # setup connection with twitter
        auth = tweepy.OAuthHandler(
            twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token,
                              twitter_access_token_secret)
        api = tweepy.API(auth)

        for post in posts:

            # avoid duplicate tweets
            if isPostTweeted(post):
                continue

            print(post.title + post.url)
            api.update_status(status=post.title + '\n' + post.url)
            storePostId(post)
    except Exception as error:
        print('Error while posting tweet: {}'.format(error))


def main():
    while True:
        post_tweet()
        time.sleep(interval)


if __name__ == '__main__':
    main()
