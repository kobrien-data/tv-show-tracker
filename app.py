from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
import os
import secrets
from pymongo import MongoClient
import requests
from urllib.parse import quote
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB setup
client = MongoClient(app.config['MONGODB_URI'], tls=True,
    tlsAllowInvalidCertificates=True)
db = client['tv_tracker']
shows_collection = db['shows']
users_collection = db['users']

# OAuth setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, email, name, picture):
        self.id = user_id
        self.email = email
        self.name = name
        self.picture = picture

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'_id': user_id})
    if user_data:
        return User(str(user_data['_id']), user_data['email'], user_data['name'], user_data.get('picture'))
    return None

@app.route('/test-session')
def test_session():
    if 'test' in session:
        return f"Session works! Value: {session['test']}"
    else:
        session['test'] = 'hello'
        return 'Session set. <a href="/test-session">Refresh to test</a>'

# Login route
@app.route('/login')
def login():
    # Manually create and store nonce and state
    nonce = secrets.token_urlsafe(16)
    state = secrets.token_urlsafe(16)
    
    session['oauth_nonce'] = nonce
    session['oauth_state'] = state
    
    print(f"Setting state in session: {state}")
    print(f"Session after setting state: {dict(session)}")
    
    redirect_uri = url_for('authorize', _external=True)

    print(f"====== REDIRECT URI DEBUG ======")
    print(f"Redirect URI being sent: {redirect_uri}")
    print(f"================================")
    
    # Use authorize_redirect with explicit state
    return google.authorize_redirect(
        redirect_uri,
        nonce=nonce,
        state=state
    )

# OAuth callback
@app.route('/login/callback')
def authorize():
    print(f"Session in callback: {dict(session)}")
    print(f"State from request: {request.args.get('state')}")
    print(f"State from session: {session.get('oauth_state')}")
    
    try:
        # Authlib will automatically verify the state from session
        token = google.authorize_access_token()
        
        # Get user info
        user_info = token.get('userinfo')
        
        # Clear OAuth session data
        session.pop('oauth_nonce', None)
        session.pop('oauth_state', None)
        
        user_id = str(user_info['sub'])
        
        users_collection.update_one(
            {'_id': user_id},
            {'$set': {
                '_id': user_id,
                'email': user_info['email'],
                'name': user_info['name'],
                'picture': user_info.get('picture')
            }},
            upsert=True
        )
        
        user = User(user_id, user_info['email'], user_info['name'], user_info.get('picture'))
        login_user(user)
        return redirect(url_for('index'))
        
    except Exception as e:
        print(f"Full error: {e}")
        import traceback
        traceback.print_exc()
        return f"Error during OAuth callback: {e}<br><br>Check terminal for details", 400

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Homepage - display all tracked shows"""
    shows = list(shows_collection.find({'user_id': current_user.id}))
    for show in shows:
        print(f"\n{show['name']}:")
        print(f"  Has seasons_data? {'seasons_data' in show}")
        if 'seasons_data' in show:
            print(f"  Seasons data: {show['seasons_data']}")
    return render_template('index.html', shows=shows)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_show():
    """Add a new show"""
    if request.method == 'GET':
        return render_template('add_show.html')
    
    # Handle search - FIRST IF
    if 'search' in request.form:
        print("Handling search...")
        search_query = request.form.get('query')
        encoded_query = quote(search_query)
        url = f"https://api.themoviedb.org/3/search/tv?query={encoded_query}&api_key={app.config['TMDB_API_KEY']}"
        
        response = requests.get(url)
        data = response.json()
        
        return render_template('add_show.html', results=data.get('results', []), search_query=search_query)
    
    # Handle selecting a show - ELIF (not if!)
    elif 'select_show' in request.form:
        print("Handling select_show...")
        show_id = request.form.get('show_id')
        show_name = request.form.get('show_name')
        
        print(f"Selected: {show_name} (ID: {show_id})")
        
        # Get detailed info
        detail_url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={app.config['TMDB_API_KEY']}"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()

        seasons = detail_data.get('seasons', [])
        print(f"Raw seasons from API: {seasons}")
        actual_seasons = [s for s in seasons if s.get('season_number', 0) > 0]  # Filter out "Season 0" (specials)
        print(f"Filtered actual_seasons: {actual_seasons}")

        seasons_data = {}
        for season in actual_seasons:
            seasons_data[str(season['season_number'])] = season['episode_count']
        print(f"Final seasons_data: {seasons_data}")

        print(f"Seasons data: {seasons_data}")
        
        # Prepare show info to pass to template
        poster_path = detail_data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w342{poster_path}" if poster_path else None
        
        show_info = {
            'id': show_id,
            'name': show_name,
            'number_of_seasons': detail_data.get('number_of_seasons', 0),
            'poster_url': poster_url,
            'overview': detail_data.get('overview', '')
        }
        print(f"Show data being saved: {show_info}") 
        print("Returning template with selected_show...")
        return render_template('add_show.html', selected_show=show_info)
    
    # Handle final add with season/episode - ELIF (not if!)
    elif 'confirm_add' in request.form:
        print("Handling confirm_add...")
        show_id = request.form.get('show_id')
        show_name = request.form.get('show_name')
        poster_url = request.form.get('poster_url')
        overview = request.form.get('overview')
        number_of_seasons = int(request.form.get('number_of_seasons'))
        current_season = int(request.form.get('current_season'))
        current_episode = int(request.form.get('current_episode'))

        detail_url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={app.config['TMDB_API_KEY']}"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()
        
        seasons = detail_data.get('seasons', [])
        actual_seasons = [s for s in seasons if s.get('season_number', 0) > 0]
        
        seasons_data = {}
        for season in actual_seasons:
            seasons_data[str(season['season_number'])] = season['episode_count']
        
        # Prepare show data
        show_data = {
            'user_id': current_user.id,
            'name': show_name,
            'tmdb_id': show_id,
            'number_of_seasons': number_of_seasons,
            'seasons_data': seasons_data,
            'current_season': current_season,
            'current_episode': current_episode,
            'poster_url': poster_url if poster_url else None,
            'overview': overview
        }
        
        # Save to MongoDB
        shows_collection.update_one(
            {'name': show_name, 'user_id': current_user.id},
            {'$set': show_data},
            upsert=True
        )
        
        return redirect(url_for('index'))
    
    # If nothing matched
    return redirect(url_for('add_show'))

@app.route('/update/<show_name>', methods=['GET', 'POST'])
@login_required
def update_show(show_name):
    """Update a show's progress"""
    show = shows_collection.find_one({'name': show_name, 'user_id': current_user.id})
    
    if not show:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        season = int(request.form.get('season'))
        episode = int(request.form.get('episode'))
        
        shows_collection.update_one(
            {'name': show_name, 'user_id': current_user.id},
            {'$set': {
                'current_season': season,
                'current_episode': episode
            }}
        )
        
        return redirect(url_for('index'))
    
    return render_template('update_show.html', show=show)

@app.route('/delete/<show_name>', methods=['POST'])
@login_required
def delete_show(show_name):
    """Delete a show"""
    shows_collection.delete_one({'name': show_name, 'user_id': current_user.id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
