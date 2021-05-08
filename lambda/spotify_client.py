from secrets import spotify_authorization

import requests

from request_utils import check_response_code

starting_url = "https://api.spotify.com/v1/shows/4rOoJ6Egrf8K2IrywzwOMk/episodes?market=US&limit=50"


def get_filtered_episodes_from_spotify():
    bearer_token = _get_bearer_token()
    next_url = starting_url
    spotify_episode_numbers = set()

    while next_url != None:
        response = _get_episodes_from_spotify(next_url, bearer_token)
        next_url = response['next']
        raw_episodes = response['items']
        spotify_episode_numbers.update(_filter_episodes(raw_episodes))

    return spotify_episode_numbers


def _get_bearer_token():
    url = "https://accounts.spotify.com/api/token"
    payload = 'grant_type=client_credentials'
    headers = {
        'Authorization': f'Basic {spotify_authorization}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload)
    check_response_code(response)
    return response.json()['access_token']


def _get_episodes_from_spotify(url, bearer_token):
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    response = requests.request("GET", url, headers=headers)
    check_response_code(response)
    return response.json()


def _filter_episodes(episodes):
    episode_numbers = set()
    for ep in episodes:
        name: str = ep['name']
        if not name.startswith('#'):
            continue

        episode_numbers.add(name.split('-')[0].strip())

    return episode_numbers
