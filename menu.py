import pygame
import sys
import os
import json
import numpy as np
import game_logic

# importieren der Funktionen aus leaderboard_utils
from leaderboard_utils import load_leaderboard, save_leaderboard, update_leaderboard_if_high_score, reset_leaderboard_data



# Farben definieren
GREEN = "\033[92m"
RED = '\033[91m'
RESET = "\033[0m"

"""
LEADERBOARD_FILE = "data/leaderboard.json"

def load_leaderboard():
    ### Loads the leaderboard from a JSON file. ###
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_leaderboard(leaderboard):
    ### Saves the leaderboard to a JSON file. ###
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4, sort_keys=True)
"""

def update_leaderboard_if_high_score(player_name, score):
    ### Checks if the player's score is in the top 3 and updates the leaderboard file if needed. ### 


    # Load current leaderboard
    leaderboard = load_leaderboard()

    # Combine with new score
    all_scores = list(leaderboard.items()) + [(player_name, score)]

    # Sort by score descending, then name
    all_scores.sort(key=lambda x: (-x[1], x[0]))

    # Keep top 5
    new_top_three = dict(all_scores[:5])

    # Save updated leaderboard
    save_leaderboard(new_top_three)

    print(f"{GREEN}Leaderboard has been updated!{RESET}")



def play_music():
    """Abspielt die Musik im Hintergrund."""
    pygame.mixer.init()  # Initialisiere den Mixer
    music_path = "/Users/andreweigel/Library/Mobile Documents/com~apple~CloudDocs/beyond_belief_game/music/xxx.wav"  # Pfad zur WAV-Datei
    if os.path.exists(music_path):  # Überprüfen, ob die Datei existiert
        pygame.mixer.music.load(music_path)  # Lade die WAV-Datei
        pygame.mixer.music.play(-1)  # Spiele die Musik in einer Schleife
    else:
        print(f"{GREEN}Die Datei wurde nicht gefunden: {music_path}{RESET}")

def clear_screen():
    """Clears the screen"""
    # Check if running on Windows terminal
    if os.name == 'nt':
        os.system('cls')
    else:
        # On Unix-like systems, try clear command first
        if 'TERM' in os.environ:
            os.system('clear')
        else:
            # PyCharm built-in console fallback: print many newlines
            print("\n" * 100)


def show_leaderboard():
    """Lists all players and their scores."""
    leaderboard = load_leaderboard()
    leaderboard_list = list(leaderboard.items())
    print(f"{GREEN}Leaderboard:{RESET}")
    print()
    for player, score in leaderboard_list:
        print(f"{GREEN}{player}: {score}{RESET}")


def get_player_name():
    """Asks the user for their name."""
    # Input für den Spielernamen innerhalb eines grünen Rahmens
    print(
        f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    player_name = input(f"{GREEN}What is your name... as you step into the unknown?: {RESET}").strip()

    print(
        f"{GREEN}╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    return player_name


def play_game():
    """Handles the new game flow."""
    player_name = get_player_name()
    print(
        f"{GREEN}🕵️ Hello {player_name}, now we enter the game of truth and lies.\nTwo truths, one lie... "
        f"but only one chance to uncover it.{RESET}")
    print(f"{GREEN}╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")

    total_points = game_logic.play_game()

    # INSERT LEADERBOARD STUFF

    clear_screen()
    display_game_over_screen(total_points)

    input("Press Enter to return to main menu. ")


def reset_leaderboard():
    """Clears the leaderboard."""
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    confirm = input("Are you sure you want to reset the leaderboard? (yes/no): ")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

    if confirm.lower() == "yes":
        reset_leaderboard_data()
        print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("Leaderboard has been reset.{RESET}")
        print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
        print(f"{RESET}")


def quit_game():
    """Exits the game."""
    print("╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("❌The game has been quit. The truth remains, waiting until we meet again.❌")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")

    sys.exit()

    """
    from moviepy.editor import VideoFileClsip

    # Funktion, um das Video im Vollbildmodus anzuzeigen
    def zeige_video_vollbild(screen, video_pfad):
        # Lade das Video mit moviepy
        clip = VideoFileClip(video_pfad)

        # Bildschirmgröße ermitteln
        screen_size = screen.get_size()

    # === GIF laden von Datei ===
    def gif_aus_datei_laden(pfad):
        return Image.open(pfad)


    # === GIF in Pygame-kompatible Frames umwandeln ===
    def gif_zu_pygame_frames(gif):
        frames = []
        try:
            while True:
                frame = gif.copy().convert("RGBA")
                pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
                frames.append(pygame_frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        return frames, gif.size


    # === Hauptprogramm ===
    def show_gif():
        pygame.init()
        pygame.mixer.init()

        # Sound laden
        pust_sound = pygame.mixer.Sound("data/pusten.wav")
        sound_channel = pygame.mixer.Channel(0)  # Dedizierter Kanal für den Sound

        # GIF laden
        gif = gif_aus_datei_laden("data/BIGGY.gif")
        frames, (width, height) = gif_zu_pygame_frames(gif)

        # Vollbild-Modus aktivieren
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        pygame.display.set_caption("GIF mit Pustesound")
        clock = pygame.time.Clock()

        # Animation starten
        running = True
        frame_index = 0
        frame_delay = 100  # Millisekunden zwischen Frames
        last_update = pygame.time.get_ticks()

        # Sound starten, wenn die Animation beginnt
        sound_channel.play(pust_sound, loops=-1)  # -1 für endlose Wiederholung

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            now = pygame.time.get_ticks()
            if now - last_update > frame_delay:
                frame_index = (frame_index + 1) % len(frames)
                last_update = now

            screen.blit(frames[frame_index], (0, 0))
            pygame.display.flip()
            clock.tick(60)

        # Aufräumen beim Beenden
        sound_channel.stop()
        pygame.quit()

    show_gif()
    sys.exit()

def print_main_menu():
    """Displays the menu options to the user."""
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║ ▄▄▄▄     ▓█████▓  ██   ██▓  ▒█████▀    ███▄   ██   ▓█████▄    ▄▄▄▄   ▓█████   ██▓      ██▓  ▓██████  ████████ ║")
    print("║ ▓█████▄   ▓█      ▒██  ██▒  ▒█▒   ██▒  ██ ▀█  ██   ▒██▀ ██▌  ▓█████▄ ▓█   ▀  ▓██▒      ▓██  ▒▓█      ▓██      ║")
    print("║ ▒██▒ ▄█  █▒███     ▒██ ██░  ▒█░   ██▒  ██  ▀█ █▒   ██    █▌  ▒██▒ ▄█ █▒███   ▒██░      ▒██  ▒▒████   ▒██████  ║")
    print("║ ▒██░█▀    ▒▓█  ▄  ░ ▐██▓▒   ██   ██░▓  █▒   ▐▌█▒   ▓█▄   █▌  ▒██░█▀  ▒▓█  ▄  ▒██░      ░██  ░▒▓█  ▄  ░██▒  ░  ║")
    print("║ ░▓█  ▀█  ▓░▒████▒ ░ ██▒░    ████▓▒░▒█  █░    ██  ░ ▒████▓    ░▓█  ▀█ ▓░▒████▒ ░██████▒ ░██░ ░▒█████  ▒██░     ║")
    print("║ ░▒▓███▀  ▒░░ ▒░ ░  ██▒▒   ░           ▒░                     ░▒▓███▀ ▒░░ ▒░ ░░ ▒░▓  ░░▓  ░░ ▒░ ░ ▒ ░          ║")
    print("║ ▒░▒   ░    ░ ░  ░  ░▒░    ▒    ░ ░    ░ ▒░ ░ ▒    ░▒     ░  ░ ░  ░░ ░ ▒  ░ ▒ ░ ░ ░  ░ ░                       ║")
    print("║ ░    ░      ░   ▒ ▒ ░░  ░   ░ ▒     ░   ░ ░  ░ ░  ░   ░      ░    ░     ░ ░    ▒ ░   ░    ░ ░                 ║")
    print("║ ░           ░  ░░ ░         ░ ░           ░    ░      ░           ░  ░    ░  ░ ░     ░  ░                     ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print("╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║ Welcome to Beyond Belief: Fact or Fiction - The game where knowledge meets instinct                           ║")
    print("╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║ Three statements. One is a lie. Will your instincts guide you?                                                ║")
    print("║ Behind every fact lies a shadow. Find the one that doesn't belong.                                            ║")
    print("╠═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print("║ Menu:                                                                                                         ║")
    print("║   1. Play Game                                                                                                ║")
    print("║   2. Show Leaderboard                                                                                         ║")
    print("║   3. Reset Leaderboard                                                                                        ║")
    print("║   4. Quit Game                                                                                                ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")



def evaluate_menu_input(user_input):
    valid_choices = {'1', '2', '3', '4'}
    user_input = user_input.strip()

    if user_input in valid_choices:
        return int(user_input)
    else:
        raise ValueError("Invalid menu option. Please enter a number between 1 and 4.")


def display_game_over_screen(points_count):
    ascii_art = f"""{RED}
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  ▄█████    ▄▄▄        ███▄ ▄███▓ ▓█████     ▒█████   ██▒   █▓▓ █████  ███▀██▄                                 ║
║  ██▒  █▒  ▒████▄     ▓██▒▀█▀ ██▒ ▓█   ▀    ▒██▒  ██▒ ▓██░   █▒ ▓█   ▀ ▓██  ▒██▒                               ║
║  ███░▄▄▄  ▒██  ▀█▄   ▓██    ▓██░ ▒███      ▒██░  ██▒ ▓██  █▒░ ▒███    ▓██ ░▄█▒                                ║
║  ███  ██▓ ░██▄▄▄▄██  ▒██    ▒██  ▒▓█  ▄    ▒██   ██░  ▒██ █░ ░▒▓█  ▄  ▒██▀▀█▄                                 ║
║  ░▒████▀▒  ▓█   ▓██ ▒▒██▒   ░██▒ ░▒████▒   ░ ████▓▒░   ▒██░  ░▒████▒░ ██▓  ▒█▒                                ║
║   ░▒    ▒  ▒▒   ▓▒█ ░░ ▒░   ░  ░░ ░ ▒░ ░   ░ ▒░▒░▒░    ░▐░   ░░ ▒░ ░░  ▒▓ ░▒▓░                                ║
║    ░    ░   ▒   ▒▒  ░░  ░      ░ ░  ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░   ░▒ ░ ▒░                                ║
║  ░ ░    ░   ░   ▒    ░      ░       ░      ░ ░ ░ ▒       ░░     ░      ░░   ░                                 ║
║      ░       ░   ░       ░       ░  ░       ░ ░        ░     ░  ░   ░                                         ║
║                                                        ░                                                      ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝                                                         
    {RESET}"""
    print(ascii_art)
    print(f"{GREEN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║ Your final score: {points_count}                                                                                          ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")