#!/usr/bin/python3

# Retrieve the authenticated user's uploaded videos.
# Sample usage:
# python my_uploads.py

# import re

import pickle

# import google.oauth2.credentials
# import google_auth_oauthlib.flow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    credentials = load_authentication_tokens()
    if credentials is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES
        )
        credentials = flow.run_console()
        store_authentication_tokens(credentials)

    return build(
        API_SERVICE_NAME,
        API_VERSION,
        credentials=credentials
    )


def store_authentication_tokens(credentials):
    pickle.dump(credentials, open('credentials.pickle', 'wb'))


def load_authentication_tokens():
    try:
        pkl = pickle.load(open('credentials.pickle', 'rb'))
        return pkl
    except (OSError, IOError) as e:
        return None


def list_playlist_videos(playlistId):
    # Retrieve the list of videos in the authenticated user's playlist by ID.
    playlistitems_list_request = youtube.playlistItems().list(
        playlistId=playlistId,
        part='snippet',
        maxResults=5
    )

    print('Videos in list %s' % playlistId)
    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()

        # Print information about each video.
        for playlist_item in playlistitems_list_response['items']:
            title = playlist_item['snippet']['title']
            video_id = playlist_item['snippet']['resourceId']['videoId']
            print('%s (%s)' % (title, video_id))

        playlistitems_list_request = youtube.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)


if __name__ == '__main__':
    youtube = get_authenticated_service()
    try:
        list_playlist_videos("PLBNBJ7rq0OELC5k4_HVssC8Hj4XXqLrbN")
    except e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
