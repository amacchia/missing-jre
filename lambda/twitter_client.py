from datetime import datetime
from secrets import (twitter_access_token, twitter_api_key, twitter_secret_key,
                     twitter_token_secret)

import requests
from requests_oauthlib import OAuth1

from request_utils import check_response_code

url = "https://api.twitter.com/1.1/statuses/update.json"


MAX_CHARACTERS_PER_TWEET = 280


def tweet_missing_episodes(missing_episodes):
    tweets = _build_tweets(missing_episodes)

    first_tweet = tweets[0]
    reply_id = _post_tweet(first_tweet, None)
    for tweet in tweets[1:]:
        reply_id = _post_tweet(tweet, reply_id)


def _build_tweets(missing_episodes):
    tweets = []

    tweet_string = f'Total Missing Episodes as of {datetime.now().isoformat()}: {len(missing_episodes)}\n'
    for missing_ep in missing_episodes:
        missing_ep_string = f"{missing_ep['episodeNumber']} - {missing_ep['guest']}"
        if len(tweet_string) + len(missing_ep_string) > MAX_CHARACTERS_PER_TWEET:
            tweets.append(tweet_string)
            tweet_string = missing_ep_string
            continue
        tweet_string += f"\n{missing_ep_string}"

    return tweets


def _post_tweet(tweet_status, reply_status_id):
    params = {
        'status': tweet_status,
        'in_reply_to_status_id': reply_status_id
    }
    auth = OAuth1(twitter_api_key, twitter_secret_key,
                  twitter_access_token, twitter_token_secret)

    response = requests.request("POST", url, params=params, auth=auth)
    check_response_code(response)
    return response.json()['id']
