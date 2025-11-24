from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import MONGODB_URI, TMDB_API_KEY
from pymongo import MongoClient
import requests
from urllib.parse import quote

app = Flask(__name__)

# MongoDB setup
client = MongoClient(MONGODB_URI, tls=True,
    tlsAllowInvalidCertificates=True)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['tv_tracker']
shows_collection = db['shows']

@app.route('/')
def index():
    """Homepage - display all tracked shows"""
    shows = list(shows_collection.find())
    return render_template('index.html', shows=shows)

@app.route('/add', methods=['GET', 'POST'])
def add_show():
    """Add a new show"""
    if request.method == 'GET':
        return render_template('add_show.html')
    
    # Handle search
    if 'search' in request.form:
        search_query = request.form.get('query')
        encoded_query = quote(search_query)
        url = f"https://api.themoviedb.org/3/search/tv?query={encoded_query}&api_key={TMDB_API_KEY}"
        
        response = requests.get(url)
        data = response.json()
        
        return render_template('add_show.html', results=data.get('results', []), search_query=search_query)
    
    # Handle adding selected show
    if 'add_show' in request.form:
        show_id = request.form.get('show_id')
        show_name = request.form.get('show_name')
        
        # Get detailed info
        detail_url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={TMDB_API_KEY}"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()
        
        # Prepare show data
        poster_path = detail_data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w342{poster_path}" if poster_path else None
        
        show_data = {
            'name': show_name,
            'tmdb_id': show_id,
            'number_of_seasons': detail_data.get('number_of_seasons', 0),
            'current_season': 1,
            'current_episode': 1,
            'poster_url': poster_url,
            'overview': detail_data.get('overview', '')
        }
        
        # Save to MongoDB
        shows_collection.update_one(
            {'name': show_name},
            {'$set': show_data},
            upsert=True
        )
        
        return redirect(url_for('index'))
    
    return redirect(url_for('add_show'))

@app.route('/update/<show_name>', methods=['GET', 'POST'])
def update_show(show_name):
    """Update a show's progress"""
    show = shows_collection.find_one({'name': show_name})
    
    if not show:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        season = int(request.form.get('season'))
        episode = int(request.form.get('episode'))
        
        shows_collection.update_one(
            {'name': show_name},
            {'$set': {
                'current_season': season,
                'current_episode': episode
            }}
        )
        
        return redirect(url_for('index'))
    
    return render_template('update_show.html', show=show)

@app.route('/delete/<show_name>', methods=['POST'])
def delete_show(show_name):
    """Delete a show"""
    shows_collection.delete_one({'name': show_name})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
