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

# IDs of the posts last tweeted
last_tweeted_posts_id = []

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


# tweet reddit posts
def post_tweet():
    global last_tweeted_posts_id
    try:
        posts = get_reddit_posts()

        # setup connection with twitter
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        api = tweepy.API(auth)

        # IDs of the posts tweeted now
        curr_tweeted_posts_id = []

        # reverse posts to keep timeline posts in the same order as reddit
        for post in reversed(list(posts)):
            # avoid duplicate tweets
            if post.id in last_tweeted_posts_id:
                curr_tweeted_posts_id.append(post.id)
                continue

            print(post.title + post.url)
            api.update_status(status=post.title + '\n' + post.url)
            curr_tweeted_posts_id.append(post.id)
    except Exception as error:
        print('Error while posting tweet: {}'.format(error))
    finally:
        # assign currently tweeted post IDs list to the last tweeted list
        last_tweeted_posts_id = curr_tweeted_posts_id


def main():
    while True:
        post_tweet()
        time.sleep(interval)


if __name__ == '__main__':
    main()
