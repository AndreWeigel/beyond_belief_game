import random
import wiki_api
import lie_gen
import os
import textwrap

GREEN = "\033[92m"
RED = '\033[91m'
RESET = "\033[0m"

def clear_screen():
    """Clears the screen"""
    if os.name == 'nt':
        os.system('cls')
    else:
        if 'TERM' in os.environ:
            os.system('clear')
        else:
            print("\n" * 100)

def get_sentences_for_game():
    page_title, sentences = wiki_api.get_valid_wikipedia_page_info(spooky=True)
    selected_sentences = random.sample(sentences[:6], 3)
    lie_index = random.randrange(3)
    original_sentence = selected_sentences[lie_index]

    attempts = 0
    while ('=' in original_sentence or
           any(char.isdigit() for char in original_sentence) or
           attempts > 5):
        selected_sentences = random.sample(sentences[:6], 3)
        original_sentence = selected_sentences[lie_index]
        attempts += 1

    selected_sentences[lie_index] = lie_gen.generate_lie(original_sentence)
    return page_title, selected_sentences, lie_index

def print_boxed_text(lines, title=None):
    """Prints a formatted box with optional title"""
    max_width = 117  # angepasste Breite
    print(f"{GREEN}╔" + "═" * max_width + "╗")
    if title:
        title_lines = textwrap.wrap(title, max_width)
        for line in title_lines:
            print(f"║ {line.ljust(max_width)} ║")
        print("╠" + "═" * max_width + "╣")
    for line in lines:
        wrapped = textwrap.wrap(line, max_width)
        for w_line in wrapped:
            print(f"║ {w_line.ljust(max_width)} ║")
    print("╚" + "═" * max_width + "╝" + f"{RESET}")

def print_lives_and_points(lives, points):
    lives_str = f"Lives: {lives * '❤️ '}".strip()
    points_str = f"Points: {points}"
    max_width = 117
    spacing = max_width - len(lives_str) - len(points_str)
    line = lives_str + " " * spacing + points_str
    print(f"{GREEN}╔" + "═" * max_width + "╗")
    print(f"║ {line.ljust(max_width)} ║")
    print(f"╚" + "═" * max_width + "╝" + f"{RESET}")

def print_wrapped_sentence(index, sentence):
    max_width = 117
    wrapped = textwrap.wrap(sentence, width=max_width - 5)  # Platz für Nummerierung
    print("╠" + "═" * max_width + "╣")
    for i, line in enumerate(wrapped):
        if i == 0:
            print(f"║ {index}.  {line.ljust(max_width - 5)} ║")
        else:
            print(f"║      {line.ljust(max_width - 5)} ║")
    print("╚" + "═" * max_width + "╝")


def display_sentences(page_title, sentences):
    print_boxed_text([], title=f"Wikipedia Article: {page_title}")
    for idx, sentence in enumerate(sentences, 1):
        print_wrapped_sentence(idx, sentence)

def main_game_loop():
    page_title, sentences, lie_index = get_sentences_for_game()
    display_sentences(page_title, sentences)
    print_boxed_text(["What's the lie? (1-3)", ""])
    choice = int(input("Type here and press Enter: "))
    if choice == lie_index + 1:
        print(f"{GREEN}✅ You're right! ✅{RESET}")
        return True
    else:
        print(f"{RED}❌ You're wrong! ❌")
        print(f"The correct answer was: {lie_index + 1}{RESET}")
        return False

def play_game():
    lives_count = 3
    points_count = 0
    while True:
        clear_screen()
        print_lives_and_points(lives_count, points_count)

        if main_game_loop():
            points_count += 1
            print_boxed_text([f"You have {points_count} point!" if points_count == 1 else f"You have {points_count} points!"])
        else:
            lives_count -= 1
            if lives_count > 0:
                print_boxed_text([f"You have {lives_count} {'life' if lives_count == 1 else 'lives'} left!"])
            if lives_count == 0:
                print_boxed_text(["GAME OVER", f"You have {points_count} points"])
                break
        input("Press Enter to continue ")
    return points_count

if __name__ == "__main__":
    play_game()
