from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os
from spotifyclient import SpotifyClient
from dotenv import load_dotenv

load_dotenv()
SPOTIFY_AUTHORIZATION_TOKEN = os.getenv('SPOTIFY_AUTHORIZATION_TOKEN')
# SPOTIFY_USER_ID = os.getenv("SPOTIFY_USER_ID")

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ban the wind'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/username', methods=["GET", "POST"])
def username():
    playlist = request.form.get("playlist")
    find_id = request.form.get("find_id")
    if(playlist):
        return render_template('playlist.html', session=session)
    if(find_id):
        return render_template('DO_LATERQUES.html', session=session)
    else:
        redirect('index.html')
    # return render_template('Username_howto.html')

@app.route('/playlist', methods=["GET", "POST"])
def playlist():
    if(request.method == 'POST'):
        SPOTIFY_USER_ID = request.form.get('user_id')
        vis_num = request.form.get('vis_num')
        global play_length
        play_length = request.form.get('length')
        global play_name
        play_name = request.form.get('play_name')
        global spotify_client
        spotify_client = SpotifyClient(SPOTIFY_AUTHORIZATION_TOKEN, SPOTIFY_USER_ID)
        global last_played_tracks
        last_played_tracks = spotify_client.get_last_played_tracks(vis_num)
        length = len(last_played_tracks)
        return render_template('last_tracks.html', len=length, last_played_tracks=last_played_tracks, num=vis_num)

@app.route('/last_tracks', methods=["GET", "POST"])
def last_tracks():
    seeds = request.form.get('seeds')
    seeds = seeds.split()
    seed_tracks = [last_played_tracks[int(seed)-1] for seed in seeds]
    recommended_tracks = spotify_client.get_track_recommendations(seed_tracks, limit=play_length)
    playlist = spotify_client.create_playlist(play_name)
    spotify_client.populate_playlist(playlist, recommended_tracks)
    if(request.method == 'POST'):
        return render_template('playlist_done.html', session=session)

@app.route('/playlist_done')
def playlist_done():
    # return render_template('playlist_done.html', session=session)
    pass

if __name__ == '__main__':
    app.run()