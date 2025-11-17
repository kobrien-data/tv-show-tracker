def load_shows() -> dict:
    """
    Loads the shows dictionary from a file

    Returns:
    dict: The dictionary containing TV show tracking information
    """
    import json
    import os
    
    # Check if file exists
    if not os.path.exists('shows.json'):
        return {}  # Return empty dict if no file yet
    
    # Load and return the existing data
    with open('shows.json', 'r') as f:
        return json.load(f)


def save_shows(shows: dict) -> None:
    """
    Saves the shows dictionary to a file

    Parameters:
    shows (dict): The dictionary containing TV show tracking information.

    Returns:
    None
    """
    # Simulate saving to a file
    with open('shows.json', 'w') as f:
        import json
        json.dump(shows, f, indent=4)


def add_show() -> None:
    """
    Adds a new TV show to the tracking dictionary.
    """
    tv_show_name = input("Enter TV show name: ").capitalize()
    while True:
        try:
            no_of_seasons = int(input("Enter number of seasons: "))
            if no_of_seasons <= 0:
                print("Number of seasons must be at least 1")
            else: 
                break
        except ValueError:
            print("Please enter a valid integer for number of seasons.")

    while True:
        try:
            season_number = int(input("Enter season number: "))
            if season_number < 1 or season_number > no_of_seasons:
                print(f"Season number must be between 1 and {no_of_seasons}")
            else:
                break
        except ValueError:
            print("Please enter a valid integer for season number.")

    while True:
        try:
            episode_number = int(input("Enter episode number: "))
            if episode_number < 1:
                print("Episode number must be at least 1")
            else:
                break
        except ValueError:
            print("Please enter a valid integer for episode number.")
    

    # Add the new show (this is how you create the structure)
    shows = load_shows()
    shows[tv_show_name] = {
        "number_of_seasons": no_of_seasons,
        "current_season": season_number,
        "current_episode": episode_number
    }
    
    # Save to file
    save_shows(shows)
    
    print(f"Added '{tv_show_name}', Number of seasons {no_of_seasons}, Current Season {season_number}, Episode {episode_number}")

def list_shows() -> None:
    """
    Lists all TV shows in the tracking dictionary.
    """
    shows = load_shows()
    
    if not shows:
        print("No shows tracked yet.")
        return
    

    print("\n" + "="*60)
    print("YOUR TV SHOWS")
    print("="*60)


    for show, info in shows.items():
        total_seasons = info['number_of_seasons']
        current_season = info['current_season']
        current_episode = info['current_episode']

        seasons_completed = current_season - 1
        progress_percent = ((current_season - 1) / total_seasons) * 100 if total_seasons > 0 else 0

        bar_length = 20
        filled_length = int(bar_length * progress_percent / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        if current_season == total_seasons:
            status = "Final Season"
        elif current_season == 1:
            status = "Just Started"
        else:
            status = "In Progress"
        print(f"\n{show} - {status}")
        print(f"Season {current_season}, Episode {current_episode} / {total_seasons} Seasons Total")
        print(f"Seasons Completed: {progress_percent:.0f}% [{bar}]")
    print("\n" + "="*60 + "\n")

def edit_show() -> None:
    """
    Edits an existing TV show in the tracking dictionary.
    """
    tv_show_name = input("Enter TV show name to edit: ")
    while True:
        try:
            season_number = int(input("Enter season number: "))
            episode_number = int(input("Enter episode number: "))
            break
        except ValueError:
            print("Please enter valid integers for season and episode numbers.")
    
    shows = load_shows()
    
    if tv_show_name in shows:
        shows[tv_show_name]["current_season"] = season_number
        shows[tv_show_name]["current_episode"] = episode_number
        
        # Save to file
        save_shows(shows)
        
        print(f"Updated '{tv_show_name}' to Season {season_number}, Episode {episode_number}")
    else:
        print(f"Show '{tv_show_name}' not found.")


def delete_show() -> None:
    """
    Deletes a TV show from the tracking dictionary.
    """
    tv_show_name = input("Enter TV show name to delete: ")
    
    shows = load_shows()
    
    if tv_show_name in shows:
        del shows[tv_show_name]
        
        # Save to file
        save_shows(shows)
        
        print(f"Deleted show '{tv_show_name}'")
    else:
        print(f"Show '{tv_show_name}' not found.")

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
            edit_show()
        elif choice == '4':
            delete_show()
        elif choice == '5':
            print("Exiting TV Show Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
