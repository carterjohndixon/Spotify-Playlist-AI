import os
from spotifyclient import SpotifyClient
from dotenv import load_dotenv

load_dotenv()
SPOTIFY_AUTHORIZATION_TOKEN = os.getenv('SPOTIFY_AUTHORIZATION_TOKEN')
# SPOTIFY_USER_ID = os.getenv("SPOTIFY_USER_ID")

def main():
    spotify_client = SpotifyClient(SPOTIFY_AUTHORIZATION_TOKEN, SPOTIFY_USER_ID)

    num_tracks_to_visualize = int(input("How many tracks would you like to visualize? (AT MOST 50): "))
    last_played_tracks = spotify_client.get_last_played_tracks(num_tracks_to_visualize)
    print(last_played_tracks)

    print(f"Here are the last {num_tracks_to_visualize} tracks you've listened to on Spotify: ")
    for index, track in enumerate(last_played_tracks):
        print(f"{index+1}- {track}")

    indexes = input("Enter a list of up to 5 track you'd like to use as seeds. Use indexes seperated by a space: ")
    indexes = indexes.split()
    seed_tracks = [last_played_tracks[int(index)-1] for index in indexes]

    num_of_songs_on_new_playlist = int(input("How many songs do you want on this playlist? (AT MOST 100): "))
    recommended_tracks = spotify_client.get_track_recommendations(seed_tracks, limit=num_of_songs_on_new_playlist)
    for index, track in enumerate(recommended_tracks):
        print(f"{index+1}- {track}")

    playlist_name = input("What's the playlists name? ")
    playlist = spotify_client.create_playlist(playlist_name)
    print(f"Playlist '{playlist_name}'  was created successfully.")

    spotify_client.populate_playlist(playlist, recommended_tracks)
    print(f"Recommended tracks successfully uploaded to play list '{playlist_name}'")

if __name__ == '__main__':
    main()