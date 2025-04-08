import pickle
import os
import requests
import nltk
import time
import re
import random

# Set NLTK data path locally
nltk.data.path.append('./nltk_data')
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
MINIMUM_SENTENCE_COUNT = 3

# Spooky Wikipedia categories
spooky_categories = [
    "Horror_genres",
    "Ghosts",
    "Reportedly_haunted_locations",
    "Paranormal",
    "Cryptids",
    "Horror_films_by_genre",
    "Ghosts_in_popular_culture",
    "Paranormal_television",
    "Hominid_cryptids",
    "Reportedly_haunted_houses",
    "Demonology",
    "Mythological_monsters",
    "Supernatural_horror_films",
    "Occult",
    "Urban_legends",
    "Witchcraft",
    "Vampires",
    "Werewolves",
    "Zombie_films"
]

def fetch_random_wikipedia_title():
    """Fetches a random Wikipedia page title."""
    try:
        params = {
            "action": "query",
            "list": "random",
            "rnlimit": 1,
            "rnnamespace": 0,
            "format": "json"
        }
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        return response.json()["query"]["random"][0]["title"]
    except Exception as e:
        print(f"Error fetching title: {e}")
        return None

def fetch_random_page_from_category(category, limit=100):
    """Fetches a random Wikipedia page title from a specified category."""
    try:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": limit,
            "cmtype": "page",
            "format": "json"
        }
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        members = response.json()["query"]["categorymembers"]
        if not members:
            print(f"No pages found in category: {category}")
            return None
        page = random.choice(members)
        return page["title"]
    except Exception as e:
        print(f"Error fetching category page: {e}")
        return None

def fetch_wikipedia_page_content(title):
    """Fetches the plaintext content of a Wikipedia page given its title."""
    try:
        params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": True,
            "titles": title,
            "format": "json"
        }
        response = requests.get(WIKIPEDIA_API_URL, params=params)
        pages = response.json()["query"]["pages"]
        return next(iter(pages.values())).get("extract", "")
    except Exception as e:
        print(f"Error fetching content: {e}")
        return None

def load_tokenizer():
    """Loads the NLTK Punkt tokenizer from local storage."""
    model_path = os.path.join('nltk_data', 'tokenizers', 'punkt', 'english.pickle')
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def divide_sentences(text):
    """Tokenizes raw text into sentences."""
    tokenizer = load_tokenizer()
    return tokenizer.tokenize(text)

def clean_sentences(sentences):
    """Cleans sentences by removing Wikipedia-specific markup."""
    cleaned = []
    for s in sentences:
        s = re.sub(r'\=\=.*?\=\=', '', s)
        s = re.sub(r'\[\[|\]\]', '', s)
        s = re.sub(r'\{\{.*?\}\}', '', s)
        s = re.sub(r'<ref.*?>.*?</ref>', '', s)
        s = re.sub(r'\n', ' ', s)
        cleaned.append(s.strip())
    return cleaned

def filter_linguistically_normal_nltk(sentences):
    """Filters sentences to retain linguistically normal sentences."""
    return [s.strip() for s in sentences if len(s) >= 20 and len(s.split()) >= 4 and not re.match(r'^[^a-zA-Z]+$', s) and not any(char in s for char in "{}[]|=*<>") and s.count('.') <= 3]

def is_sentence_appropriate(sentences):
    """Checks if the sentence count meets the minimum requirement."""
    return len(sentences) >= MINIMUM_SENTENCE_COUNT

def get_valid_wikipedia_page_info(spooky=False):
    """Fetches a valid Wikipedia page, optionally from spooky categories."""
    while True:
        title = fetch_random_page_from_category(random.choice(spooky_categories)) if spooky else fetch_random_wikipedia_title()
        content = fetch_wikipedia_page_content(title)
        sentences = filter_linguistically_normal_nltk(clean_sentences(divide_sentences(content)))
        if is_sentence_appropriate(sentences):
            return title, sentences
        time.sleep(0.5)

if __name__ == "__main__":
    title, sentences = get_valid_wikipedia_page_info(spooky=True)
    print(f"Title: {title}")
    print(f"Sentences ({len(sentences)}):")
    for sentence in sentences:
        print(sentence)