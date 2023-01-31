import os
import subprocess

import spotipy
from spotipy import util


class Spotify:
    def __init__(self):
        scope = 'user-read-playback-state,user-modify-playback-state,app-remote-control,user-read-currently-playing'
        self.__token = util.prompt_for_user_token(
            os.environ['SPOTIPY_USERNAME'],
            scope,
            os.environ['SPOTIPY_CLIENT_ID'],
            os.environ['SPOTIPY_CLIENT_SECRET'],
            os.environ['SPOTIPY_REDIRECT_URI'],
        )
        self.__spotify = spotipy.Spotify(auth=self.__token)

    def is_device_avaliable(self):
        """Check if spotify is running, if not, open it

        Returns:
            bool: True if spotify is running, False otherwise
        """
        
        devices = self.__spotify.devices()['devices']

        if len(devices) == 0:
            return False

        for device in devices:
            if device['is_active'] is True:
                return True

        return False

    def open_client(self):
        """Open spotify client
        """
        
        command = 'flatpak run com.spotify.Client '
        subprocess.call(command.split())

    def play_song(self, song_name):
        results = self.__spotify.search(song_name, limit=1, type='track')
        if len(results['tracks']['items']) == 0:
            return 'Não consegui encontrar.'

        uri = results['tracks']['items'][0]['uri']
        self.__spotify.start_playback(device_id=None, uris=[uri])

        artist_name = results['tracks']['items'][0]['artists'][0]['name']
        song_name = results['tracks']['items'][0]['name']

        return f'Tocando música: {song_name} de {artist_name}'

    def play_playlist(self, playlist_name):
        print(playlist_name)
        my_playlists = self.__spotify.current_user_playlists()
        match = [playlist for playlist in my_playlists['items']
                 if playlist['name'].lower() == playlist_name.lower()]
        if not match:
            return 'Não consegui encontrar.'

        self.__spotify.start_playback(context_uri=match[0]['uri'])
        return f"Tocando playlist: {match[0]['name']}"

    def search_and_play_playlist(self, search_query):
        results = self.__spotify.search(search_query, limit=1, type='playlist')
        if len(results['playlists']['items']) == 0:
            return 'Não consegui encontrar a playlist.'

        playlist = results['playlists']['items'][0]
        self.__spotify.start_playback(context_uri=playlist['uri'])

        return f"Tocando playlist: {playlist['name']}"

    def toggle_play_pause(self):
        is_playing = self.__spotify.current_playback()['is_playing']

        if is_playing:
            self.__spotify.pause_playback()
        else:
            self.__spotify.start_playback()

    def next(self):
        self.__spotify.next_track()

    def previous(self):
        self.__spotify.previous_track()

