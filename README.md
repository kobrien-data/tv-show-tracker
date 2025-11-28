# TV Show Tracker
An application used to track which season/episode of a TV show you're on to so you don't ever forget which episode was the last one you watched

## 🎯 The Motivation
Among recent conversations around streaming services and whether we actually own digital content that we pay for, and the disappointment of going to watch your favourite show only to notice that it is no longer available on any of the services you pay for has some people returning to physical media like DVDs. 

As this is something that I myself have started doing, one problem that I've had is remembering what was the last episode I watched, especially if I've taken a break from watching the show for a while. Streaming provides a digital bookmark, you can put a physical bookmark in a book, but you can't bookmark a DVD. And that's why I wanted to make this application, so that I, and many other DVD users can easily create bookmarks for our shows, and don't have to spend time searching Wikipedia for the episode that sounds the most familiar. 

## ✨ Features
* **Track Multiple Shows:** Add and manage all your TV shows in one place
* **Episode Bookmarking:** Save you current season and episode for each show
* **Extra Show Information:** Automatic integration with TMDB API for show details, artwork, etc
* **Persistent Storage:** MongoDB Atlas integration ensures your data is always saved

## 🚀 Live Demo
Check out the live application: [TV Show Tracker](https://tv-show-tracker-6yet.onrender.com/)

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database:** MongoDB Atlas
* **API:** TMBD API
* **Deployment:** Render

## 📋 Prerequisites
If you want to run this project locally, make sure you have:
* Python 3.10 or higher
* MongoDB Atlas account
* TMDB API Key

## 🔧 Installation
1. **Clone the repository**
    ```
    git clone https://github.com/kobrien-data/tv-show-tracker.git
    cd tv-show-tracker
    ```
2. **Create a virtual environment**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   * substitute the values in the config.py file for your own
5. **Run the application**
   ```
   python3 app.py
   ```
6. **Navigate to:** http://localhost:5001

## 📖 Usage
1. **Add Show:** Enter the TV show name to search TMDB and add it to your tracker
2. **Update Show:** Mark your current season and episode for each show
3. **List Shows:** See all your shows with their current progress at a glance
4. **Delete Show:** Remove shows you've finished or no longer watch

## 🗺️ Development Journey
This project evolved through several phases:
1. **MVP:** Basic Python CLI with JSON file storage
2. **API Integration:** Added TMDB API for rich show metadata
3. **Database Migration:** Transitioned from JSON to MongoDB Atlas for scalable data storage
4. **Web Interface:** Built Flask web application with responsive UI
5. **User Integration:** Integrated user capabilities using Google OAuth

## 👩🏻‍💻 Author
**Kai O'Brien**
