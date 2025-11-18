from config import TMDB_API_KEY, MONGODB_URI
import requests
import pymongo
from urllib.parse import quote

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = MONGODB_URI
# Create a new client and connect to the server
client = MongoClient(uri)
db = client['tv_show_tracker']  # Database name
shows_collection = db['shows']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def get_show(show_name: str) -> dict | None:
    """
    Retrieves a show's data from the MongoDB collection.

    Parameters:
    show_name (str): The name of the TV show.

    Returns:
    dict | None: The data associated with the TV show, or None if not found.
    """
    show_doc = shows_collection.find_one({'name': show_name})
    if show_doc:
        return {k: v for k, v in show_doc.items() if k not in ['_id', 'name']}
    return None

def delete_show() -> None:
    """
    Deletes a show from the MongoDB collection.

    Parameters:
    show_name (str): The name of the TV show.

    Returns:
    None
    """
    show_name = input("Enter the name of the show to update: ")
    shows_collection.delete_one({'name': show_name})

def update_episode() -> None:
    """
    Updates the current season and episode of a TV show in the MongoDB collection.

    Returns:
    None
    """
    if shows_collection.count_documents({}) == 0:
        print("No shows tracked yet.")
        return
    
    print("Tracked Shows:")
    all_shows = list(shows_collection.find())
    for i, show in enumerate(all_shows, 1):
        print(f"{i}. {show['name']} (S{show['current_season']}E{show['current_episode']})")

    try:
        choice = int(input("Select a show to update by number: "))
        if choice < 1 or choice > len(all_shows):
            print("Invalid choice.")
            return
        
        selected_show = all_shows[choice - 1]
        show_name = selected_show['name']
    except ValueError:
        print("Please enter a valid number.")
        return
    
    try:
        season_number = int(input("Enter the new season number: "))
        episode_number = int(input("Enter the new episode number: "))
    except ValueError:
        print("Please enter valid integers for season and episode numbers.")
        return
    
    result = shows_collection.update_one(
        {'name': show_name},
        {'$set': {
            'current_season': season_number,
            'current_episode': episode_number
        }}
    )
    if result.modified_count > 0:
        print(f"Updated '{show_name}' to Season {season_number}, Episode {episode_number}.")
    else:
        print(f"No changes made to '{show_name}'.")


def add_show() -> None:
    """
    Adds a new TV show to the tracking dictionary.
    """
    tv_show_name = input("Enter TV show name: ").capitalize()
    encoded_name = quote(tv_show_name)
    url = f"https://api.themoviedb.org/3/search/tv?query={encoded_name}&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data['results']:
        print(f"No results found for '{tv_show_name}'. Please check the name and try again.")
    else:
        print(f"\nFound {len(data['results'])} result(s):\n")
        for i, show in enumerate(data['results'], 1):
        # Handle missing first_air_date
            year = show.get('first_air_date', 'Unknown')[:4] if show.get('first_air_date') else 'Unknown'
            print(f"{i}. {show['original_name']} ({year})")

    while True:
        try:
            choice = int(input("\nEnter the number of the correct show: "))
            if 1 <= choice <= len(data['results']):
                selected_show = data['results'][choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(data['results'])}")
        except ValueError:
            print("Please enter a valid number")
    
    # Now you have the selected show!
    show_id = selected_show['id']
    show_name = selected_show['original_name']
    
    print(f"\nYou selected: {show_name}")

    detail_url = f"https://api.themoviedb.org/3/tv/{show_id}?api_key={TMDB_API_KEY}"
    detail_response = requests.get(detail_url)
    detail_data = detail_response.json()
    no_of_seasons = detail_data['number_of_seasons']
    poster_path = detail_data.get('poster_path', None)

    while True:
        try:
            season_number = int(input("Enter the season you're currently watching: "))
            if season_number < 1 or season_number > no_of_seasons:
                print(f"Season number must be between 1 and {no_of_seasons}")
            else:
                break
        except ValueError:
            print("Please enter a valid integer for season number.")

    while True:
        try:
            episode_number = int(input("Enter the number of the last episode you watched: "))
            if episode_number < 1:
                print("Episode number must be at least 1")
            else:
                break
        except ValueError:
            print("Please enter a valid integer for episode number.")
    

    show_data = {
        "number_of_seasons": no_of_seasons,
        "current_season": season_number,
        "current_episode": episode_number,
        poster_path: poster_path
    }

    shows_collection.update_one(
        {'name': tv_show_name},
        {'$set': {'name': tv_show_name, **show_data}},
        upsert=True
    )
    
    print(f"Added '{tv_show_name}', Number of seasons {no_of_seasons}, Current Season {season_number}, Episode {episode_number}")

def list_shows() -> None:
    """
    Lists all TV shows in the tracking dictionary.
    """
    all_shows = shows_collection.find()
    
    if shows_collection.count_documents({}) == 0:
        print("No shows tracked yet.")
        return
    

    print("\n" + "="*60)
    print("YOUR TV SHOWS")
    print("="*60)


    for show_doc in all_shows:
        show_name = show_doc['name']
        total_seasons = show_doc['number_of_seasons']
        current_season = show_doc['current_season']
        current_episode = show_doc['current_episode']

        seasons_completed = current_season - 1
        progress_percent = (seasons_completed / total_seasons) * 100 if total_seasons > 0 else 0

        bar_length = 20
        filled_length = int(bar_length * progress_percent / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        if current_season == total_seasons:
            status = "Final Season"
        elif current_season == 1:
            status = "Just Started"
        else:
            status = "In Progress"
        print(f"\n{show_name} - {status}")
        print(f"Season {current_season}, Episode {current_episode} / {total_seasons} Seasons Total")
        print(f"Seasons Completed: {progress_percent:.0f}% [{bar}]")
    print("\n" + "="*60 + "\n")

def menu() -> None:
    """
    Displays the menu and handles user input.
    """
    while True:
        print("\nTV Show Tracker Menu:")
        print("1. Add Show")
        print("2. List Shows")
        print("3. Edit Show")
        print("4. Delete Show")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_show()
        elif choice == '2':
            list_shows()
        elif choice == '3':
            update_episode()
        elif choice == '4':
            delete_show()
        elif choice == '5':
            print("Exiting TV Show Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
