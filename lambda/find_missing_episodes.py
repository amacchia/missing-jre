import json
import traceback
import logging

from spotify_client import get_filtered_episodes_from_spotify
from twitter_client import tweet_missing_episodes

logger = logging.getLogger()

def main(event, lambda_context):
    try:
        spotify_episode_numbers = get_filtered_episodes_from_spotify()
        logger.info("Retrieved episodes from spotify")
        all_episodes_dict = get_all_episodes_dict()
        logger.info("Read in master list")
        missing_episodes = find_missing_episodes(
            all_episodes_dict, spotify_episode_numbers)
        logger.info("Found missing episodes")
        tweet_missing_episodes(missing_episodes)
        logger.info("Tweeted missing episodes")
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)


def get_all_episodes_dict():
    with open("master-list.json") as all_episodes_json:
        return json.load(all_episodes_json)


def find_missing_episodes(all_episodes_dict, spotify_episode_numbers):
    all_episode_numbers = set(all_episodes_dict.keys())
    missing_episode_numbers = all_episode_numbers - spotify_episode_numbers
    missing_episode_numbers = sorted(
        missing_episode_numbers, key=lambda e: int(e[1:]), reverse=True)
    return [all_episodes_dict[missing_ep_number]
            for missing_ep_number in missing_episode_numbers]


if __name__ == '__main__':
    main(None, None)
