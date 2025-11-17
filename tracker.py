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
    tv_show_name = input("Enter TV show name: ")
    season_number = int(input("Enter season number: "))
    episode_number = int(input("Enter episode number: "))
    

    # Add the new show (this is how you create the structure)
    shows = load_shows()
    shows[tv_show_name] = {
        "current_season": season_number,
        "current_episode": episode_number
    }
    
    # Save to file
    save_shows(shows)
    
    print(f"Added '{tv_show_name}', Season {season_number}, Episode {episode_number}")

def list_shows() -> None:
    """
    Lists all TV shows in the tracking dictionary.
    """
    shows = load_shows()
    
    if not shows:
        print("No shows tracked yet.")
        return
    
    for show, info in shows.items():
        print(f"{show}: Season {info['current_season']}, Episode {info['current_episode']}")

def edit_show() -> None:
    """
    Edits an existing TV show in the tracking dictionary.
    """
    tv_show_name = input("Enter TV show name to edit: ")
    season_number = int(input("Enter new season number: "))
    episode_number = int(input("Enter new episode number: "))
    
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
