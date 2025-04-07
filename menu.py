
import sys
#Beispiel

#HIER leaderboard



def show_leaderboard(leaderboard): #Beispiel
    """Lists all players and their scores."""
    leaderboard_list = list(leaderboard.items())
    print("Leaderboard:")
    print()
    for player, score in leaderboard_list:
        print(f"{player}: {score}")


def new_game():
    """Handles the new game flow."""
    players = []

    player_name = input("What is your name... as you step into the unknown?: ").strip()
    players.append(player_name)
    print(f"✅ Player '{player_name}' added.")
    print(f"🕵️ Hello {player_name}, now we enter a game of truth and lies."
          f"\nTwo truths, one lie... but only one chance to uncover it.")






def reset_leaderboard(leaderboard):
    """Clears the leaderboard."""
    confirm = input("Are you sure you want to reset the leaderboard? (yes/no): ")
    if confirm == "yes":
        leaderboard.clear()
        print("Leaderboard has been reset.")


def quit_game():
    """Exits the game."""
    print("❌The game has been quit. The truth remains, waiting until we meet again. ❌")
    sys.exit()


def print_menu():
    """Displays the menu options to the user."""
    print("----------------------------------------------------------------------------------------")
    print("🕵️‍♀️Welcome to Beyond Belief: Fact or Fiction - The game where knowledge meets instinct🕵️‍♀️")
    print("Three statements. One is a lie. Will your instincts guide you?")
    print("Behind every fact lies a shadow. Find the one that doesn't belong.")

    print("\nMenu:")
    print("1. New Game")
    print("2. Show Leaderboard")
    print("3. Reset Leaderboard")
    print("4. Quit Game")
    print()


def process_user_choice():
    """Processes the user's menu selection."""
    while True:
        print_menu()
        choice = input("Enter choice (1-4): ")
        print()

        if choice == '1':
            new_game()
        elif choice == '2':
            show_leaderboard()
        elif choice == '3':
            reset_leaderboard()
        elif choice == '4':
            quit_game()

        else:
            print("Invalid choice.")

        print()
        input("Press Enter to continue ")
        print()


def main():
    """Main function that starts the program."""
    process_user_choice()


if __name__ == "__main__":
    main()