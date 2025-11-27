import os
class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET')
    SECRET_KEY=os.environ.get('SECRET_KEY')