import requests
import urllib.parse
from flask import Flask, redirect, jsonify, request, session
from datetime import datetime
import time
import spotifyManager

app = Flask(__name__)
app.secret_key = '123456789'

#put your CLIENT ID here
CLIENT_ID = ''
#put your client secret here
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Please sign into your spotify account <a href ='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-read-currently-playing'
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI
    }
    
    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'
    
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        session['access_token'] = token_info['access_token'] #uses to authorize access
        session['refresh_token'] = token_info['refresh_token'] #refreshes the access token
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in'] #number of seconds before access tokens expires
        
        return "<a href ='/check-ads'>click here to start the service</a>"
@app.route('/check-ads')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    previous_track = ""
    while True:
        response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)
        current_song = response.json()
        if current_song['currently_playing_type'] == "ad":
            spotifyManager.restartSpotify()
            previous_track = ""
            time.sleep(3)
            continue
        if current_song['item']['name'] != previous_track:
            pause = current_song['item']['duration_ms'] - current_song['progress_ms']
            time.sleep(pause/1000 - 5)
            previous_track = current_song['item']['name']
            
            
        

@app.route('/refresh-token')
def refresh_token():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        response = requests.post(TOKEN_URL, data = req_body)
        new_token_info = response.json() 
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
        return redirect('/refresh-token')
    return redirect('/check-ads')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
        
        