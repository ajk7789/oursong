import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

def get_most_popular(tracks):
    """
    description: finds the most popular track in a list of tracks
    parameters:
        tracks - a list of json strings of spotify tracks
    returns:
        string id of the most popular song within the list of tracks
    """
    highest_popularity = 0
    most_popular = ''
    for track in tracks:
        if track['popularity'] > highest_popularity:
            highest_popularity = track['popularity']
            most_popular = track['id']
    return most_popular


def main():
    """
    description: main program for finding a song result
    parameters: None
    returns: None
    """

    load_dotenv() # loads the environment variables from my .env file

    # uses my spotify credentials to create a spotipy object
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    date = '2012-07-11' # example date we are using for the search

    # instantiating empty stuff
    same_year_songs = []
    songs = []
    counter = 0
    highest_popularity = 0
    most_popular = ''

    max_queries = 10 # max number of times we'll query spotify before giving up

    # searches spotify <10 times, looking for tracks under the 'romance' genre
    while len(same_year_songs) == 0 and len(songs) == 0 and counter < max_queries:
        results = sp.recommendations(seed_genres=['romance'], limit=100, country='US') # can only get 100 results per query
        for track in results['tracks']:
            if track['album']['release_date_precision'] == "day":
                if track['album']['release_date'] == date:
                    same_year_songs.append(track) # one list for songs release on the exact day and year
                elif track['album']['release_date'][5:] == date[5:]:
                    songs.append(track) # a different list for songs release on the same day
                if track['popularity'] > highest_popularity: # also keeping track of most popular song
                    highest_popularity = track['popularity']
                    most_popular = track["id"] 
        counter += 1

    if len(same_year_songs) > 0: # try and make the result the most popular track from the exact same date
        song_result = get_most_popular(same_year_songs)
    elif len(songs) > 0: # if none, make it the most popular song from the same day
        song_result = get_most_popular(songs)
    else: # last case, we just make it the most popular song
        song_result = most_popular

    print(song_result)

if __name__ == '__main__':
    main()